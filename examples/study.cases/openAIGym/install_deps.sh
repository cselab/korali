#!/bin/bash

mkdir _model/pyBulletEnvironments
git clone git@github.com:bulletphysics/bullet3.git
cp bullet3/examples/pybullet/gym/pybullet_envs/* _model/pyBulletEnvironments
rm -rf ./bullet3/ _model/pyBulletEnvironments/kerasrl_utils.py
pip install pybullet --user
