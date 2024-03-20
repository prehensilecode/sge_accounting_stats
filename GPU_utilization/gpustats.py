#!/usr/bin/env python3
import pandas as pd

gpustats_df = pd.read_csv('gpu_stats.csv')
gpustats_df.describe()

# shorten some GPU type names
gpustats_df.loc[gpustats_df['GPU type'] == 'Tesla P100-PCIE-12GB', 'GPU type'] = 'P100'
gpustats_df.loc[gpustats_df['GPU type'] == 'Tesla V100-PCIE-16GB', 'GPU type'] = 'V100'

# remove IDLE rows
gpustats_df = gpustats_df[gpustats_df['user'] != 'IDLE']

bygputype_df = gpustats_df[['GPU type', 'memUsed (MiB)', 'memory percentage used']].groupby('GPU type')

bygputype_df.describe()
