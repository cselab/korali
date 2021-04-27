project('korali', ['c', 'cpp'],
  version: '2.0.0',
  license: 'GPL-3.0-only', # or also later?
  default_options: [
    'cpp_std=c++17',
    'b_ndebug=if-release',
    'b_asneeded=false',
    'default_library=shared'
    ]
)

# compiler object
cpp = meson.get_compiler('cpp')

# configuration object
korali_conf = configuration_data()

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
korali_use_mpi = false
if user_want_mpi and mpi_dep.found()
  korali_use_mpi = true
  korali_deps += mpi_dep
elif user_want_mpi and not mpi_dep.found()
  message('''Configuration requests MPI but could not find implementation.
    Building without MPI support''')
endif

# check for OpenMP support
korali_deps += dependency('openmp', required: false)

# process required korali dependencies
korali_deps += dependency('eigen3', fallback: ['eigen', 'eigen_dep'], required: true)
# TODO: [fabianw@mavt.ethz.ch; 2021-02-13] should probably test for system cblas
# (needs benchmark: gslcblas versus system cblas (and possibly ATLAS))
korali_deps += dependency('gsl', fallback: ['gsl', 'gsl_dep'], version : '>=2.5', required: true)
korali_deps += dependency('pybind11', fallback: ['pybind11', 'pybind11_dep'], required: true)

# process optional korali dependencies
user_want_onednn = get_option('onednn')
dnnl_dep = dependency(
  'dnnl',
  required: get_option('wrap_mode') == 'nofallback',
)
korali_use_onednn = true
if user_want_onednn and (
     not dnnl_dep.found()
     or get_option('wrap_mode') == 'forcefallback'
     or 'dnnl' in get_option('force_fallback_for')
   )
  cmake = import('cmake')
  opt_var = cmake.subproject_options()
  opt_var.add_cmake_defines({
      'DNNL_BUILD_EXAMPLES': false,
      'DNNL_BUILD_TESTS': false,
      'DNNL_ENABLE_CONCURRENT_EXEC': true,
      'CMAKE_INSTALL_PREFIX': '@PREFIX@',
      'BUILD_SHARED_LIBS': true,
      })
  sub_proj = cmake.subproject('dnnl', options: opt_var)
  korali_deps += sub_proj.dependency('dnnl', version : '>=2.0', required: true)
elif user_want_onednn and dnnl_dep.found()
  korali_deps += dnnl_dep
else
  korali_use_onednn = false
endif

# FIXME: [fabianw@mavt.ethz.ch; 2021-03-26] CUDNN not tested
korali_use_cudnn = false
if get_option('cudnn') != ''
  korali_deps += cpp.find_library('cudnn', dirs: [get_option('cudnn') + '/lib64'])
  korali_use_cudnn = true
endif

korali_conf.set('_KORALI_USE_MPI', korali_use_mpi,
  description: 'Use MPI for distributed memory paralleism',
)
korali_conf.set('_KORALI_USE_ONEDNN', korali_use_onednn,
  description: 'Use Intel OndeDNN backend for Deep Neural Networks',
)
korali_conf.set('_KORALI_USE_CUDNN', korali_use_cudnn,
  description: 'Use NVIDIA CUDNN backend for Deep Neural Networks',
)

# process korali extension
subdir('source')

# process korali pure python
subdir('python/korali')

nomalloc = environment({'MALLOC_PERTURB_': '0'})
subdir('tests')
subdir('examples')
