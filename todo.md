# Korali core

* [ ] Use new implementation of subprojects/rtnorm
* [X] remove eigen and rtnorm flags
* [X] Provide option to explicitly index the namespace hierarchy (e.g. @startNamespace0)
* [ ] change "" to <> in includes where needed (examples cxx)
* [ ] integrate meson in CircleCI config
* [X] add pkg-config entry for korali installation
* [X] update Dockerfile with meson support
* [ ] may need `config.h` header -- check what are all these flags in `python/korali/cxx/cflags.py`


# Python module

* [X] restructure python
* [X] env script (gitignore)
* [X] add requirements.txt file (will be taken care of by pep517; see pyproject.toml file)


# Third-party

* [X] libco and gsl
* [X] check for more third-party code to move
* [X] rename external to third-party (or subprojects)
* [Χ] optional third-party
* [ ] Fix the `git clean -xdf .` in all `._fetch.sh` scripts. It will fail in a release.
* [ ] doxygen and llvm dependencies
* [ ] check for minimum version of GSL


# Documentation

* [ ] doxygen
* [ ] site


# Tests

* [X] return value in all tests
* [X] write tests in meson
* [ ] configure circleci
* [X] write separate tests for each file
* [ ] check again the test in running.cxx, running.mpi, reinforcement

# FIXME

* [Χ] pybind is installed with --user and was not found by meson
