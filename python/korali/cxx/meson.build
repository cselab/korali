# Run flag generating command
run_command(python, './createFlags.py', cpp.cmd_array())

# pure python sources
python_sources = files([
  'flags.in',
  '__init__.py',
  '__main__.py'
])

# Install pure Python
python.install_sources(
    python_sources,
    pure: false, # will be installed next to binaries
    subdir: korali / 'cxx'  # folder relative to site-packages to install to
)
