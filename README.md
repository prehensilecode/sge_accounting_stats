# sge_accounting_stats
Simple stats on SGE accounting data.

## Install requirements
```
python3 -m pip install -r requirements.txt
```

### Prep
The `accounting` file must be in this directory (or modify the path in the Python scripts).

### Cut down accounting file to manageable size
```
sbatch prune.sh
```

### Run analysis
Either directly:
```
./sgestats.py
```

or submit to cluster:
```
sbatch sgestats.sh
```

### Note on use of Modin/Ray and Feather
- Modin parallelizes, and is noticeably faster
- Feather files are much faster to write and much smaller. Comparable JSON is about 4x larger, and much, much slower to read.

Using standard Pandas and doing i/o to CSV files, the `sgestats.py` job runs in about 3.5 to 4 minutes, having to munge the `category` column into their own columns. Using the Feather file, and Modin with Ray, the job runs in about 45 seconds.

N.B. was unable to pip install `modin[ray]` on Ubuntu 23.10 using Homebrew-installed Python 3.12.2
