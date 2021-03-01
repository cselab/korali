# pure python sources
python_sources = files([
  'CMAES.py',
  'DEA.py',
  'LMCMAES.py',
  'MCMC.py',
  'MOCMAES.py',
  'Nested.py',
  'TMCMC.py',
  '__init__.py',
  '__main__.py',
  'helpers.py',
])

# Install pure Python
python.install_sources(
    python_sources,
    pure: false, # will be installed next to binaries
    subdir: korali / 'plotter'  # folder relative to site-packages to install to
)
