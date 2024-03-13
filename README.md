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
./cubicstats.py
```

or submit to cluster:
```
sbatch cubicstats.sh
```
