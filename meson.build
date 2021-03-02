project('Korali', ['c', 'cpp'],
  version: '2.0.0',
  license: 'GPL-3.0-only', # or also later?
  default_options: [
    'cpp_std=c++17',
    'b_ndebug=if-release',
    'default_library=shared',
    ]
)

# python installation
pymodule = import('python')
python = pymodule.find_installation('python3', required: true)

korali = 'korali' # python package name
korali_extension = 'libkorali' # cpp extensions name
korali_install_base = python.get_install_dir() / korali
korali_install_headers = korali_install_base / 'include'

# list of Korali dependencies
korali_deps = []
korali_cpp_args = []

# check for MPI
mpi_dep = dependency('mpi', language: 'cpp', required: false)
user_want_mpi = get_option('mpi')
if user_want_mpi and mpi_dep.found()
  korali_deps += mpi_dep
  korali_cpp_args += '-D_KORALI_USE_MPI'
elif user_want_mpi and not mpi_dep.found()
  message('''Configuration requests MPI but could not find implementation.
    Building without MPI support''')
endif

# check for OpenMP support
korali_deps += dependency('openmp', required: false)


# process optional korali dependencies
onednn_dep = dependency('onednn', required: false)
user_want_onednn = get_option('onednn')
if user_want_onednn and onednn_dep.found()
  korali_deps += onednn_dep
  korali_cpp_args += '-D_KORALI_USE_ONEDNN'
elif user_want_onednn and not onednn_dep.found()
  onednn_version = '2.0'
  _r = run_command('subprojects/onednn/._fetch.sh', [onednn_version, join_paths('subprojects','onednn')])
  if _r.returncode() != 0
    error('Failed to obtain onednn source for version ' + onednn_version)
  endif

  cmake = import('cmake')

  opt_var = cmake.subproject_options()
  opt_var.add_cmake_defines({
      'DNNL_BUILD_EXAMPLES': false,
      'DNNL_BUILD_TESTS': false,
      'DNNL_ENABLE_CONCURRENT_EXEC': true,
      'CMAKE_INSTALL_PREFIX': '@PREFIX@',
      'DNNL_CPU_RUNTIME': 'SEQ',
      'BUILD_SHARED_LIBS': true,
      })

  sub_proj = cmake.subproject('onednn', options: opt_var)

  korali_deps += sub_proj.dependency('dnnl')
  korali_cpp_args += '-D_KORALI_USE_ONEDNN'
endif

# process required korali dependencies
korali_deps += dependency('eigen3', fallback: ['eigen', 'eigen_dep'], required: true)
# TODO: [fabianw@mavt.ethz.ch; 2021-02-13] should probably test for system cblas
# (needs benchmark: gslcblas versus system cblas (and possibly ATLAS))
korali_deps += dependency('gsl', fallback: ['gsl', 'gsl_dep'], required: true)
korali_deps += dependency('libco', fallback: ['libco', 'libco_dep'], required: true)
korali_deps += dependency('libgp', fallback: ['libgp', 'libgp_dep'], required: true)
korali_deps += dependency('pybind11', fallback: ['pybind11', 'pybind11_dep'], required: true)
korali_deps += dependency('rtnorm', fallback: ['rtnorm', 'rtnorm_dep'], required: true)


# process korali extension
subdir('source')

# process korali pure python
subdir('python/korali')

nomalloc = environment({'MALLOC_PERTURB_': '0'})
subdir('tests')
subdir('examples')

# create symbolic link to shared library (used for pkg-config later)
meson.add_install_script('tools/build/post_install.sh', korali_install_base, korali_extension)

# create a pkg-config entry
pkg_mod = import('pkgconfig')
pkg_mod.generate(
  name: 'Korali',
  filebase: 'korali',
  description: 'High-Performance Uncertainty Quantification, Optimization, and DRL',
  extra_cflags: ['-I' + korali_install_headers],
  libraries: ['-L' + korali_install_base, '-l' + korali]
)
