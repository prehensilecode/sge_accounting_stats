#!/bin/bash
#SBATCH --ntasks-per-node=8
#SBATCH --mem-per-cpu=16G
#SBATCH --time=0:30:00
#SBATCH --output=sgestats-%j.out

source ~/Venvs/sgeacct/bin/activate

export MODIN_ENGINE=ray
export MODIN_CPUS=$SLURM_NTASKS

cp -f accounting* $TMP
cp sgestats.py $TMP
cd $TMP
./sgestats.py
cp accounting_postprocessed* $SLURM_SUBMIT_DIR
cp *.png *.pdf $SLURM_SUBMIT_DIR
