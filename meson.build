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
summary({
  'buildtype': get_option('buildtype'),
  'default_library': get_option('default_library'),
  }, section: 'Build')

# compiler object
cpp = meson.get_compiler('cpp')
cpp_args = []

# configuration object
korali_conf = configuration_data()

# python installation
pymodule = import('python')
python = pymodule.find_installation('python3', required: true)

korali = 'korali' # python package name
korali_install_base = python.get_install_dir() / korali
korali_install_headers = korali_install_base / 'include'
summary({
  'prefix': korali_install_base,
  'python': python.language_version()
  }, section: 'Python')

# list of Korali dependencies
null_dep = dependency('', required : false) # used for simplification of code
korali_deps = []

# process required korali dependencies
# TODO: [fabianw@mavt.ethz.ch; 2021-02-13] should probably test for system cblas
# (needs benchmark: gslcblas versus system cblas (and possibly ATLAS))
korali_deps += dependency('gsl', fallback: ['gsl', 'gsl_dep'], version : '>=2.5', required: true)
korali_deps += dependency('eigen3', fallback: ['eigen', 'eigen_dep'], required: true)
korali_deps += dependency('pybind11', fallback: ['pybind11', 'pybind11_dep'], required: true)

# process optional korali dependencies
mpi_dep = null_dep
openmp_dep = null_dep

if get_option('mpi')
  mpi_dep = dependency('mpi', language: 'cpp')  

  if mpi_dep.found() == false
   mpi_dep = dependency('mpich', required: true)
  endif
endif

if get_option('openmp')
  openmp_dep = dependency('openmp', required: false)
endif
korali_deps += [mpi_dep, openmp_dep]

onednn_dep = null_dep
if get_option('onednn') or get_option('onednn_path') != ''
  if get_option('onednn_path') != '' # prioritized if given
    # this does not resolve other dependencies the library may depend on
    onednn_dep = cpp.find_library('dnnl',
      dirs: [
        get_option('onednn_path') / 'lib',
        get_option('onednn_path') / 'lib64'],
      required: true)
    inc = get_option('onednn_path') / 'include'
    cpp_args += '-I' + inc
    assert(cpp.has_header('dnnl.h', args: '-I' + inc))
  elif get_option('onednn')
    # preferred dependency resolution via pkg-config or cmake
    onednn_dep = dependency('dnnl', required: true)
  endif
endif
korali_deps += onednn_dep

cudnn_dep = null_dep
if get_option('cudnn') or get_option('cudnn_path') != ''
  # korali internal dependency
  korali_deps += dependency('cuda', required: true)

  # cuDNN does not provide any pkg-config or other config tools, assume it does
  # not depend on other libraries
  if get_option('cudnn_path') != '' # prioritized if given
    lib = cpp.find_library('cudnn',
      dirs: [
        get_option('cudnn_path') / 'lib',
        get_option('cudnn_path') / 'lib64'],
      required: true)
    inc = include_directories(get_option('cudnn_path') / 'include')
    cudnn_dep = declare_dependency(include_directories: inc, dependencies: lib)
  elif get_option('cudnn')
    # cuDNN is installed in system path but not discoverable
    cudnn_dep = cpp.find_library('cudnn', required: true)
  endif
  assert(cpp.has_header('cudnn.h', dependencies: cudnn_dep))
endif
korali_deps += cudnn_dep

# set configuration values
korali_conf.set('_KORALI_USE_MPI', mpi_dep.found(),
  description: 'Use MPI for distributed memory parallelism',
)
korali_conf.set('_KORALI_USE_ONEDNN', onednn_dep.found(),
  description: 'Use Intel OndeDNN backend for Deep Neural Networks',
)
korali_conf.set('_KORALI_USE_CUDNN', cudnn_dep.found(),
  description: 'Use Nvidia CUDNN backend for Deep Neural Networks (requires CUDA)',
)
summary({
  'MPI': get_option('mpi'),
  'OpenMP': openmp_dep.found(),
  'oneDNN': onednn_dep.found(),
  'cuDNN': cudnn_dep.found(),
  }, section: 'Dependencies')

# process korali extension
subdir('source')

# process korali pure python
subdir('python/korali')

# tests
if get_option('test')
  nomalloc = environment({'MALLOC_PERTURB_': '0'})
  subdir('tests')
  subdir('examples')
endif
