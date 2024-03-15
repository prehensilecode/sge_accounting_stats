#!/bin/bash
#SBATCH --ntasks-per-node=8
#SBATCH --mem=180G
#SBATCH --time=0:30:00
#SBATCH --output=sgestats-%j.out

source ~/Venvs/general/bin/activate
cp -f accounting* $TMP
cp sgestats.py $TMP
cd $TMP
./sgestats.py

