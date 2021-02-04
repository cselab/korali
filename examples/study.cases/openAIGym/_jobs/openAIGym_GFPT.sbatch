#!/bin/bash -l
#SBATCH --job-name="OpenAIGym_GFPT"
#SBATCH --output=OpenAIGym_GFPT_%j.out
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-core=1
#SBATCH --ntasks-per-node=1
#SBATCH --account=eth2
#SBATCH --cpus-per-task=1
#SBATCH --partition=normal
#SBATCH --constraint=mc

# Choose Environment
#env=Ant-v2
#env=HalfCheetah-v2
#env=Hopper-v2
#env=Humanoid-v2
#env=HumanoidStandup-v2
#env=InvertedDoublePendulum-v2
#env=InvertedPendulum-v2
#env=Reacher-v2
#env=Swimmer-v2
#env=Walker2d-v2

env=AntBulletEnv-v0
#env=HalfCheetahBulletEnv-v0
#env=HopperBulletEnv-v0
#env=HumanoidBulletEnv-v0
#env=HumanoidFlagrunHarderBulletEnv-v0
#env=InvertedDoublePendulumBulletEnv-v0
#env=InvertedPendulumBulletEnv-v0
#env=InvertedPendulumSwingupBulletEnv-v0
#env=Walker2DBulletEnv-v0

pushd ..

cat run-gfpt.py

expDir=$SCRATCH/OpenAIGym_GFPT/$SLURM_JOB_ID
mkdir -p $expDir
cp run-gfpt.py $expDir
cp -r _model $expDir

popd

pushd $expDir

OMP_NUM_THREADS=36 python3 run-gfpt.py --env $env

popd

date
