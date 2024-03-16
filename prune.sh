#!/bin/bash
#SBATCH --ntasks-per-node=8
#SBATCH --mem-per-cpu=8G
#SBATCH --time=0:30:00
#SBATCH --output=prune-%j.out

source ~/Venvs/sgeacct/bin/activate

export MODIN_ENGINE=ray
export MODIN_CPUS=$SLURM_NTASKS

cp accounting $TMP
cp prune.py $TMP
cd $TMP
./prune.py
cp -f accounting_shorter $SLURM_SUBMIT_DIR
