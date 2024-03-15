#!/usr/bin/env python3
import sys, os, datetime
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import re
from pathlib import Path


def memstr_to_mebibyte(memstr: str) -> float:
    GIG = 1024.
    retval = 0.
    if memstr[-1] == 'm' or memstr[-1] == 'M':
        retval = float(memstr[:-1])
    elif memstr[-1] == 'g' or memstr[-1] == 'G':
        retval = float(memstr[:-1]) * GIG

    return retval


def parse_categories(cat):
    debug_p = False

    # takes the categories string and returns a dict in order to create new columns in the dataframe
    # we are interested only in the "-l bla bla" part

    # convert memory values to MiB
    # e.g. "-U non-deadlineusers -u zhanq -l A40=TRUE,gpu=1,gpu_A40=TRUE,h_stack=256m,h_vmem=4g,tmpfree=4g -pe threaded 32-48"
    #      -> {'gpu': 1, 'gpu_type': 'a40', 'h_stack': 256, 'h_vmem': 4*1024, 'tmpfree': 4*1024}

    if debug_p:
        print(f'DEBUG: parse_categories: type(cat) = {type(cat)}')
        print(f'DEBUG: parse_categories: cat = {cat}')

    resource_pat = re.compile(r'.*-l\ (\S*).*')
    if resource_pat.match(cat):
        resources = resource_pat.match(cat).groups(1)[0]
        if debug_p:
            print(f'DEBUG: parse_categories: resources = {resources}')
    else:
        #print(f'WARN: parse_categories: no resource request: cat = {cat}')
        #print()
        return None

    # dict to be returned
    retdict = {}

    # GPU types (complexes): A40, A100, P100, V100
    gpu_types = set(['a40', 'a100', 'p100', 'v100'])

    # we ignore the soft limits s_vmem, s_rt
    mem_types = set(['h_stack', 'h_vmem', 'tmpfree'])
    for tok in resources.split(','):
        key, val = tok.split('=')
        if key.lower() == 'gpu':
            # at some point, this became a boolean, then switched back to int
            retkey = key.lower()
            if val == 'TRUE':
                retval = 1
            else:
                retval = int(val)
        elif key.lower() in gpu_types:
            retkey = 'gpu_type'
            retval = key.lower()
        elif key.lower() in mem_types:
            retkey = key.lower()
            retval = memstr_to_mebibyte(val)
        elif key.lower() == 'hostname':
            # the accounting data already has a column "hostname" which is
            # the host allocated to the job
            retkey = 'requested_hostnames'
            retval = val
        elif key.lower() == 'h_rt':
            retkey = key.lower()
            # we have no time limit, so h_rt can be the string "INFINITY"
            # use 64-bit unsigned int
            if val.lower() == 'infinity':
                retval = np.iinfo(np.int64).max
            else:
                retval = np.int64(val)
        elif key.lower() == 'sgx':
            retkey = key.lower()
            if val.lower() == 'true':
                retval = True
            else:
                retval = False
        else:
            #print(f'WARN: unhandled key {key}; val = {val}')
            retkey = None
            retval = None

        if retkey and retval:
            retdict[retkey] = retval
        else:
            continue

    # deal with missing values
    if 'h_rt' not in retdict:
        retdict['h_rt'] = np.iinfo(np.int64).max

    if 'gpu' not in retdict:
        retdict['gpu'] = 0
        retdict['gpu_type'] = None
    else:
        # gpu in retdict but gpu_type not specified
        retdict['gpu_type'] = None

    if 'h_stack' not in retdict:
        retdict['h_stack'] = None

    if 'h_vmem' not in retdict:
        retdict['h_vmem'] = None

    if 'tmpfree' not in retdict:
        retdict['tmpfree'] = None

    if 'requested_hostnames' not in retdict:
        retdict['requested_hostnames'] = None

    if 'sgx' not in retdict:
        retdict['sgx'] = False

    if debug_p:
        print(f'DEBUG: parse_categories: retdict = {retdict}')

    return retdict


def prep_accounting(sgeacct_df):
    debug_p = False
    info_p = False
    # expand the df with stuff from the "-l resources_list"

    resources = sgeacct_df['category'].apply(parse_categories)

    if info_p:
        print(f'INFO: prep_accounting: type(resources) = {type(resources)}')

    #resources_df = pd.DataFrame(resources.tolist(), index=resources.index)
    resources_df = pd.DataFrame.from_records(resources.values, index=resources.index)

    if info_p:
        print(f'INFO: prep_accounting: sgeacct_df.describe() = \n{sgeacct_df.describe()}')
        print(f'INFO: prep_accounting: sgeacct_df.columns = \n{sgeacct_df.columns}')
        print(f'INFO: prep_accounting: sgeacct_df.head() = \n{sgeacct_df.head()}')

        print(f'INFO: prep_accounting: resources_df.describe() = \n{resources_df.describe()}')
        print(f'INFO: prep_accounting: resources_df.columns = \n{resources_df.columns}')
        print(f'INFO: prep_accounting: resources_df.head() = \n{resources_df.head()}')

    ret_df = pd.concat([sgeacct_df, resources_df], axis=1)

    if info_p:
        print( 'INFO: prep_accounting: after pd.concat()')
        print(f'INFO: prep_accounting: ret_df.columns = \n{ret_df.columns}')
        print(f'INFO: prep_accounting: ret_df.head() = \n{ret_df.head()}')

    return ret_df


def main():
    debug_p = False

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    # read in pre-filtered data
    sgeacct_df = pd.read_csv('accounting_shorter', sep=':')

    # drop all rows where start_time is earlier than submission_time
    bad_rows = sgeacct_df[sgeacct_df['start_time'] < sgeacct_df['submission_time']].index
    sgeacct_df.drop(bad_rows, inplace=True)

    sgeacct_df['submission_time'] = pd.to_datetime(sgeacct_df['submission_time'], unit='s')
    sgeacct_df['start_time'] = pd.to_datetime(sgeacct_df['start_time'], unit='s')
    sgeacct_df['end_time'] = pd.to_datetime(sgeacct_df['end_time'], unit='s')

    sgeacct_df['wait_time'] = (sgeacct_df['start_time'] - sgeacct_df['submission_time'])

    sgeacct_df = prep_accounting(sgeacct_df)

    # this is for debugging
    sgeacct_df.to_csv('accounting_postprocessed.csv', sep=':', index=False)

    if debug_p:
        print(f"DEBUG: sgeacct_df.head() = \n{sgeacct_df.head()}")
        print()

    # don't need the 'category' column - only useful for checking the accounting_postprocessed file
    sgeacct_df.drop('category', axis=1)

    print(f"Min submission_time = {sgeacct_df['submission_time'].min()} ; Min start_time = {sgeacct_df['start_time'].min()}")
    print(f"Max submission_time = {sgeacct_df['submission_time'].max()} ; Max start_time = {sgeacct_df['start_time'].max()}")
    print()

    print(f"Stats for CUBIC from {sgeacct_df['submission_time'].iloc[0]} - {sgeacct_df['end_time'].iloc[-1]}")
    print(f"No. of jobs: {len(sgeacct_df.index):.4e}")
    print(f"Median wait time = {sgeacct_df['wait_time'].median()}")
    print(f"Mean wait time = {sgeacct_df['wait_time'].mean()}")
    print(f"Min wait time = {sgeacct_df['wait_time'].min()}")
    print(f"Max wait time = {sgeacct_df['wait_time'].max()}")
    print()

    fig, ax = plt.subplots()

    n, bins, patchs = plt.hist(sgeacct_df['wait_time'].dt.total_seconds(), bins=100,
                               log=False)

    #print(f"median at {float(sgeacct_df['wait_time'].dt.total_seconds().median()) / float(sgeacct_df['wait_time'].dt.total_seconds().max())}")

    # FIXME add vertical line at the mean
    #plt.axvline(x=sgeacct_df['wait_time'].dt.total_seconds().median()/sgeacct_df['wait_time'].dt.total_seconds().max(), linestyle='dashed', color='red')

    ax.set_title('Histogram of wait time for CUBIC (Jan 01, 2023 - present)')
    ax.set_xlabel('Wait time (s)')
    ax.set_ylabel('Frequency')
    fig.tight_layout()
    plt.savefig('wait_time_all.pdf')
    plt.savefig('wait_time_all.png')
    print()


    print("Wait time for non-GPU jobs")
    nongpujobs_df = sgeacct_df[sgeacct_df['gpu'] == 0]

    if debug_p:
        print(nongpujobs_df.describe())
        print(nongpujobs_df.head())

    print(f"No. of jobs not requesting GPUs: {len(nongpujobs_df.index):.4e}")
    print(f"Median wait time = {nongpujobs_df['wait_time'].median()}")
    print(f"Mean wait time = {nongpujobs_df['wait_time'].mean()}")
    print(f"Min wait time = {nongpujobs_df['wait_time'].min()}")
    print(f"Max wait time = {nongpujobs_df['wait_time'].max()}")

    fig, ax = plt.subplots()
    n, bins, patchs = plt.hist(nongpujobs_df['wait_time'].dt.total_seconds(), bins=100,
                               log=False)
    ax.set_title('Histogram of wait time for CUBIC non-GPU jobs (Jan 01, 2023 - present)')
    ax.set_xlabel('Wait time (s)')
    ax.set_ylabel('Frequency')
    fig.tight_layout()
    plt.savefig('wait_time_nongpu.pdf')
    plt.savefig('wait_time_nongpu.png')
    print()

    print("Wait time for jobs requesting any GPU")
    gpujobs_df = sgeacct_df[sgeacct_df['gpu'] > 0]
    print(f"No. of jobs requesting GPUs of any type: {len(gpujobs_df.index):.4e}")
    print(f"Median wait time = {gpujobs_df['wait_time'].median()}")
    print(f"Mean wait time = {gpujobs_df['wait_time'].mean()}")
    print(f"Min wait time = {gpujobs_df['wait_time'].min()}")
    print(f"Max wait time = {gpujobs_df['wait_time'].max()}")
    print()

    fig, ax = plt.subplots()
    n, bins, patchs = plt.hist(gpujobs_df['wait_time'].dt.total_seconds(), bins=100,
                               log=False)
    ax.set_title('Histogram of wait time for CUBIC GPU jobs (Jan 01, 2023 - present)')
    ax.set_xlabel('Wait time (s)')
    ax.set_ylabel('Frequency')
    fig.tight_layout()
    plt.savefig('wait_time_gpu.pdf')
    plt.savefig('wait_time_gpu.png')
    print()

    print("Wait time for jobs requesting A100 GPU")
    gpua100jobs_df = sgeacct_df[(sgeacct_df['gpu'] > 0) & (sgeacct_df['gpu_type'] == 'a100')]
    print(f"No. of jobs requesting A100 GPUs: {len(gpua100jobs_df.index):.4e}")
    print(f"Median wait time = {gpua100jobs_df['wait_time'].median()}")
    print(f"Mean wait time = {gpua100jobs_df['wait_time'].mean()}")
    print(f"Min wait time = {gpua100jobs_df['wait_time'].min()}")
    print(f"Max wait time = {gpua100jobs_df['wait_time'].max()}")
    print()

    fig, ax = plt.subplots()
    n, bins, patchs = plt.hist(gpua100jobs_df['wait_time'].dt.total_seconds(), bins=100,
                               log=False)
    ax.set_title('Histogram of wait time for CUBIC A100 GPU jobs (Jan 01, 2023 - present)')
    ax.set_xlabel('Wait time (s)')
    ax.set_ylabel('Frequency')
    fig.tight_layout()
    plt.savefig('wait_time_gpu.pdf')
    plt.savefig('wait_time_gpu.png')
    print()

    print("Wait time for jobs requesting V100 GPU")
    gpuv100jobs_df = sgeacct_df[(sgeacct_df['gpu'] > 0) & (sgeacct_df['gpu_type'] == 'v100')]
    print(f"No. of jobs requesting V100 GPUs: {len(gpuv100jobs_df.index):.4e}")
    print(f"Median wait time = {gpuv100jobs_df['wait_time'].median()}")
    print(f"Mean wait time = {gpuv100jobs_df['wait_time'].mean()}")
    print(f"Min wait time = {gpuv100jobs_df['wait_time'].min()}")
    print(f"Max wait time = {gpuv100jobs_df['wait_time'].max()}")
    print()

    fig, ax = plt.subplots()
    n, bins, patchs = plt.hist(gpuv100jobs_df['wait_time'].dt.total_seconds(), bins=100,
                               log=False)
    ax.set_title('Histogram of wait time for CUBIC V100 GPU jobs (Jan 01, 2023 - present)')
    ax.set_xlabel('Wait time (s)')
    ax.set_ylabel('Frequency')
    fig.tight_layout()
    plt.savefig('wait_time_gpu.pdf')
    plt.savefig('wait_time_gpu.png')
    print()


if __name__ == '__main__':
    main()

