#!/usr/bin/env python3
import sys, os, datetime
import pandas as pd
import matplotlib

colnames=['qname', 'hostname', 'group', 'owner', 'job_name', 'job_number', 'account', 'priority', 'submission_time', 'start_time', 'end_time', 'failed', 'exit_status', 'ru_wallclock', 'ru_utime', 'ru_stime', 'ru_maxrss', 'ru_ixrss', 'ru_ismrss', 'ru_idrss', 'ru_isrss', 'ru_minflt', 'ru_majflt', 'ru_nswap', 'ru_inblock', 'ru_oublock', 'ru_msgsnd', 'ru_msgrcv', 'ru_nsignals', 'ru_nvcsw', 'ru_nivcsw', 'project', 'department', 'granted_pe', 'slots', 'task_number', 'cpu', 'mem', 'io', 'category', 'iow', 'pe_taskid', 'maxvmem', 'arid', 'ar_sub_time']

cubic_df = pd.read_csv('accounting', sep=':', names=colnames)

# keep all rows that occurred after 2023-01-01 00:00:00 = timestamp 1672549200
cubic_df = cubic_df[cubic_df['submission_time'] > 1672549200]

# keep all rows that ocurred before 2024-01-01 00:00:00 = timestamp 1704085200
#cubic_df = cubic_df[cubic_df['submission_time'] < 1704085200]

# selective
wanted_cols = ['qname', 'hostname', 'owner', 'job_number', 'submission_time', 'start_time', 'end_time', 'failed', 'exit_status', 'ru_wallclock', 'ru_utime', 'slots', 'cpu', 'mem', 'io', 'iow', 'maxvmem']

cubic_df.to_csv('accounting_shorter', columns=wanted_cols, sep=':', index=False)

