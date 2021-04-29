#!/usr/bin/env bash


# Set number of nodes here
mpiflags="mpirun -n 2"

if [ ! -z $SLURM_NNODES ]; then
 N=$SLURM_NNODES
 mpiflags="srun -N $N -n $N -c 12"
fi

set -x

$mpiflags ./run-gfpt -poissonType cosine -muteAll 1 -tdump 0 -nu 0.000018 -tend 0 -shapes 'halfDisk_radius=.06_angle=20_xpos=.1_bForced=1_bFixed=1_xvel=0.15_tAccel=5,stefanfish_L=.2_xpos=.4_bFixedy=1' -bpdx 8 -bpdy 4 -levelMax 4 -Rtol 0.5 -Ctol 0.1
