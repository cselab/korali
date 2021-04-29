subdir('plotter')
subdir('profiler')
subdir('rlview')

# pure python sources
python_sources = files([
    '__init__.py', 
])

# Install pure Python
python.install_sources(
    python_sources,
    pure: false, # will be installed next to binaries
    subdir: korali  # folder relative to site-packages to install to
)
