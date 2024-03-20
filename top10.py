#!/usr/bin/env python3
import sys
import datetime
from pathlib import Path
import pandas as pd


def prep_accounting(sgeacct_df, debug_p: bool):
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

    acctpostproc = Path('accounting_postprocessed.feather')
    if acctpostproc.is_file():
        print(f'INFO: reading feather file {acctpostproc}')
        sgeacct_df = pd.read_feather(acctpostproc)
    else:
        print(f'ERROR: no feather file {acctpostproc}')
        sys.exit(1)

    # want entries for the last 180 days
    now = datetime.datetime.now()
    sixmonths = now - datetime.timedelta(days=(6 * 30))
    print(f'DEBUG: sixmonths = {sixmonths}')

    lastsixmonths_df = sgeacct_df[sgeacct_df['start_time'] >= sixmonths]
    usagebyuser_df = lastsixmonths_df.loc[:, ['owner', 'cpu']].groupby('owner').sum(numeric_only=True).sort_values(by='cpu', ascending=False).apply(pd.to_timedelta, unit='s').reset_index()

    print()
    print('Describe:')
    print(usagebyuser_df.describe())
    print()
    print('Head:')
    print(usagebyuser_df.head(50))
    with open('top50users.html', 'w') as htmlfile:
        htmlfile.write(usagebyuser_df.to_html(index=False, justify='right'))





if __name__ == '__main__':
    main()
