# libco build
project('rtnorm', 'cpp',
  default_options: ['b_ndebug=if-release']
)

openmp_dep = dependency('openmp', required: false)

src = files([
  'rtnorm.cpp',
  'qnorm.cpp',
  ])
inc = include_directories('.')
install_headers('rtnorm.hpp', 'rtnorm_constants.hpp')
librtnorm = static_library('rtnorm', src, 
  dependencies: openmp_dep, 
  include_directories: inc, 
  pic: true, 
  install: true
)

# create dependency object that is used by dependent project
librtnorm_dep = declare_dependency(
  dependencies: openmp_dep, 
  include_directories: inc, 
  link_with: librtnorm
)
