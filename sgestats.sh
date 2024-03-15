#!/bin/bash
#SBATCH --ntasks-per-node=8
#SBATCH --mem=32G
#SBATCH --time=0:30:00
#SBATCH --output=sgestats-%j.out

source ~/Venvs/general/bin/activate
./sgestats.py

