#!/usr/bin/env python3
import sys, os
import csv
import re

res_pat = re.compile(r'.*-l\ (\S+)\ .*')

with open('categories.csv') as csvfile:
    cat_reader = csv.reader(csvfile, delimiter=':')
    for row in cat_reader:
        #print(', '.join(row))
        match = res_pat.match(row[0])
        if match:
            print(f'match.groups()[0] = {match.groups()[0]}')
        else:
            pass
            #print(f'no match; row = {row}')

