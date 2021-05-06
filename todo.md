# Korali core

* [ ] Use new implementation of subprojects/rtnorm
* [X] remove eigen and rtnorm flags
* [X] Provide option to explicitly index the namespace hierarchy (e.g. @startNamespace0)
* [ ] change "" to <> in includes where needed (examples cxx)
* [X] integrate meson in CircleCI config
* [X] add pkg-config entry for korali installation
* [X] update Dockerfile with meson support
* [X] may need `config.h` header -- check what are all these flags in `python/korali/cxx/cflags.py`
* [X] make a `requirements.txt`

# Python module

* [X] restructure python
* [X] env script (gitignore)
* [X] add requirements.txt file (will be taken care of by pep517; see pyproject.toml file)
* [X] how to handle subproject installations with PyPI install?


# Third-party

* [X] libco and gsl
* [X] check for more third-party code to move
* [X] rename external to third-party (or subprojects)
* [Χ] optional third-party
* [X] Fix the `git clean -xdf .` in all `._fetch.sh` scripts. It will fail in a release.
* [X] doxygen and llvm dependencies
* [X] check for minimum version of GSL


# Documentation

* [X] doxygen
* [X] site


# Tests

* [X] return value in all tests
* [X] write tests in meson
* [X] configure circleci
* [X] write separate tests for each file
* [ ] check again the test in running.cxx, running.mpi, reinforcement

# FIXME

* [Χ] pybind is installed with --user and was not found by meson
* [ ] ensure correctness of korali licensing before publishing on pypi.org

## List of FIXME/TODO in code

```
examples/optimization/meson.build:# TODO: [garampat@mavt.ethz.ch; 2021-03-24] multiobjective takes more than 20 min. Excluded until fixed.
examples/study.cases/RBCRelax/data/README.md:outer solution: TODO find viscosity
examples/learning/surrogates/creation/README.rst:TODO
tests/REG-000/run_test.sh:# TODO: @Fabian: how should we test for these?
source/modules/solver/sampler/HMC/HMC._hpp:// TODO: REMOVE normal/normal.hpp
source/modules/solver/sampler/HMC/HMC.config:    "Description": "TODO: is this the number of accepted proposals?"
source/modules/solver/sampler/TMCMC/TMCMC._cpp:    // TODO: refine error treatment granularity
source/modules/solver/sampler/TMCMC/TMCMC._cpp:      // TODO: refine error treatment granularity
source/auxiliar/json.hpp:      get(); // TODO(niels): may we ignore N here?
source/modules/solver/optimizer/LMCMAES/LMCMAES._cpp:  //TODO
source/modules/solver/optimizer/CMAES/CMAES._cpp:  //TODO
source/modules/solver/optimizer/CMAES/CMAES._cpp:  //TODO
source/modules/solver/optimizer/CMAES/CMAES._cpp:  //TODO
source/modules/solver/optimizer/CMAES/CMAES._cpp:    // TODO
meson.build:# TODO: [fabianw@mavt.ethz.ch; 2021-02-13] should probably test for system cblas
examples/features/meson.build:# FIXME George: add the next two experiments
examples/features/checkpoint.resume/.test-run.py:# FIXME the following scripts fail
examples/optimization/discrete/.test-run.py:# FIXME The grid search was not tested. It crashes.
examples/optimization/multiobjective/.test-run.py:# FIXME test takes too long
examples/optimization/gradient/.test-run.py:# FIXME AdaBelief fails
examples/study.cases/covid19/src/model/sir/sir.py:    # FIXME: store common variables only once
examples/study.cases/covid19/src/model/sir/intervals.py:    # FIXME: too slow
examples/study.cases/bubblePipe/.run_test.sh:# FIXME: [garampat@mavt.ethz.ch; 2021-03-23]
examples/learning/surrogates/creation/_plot/plot_gp.ipynb:       "            /* FIXME: We get \"Resource interpreted as Image but\n",
examples/learning/meson.build:# FIXME add reinforcement to the test suite
tests/STAT-005/Makefile:# FIXME: [garampat@mavt.ethz.ch; 2021-03-23] fix cflags
tests/REG-005/run_test.sh:# FIXME: [garampat@mavt.ethz.ch; 2021-03-23]
tools/helper/set_env.sh:    # FIXME: [fabianw@mavt.ethz.ch; 2021-02-04]
tools/style/style_cxx.sh:      # FIXME: [fabianw@mavt.ethz.ch; 2021-02-17] should this not be a git submodule?
```
