# libco build
include_directories('.')
install_headers('libco.h',
  install_dir: run_command(header_path, [korali_install_headers, meson.current_source_dir()]).stdout().strip()
)

korali_source += files([
  'libco.c',
  'libco.h',
  ])
