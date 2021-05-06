***********
Korali
***********

High-performance framework for uncertainty quantification, optimization and reinforcement learning.

.. image:: https://circleci.com/gh/cselab/korali.svg?style=shield
    :target: https://circleci.com/gh/cselab/korali
    :alt: Build Status
.. image:: https://readthedocs.org/projects/korali/badge/?version=latest
    :target: https://korali.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Description
===========

Korali is a high-performance framework for Bayesian UQ, optimization, and reinforcement learning. Korali's multi-language interface allows the execution of any type of computational model, either sequential or distributed (MPI), C++ or Python, and even pre-compiled/legacy applications. Korali's execution engine enables scalable sampling on large-scale HPC systems. 

Korali provides a simple interface that allows users to easily describe statistical problems and choose the algorithms to solve them, allowing users to apply a wide range of operations on the same problem with minimal re-configuration efforts. Finally, users can easily extend Korali to describe new problems and test new experimental algorithms

Website
========

Visit: https://www.cse-lab.ethz.ch/korali/ for more information.

Folders
=======

- docker/ Contains the build file for a Korali docker image
- docs/ Contains all documentation for Korali source and website
- examples/ Contains example scripts that solve all of Korali's problem types
- python/ Contains Korali's pure python source code
- source/ Contains Korali's C++ source code (python extension)
- subprojects/ Contains external dependencies required by Korali
- tests/ Contains test scripts to verify Korali's correctness
- tools/ Contains Korali's additional tools and scripts

Contact us
==========

The Korali Project is developed and maintained by

* `Sergio Miguel Martin <https://www.cse-lab.ethz.ch/member/sergio-martin/>`_, martiser at ethz.ch
* `Daniel Wälchli <https://www.cse-lab.ethz.ch/member/daniel-walchli/>`_, wadaniel at ethz.ch
* `Georgios Arampatzis <https://www.cse-lab.ethz.ch/member/georgios-arampatzis/>`_, garampat at ethz.ch
* `Pascal Weber <https://www.cse-lab.ethz.ch/member/pascal-weber/>`_, webepasc at ethz.ch

PI:

* `Petros Koumoutsakos <https://www.cse-lab.ethz.ch/member/petros-koumoutsakos/>`_, petros at ethz.ch

Additional contributors: Lucas Amoudrouz, Ivica Kicic, Fabian Wermelinger, Susanne Keller, Mark Martori.
