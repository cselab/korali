# libco build
include_directories('.')
install_headers('rtnorm.hpp',
  install_dir: run_command(header_path, [korali_install_headers, meson.current_source_dir()]).stdout().strip()
)

korali_source += files([
  'rtnorm.cpp',
  'rtnorm.hpp',
  ])
