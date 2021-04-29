# Korali core

* [ ] Use new implementation of subprojects/rtnorm
* [X] remove eigen and rtnorm flags
* [X] Provide option to explicitly index the namespace hierarchy (e.g. @startNamespace0)
* [ ] change "" to <> in includes where needed (examples cxx)
* [X] integrate meson in CircleCI config
* [X] add pkg-config entry for korali installation
* [X] update Dockerfile with meson support
* [ ] may need `config.h` header -- check what are all these flags in `python/korali/cxx/cflags.py`
* [X] make a `requirements.txt`

# Python module

* [X] restructure python
* [X] env script (gitignore)
* [X] add requirements.txt file (will be taken care of by pep517; see pyproject.toml file)
* [ ] how to handle subproject installations with PyPI install?


# Third-party

* [X] libco and gsl
* [X] check for more third-party code to move
* [X] rename external to third-party (or subprojects)
* [Χ] optional third-party
* [ ] Fix the `git clean -xdf .` in all `._fetch.sh` scripts. It will fail in a release.
* [X] doxygen and llvm dependencies
* [ ] check for minimum version of GSL


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
docker/Dockerfile:# FIXME: [fabianw@mavt.ethz.ch; 2021-02-18] use `master` branch once merged
docs/build.sh:# FIXME: [fabianw@mavt.ethz.ch; 2021-02-17] refactor doxygen into sphinx
examples/learning/surrogates/creation/README.rst:TODO
examples/learning/surrogates/creation/_plot/plot_gp.ipynb:       "            /* FIXME: We get \"Resource interpreted as Image but\n",
examples/study.cases/RBCRelax/data/README.md:outer solution: TODO find viscosity
examples/study.cases/covid19/src/model/sir/intervals.py:    # FIXME: too slow
examples/study.cases/covid19/src/model/sir/sir.py:    # FIXME: store common variables only once
meson.build:# TODO: [fabianw@mavt.ethz.ch; 2021-02-13] should probably test for system cblas
pyproject.toml:author = "Korali devs TODO"
source/auxiliar/json.hpp:      get(); // TODO(niels): may we ignore N here?
source/modules/problem/bayesian/reference/reference._cpp:  // TODO
source/modules/problem/sampling/sampling._cpp:  // TODO: Check 0 <= P(x) <= 1
source/modules/problem/sampling/sampling._cpp:  // TODO: Use Lognormalization
source/modules/solver/optimizer/CMAES/CMAES._cpp:    // TODO
source/modules/solver/optimizer/CMAES/CMAES._cpp:  //TODO
source/modules/solver/optimizer/CMAES/CMAES._cpp:  //TODO
source/modules/solver/optimizer/CMAES/CMAES._cpp:  //TODO
source/modules/solver/optimizer/LMCMAES/LMCMAES._cpp:  //TODO
source/modules/solver/sampler/TMCMC/TMCMC._cpp:      // TODO: refine error treatment granularity
source/modules/solver/sampler/TMCMC/TMCMC._cpp:    // TODO: refine error treatment granularity
tests/REG-001/run_test.sh:# FIXME: [fabianw@mavt.ethz.ch; 2021-02-17] should python code not also be checked?
tools/helper/set_env.sh:    # FIXME: [fabianw@mavt.ethz.ch; 2021-02-04] 
tools/style/style_cxx.sh:    # FIXME: [fabianw@mavt.ethz.ch; 2021-02-17] should this not be a git submodule?
```
