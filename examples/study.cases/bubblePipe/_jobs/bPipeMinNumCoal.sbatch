#!/bin/bash -l
#SBATCH --job-name="bPipeMinCoal"
#SBATCH --output=bPipeMinCoal_%j.out
#SBATCH --time=5:00:00
#SBATCH --nodes=128
#SBATCH --account=eth2
#SBATCH --partition=normal
#SBATCH --constraint=mc
#SBATCH --dependency=singleton

date 

cd ..

umask 022

python3 run-korali.py -c 32 --ngens 200 --objective minNumCoal --resultFolder _resultMinNumCoal

date
