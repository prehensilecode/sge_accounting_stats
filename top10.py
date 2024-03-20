#!/usr/bin/env python3
import sys
import datetime
from pathlib import Path
import pandas as pd


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

    # drop project pseudo users (manual list for now)
    users_to_drop = set(['niagads', 'nbthetaconn', 'rbc', 'pennlincqsm',
                         'tumordti', 'hbcddev', 'cardiauser', 'abcdqsiprep',
                         'publicstudies', 'autismuser', 'luowmdev',
                         'cbpdmaindata', 'mesa', 'bpdmaindata',
                         'multisitemd', 'superres', 'socialbrainreconfig',
                         'dbtai', 'psychanalysis', 'aslprep', 'ipp',
                         'blsauser', 'accorduser', 'pfnabcd', 'ccbt',
                         'sprintuser', 'tcgaluaddatareleases',
                         'ukbbprocessed', 'tmsbp', 'oasis', 'braintumoruser',
                         'adniuser', 'ukbbdatareleases', 'bbluser', 'rtfmri',
                         'networkreplication', 'anxiousmisery', 'respondvalidation',
                         'chistosrubencases', 'sleepplasticity', 'wolfintrinsic',
                         'whimuser', 'aibl', 'ashpfnsexdiffabcd', 'recover',
                         'chrisclarkuser', 'preventad', 'biocard', 'lookaheaduser',
                         'preclinicalad', 'tbi', 'pigtbi', 'braintumorexternal',
                         'bridgeport', 'calico', ])

    sgeacct_df = sgeacct_df[~sgeacct_df['owner'].isin(users_to_drop)]

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
