#!/usr/bin/env python3
import sys, os, datetime
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# read in pre-filtered data 
cubic_df = pd.read_csv('accounting_shorter', sep=':')

# drop all rows where start_time is earlier than submission_time
bad_rows = cubic_df[cubic_df['start_time'] < cubic_df['submission_time']].index
cubic_df.drop(bad_rows, inplace=True)

cubic_df['submission_time'] = pd.to_datetime(cubic_df['submission_time'], unit='s')
cubic_df['start_time'] = pd.to_datetime(cubic_df['start_time'], unit='s')
cubic_df['end_time'] = pd.to_datetime(cubic_df['end_time'], unit='s')

cubic_df['wait_time'] = (cubic_df['start_time'] - cubic_df['submission_time'])

print(f"Min submission_time = {cubic_df['submission_time'].min()} ; Min start_time = {cubic_df['start_time'].min()}")
print(f"Max submission_time = {cubic_df['submission_time'].max()} ; Max start_time = {cubic_df['start_time'].max()}")

print(f"Stats for CUBIC from {cubic_df['submission_time'].iloc[0]} - {cubic_df['end_time'].iloc[-1]}")
print(f"Median wait time = {cubic_df['wait_time'].median()}")
print(f"Mean wait time = {cubic_df['wait_time'].mean()}")
print(f"Min wait time = {cubic_df['wait_time'].min()}")
print(f"Max wait time = {cubic_df['wait_time'].max()}")

fig, ax = plt.subplots()

n, bins, patchs = plt.hist(cubic_df['wait_time'].dt.total_seconds(), bins=100,
                           log=False)

# add vertical line at the mean
print(f"median at {float(cubic_df['wait_time'].dt.total_seconds().median()) / float(cubic_df['wait_time'].dt.total_seconds().max())}")
#plt.axvline(x=cubic_df['wait_time'].dt.total_seconds().median()/cubic_df['wait_time'].dt.total_seconds().max(), linestyle='dashed', color='red')
ax.set_title('Histogram of wait time for CUBIC (Jan 01, 2023 - present)')
ax.set_xlabel('Wait time (s)')
ax.set_ylabel('Frequency')
fig.tight_layout()
plt.savefig('wait_time.pdf')
plt.savefig('wait_time.png')

print(cubic_df.groupby(cubic_df['submission_time'].dt.month)['wait_time'])
