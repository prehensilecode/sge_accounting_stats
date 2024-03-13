#!/bin/bash
#SBATCH --ntasks-per-node=8
#SBATCH --mem=180G
#SBATCH --time=0:30:00
#SBATCH --output=cubicstats-%j.out

source ~/Venvs/general/bin/activate
./cubicstats.py
