sample_header = files([
  'sample.hpp',
])
install_headers(sample_header,
  install_dir: run_command(header_path, [korali_install_headers, meson.current_source_dir()]).stdout().strip()
)

sample_source = files([
  'sample.cpp',
])

korali_source += sample_header
korali_source += sample_source
