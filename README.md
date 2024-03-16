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
1. Modin parallelizes, and is noticeably faster
2. Feather files are much faster to write and much smaller. Comparable JSON is about 4x larger, and much, much slower to read.

