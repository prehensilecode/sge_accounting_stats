#!/usr/bin/env python3
import sys, os
import pandas as pd

accounting = pd.read_csv('../accounting_shorter', sep=':')

# write out unique values of category column
accounting['category'].drop_duplicates().to_csv('categories.csv', sep=':', index=False)
