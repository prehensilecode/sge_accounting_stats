#!/bin/bash
#SBATCH --ntasks-per-node=8
#SBATCH --mem=180G
#SBATCH --time=8:00:00
#SBATCH --output=prune-%j.out

source ~/Venvs/general/bin/activate
./prune.py
