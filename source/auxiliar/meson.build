auxiliar_header = files([
  'cbuffer.hpp',
  'cudaUtils.hpp',
  'dnnUtils.hpp',
  'fs.hpp',
  'json.hpp',
  'jsonInterface.hpp',
  'kcache.hpp',
  'koraliJson.hpp',
  'kstring.hpp',
  'logger.hpp',
  'math.hpp',
  'py2json.hpp',
])
install_headers(auxiliar_header,
  install_dir: run_command(header_path, [korali_install_headers, meson.current_source_dir()]).stdout().strip()
)

auxiliar_source = files([
  'fs.cpp',
  'jsonInterface.cpp',
  'koraliJson.cpp',
  'kstring.cpp',
  'logger.cpp',
  'math.cpp',
])

korali_source += auxiliar_header
korali_source += auxiliar_source

subdir('libco')
subdir('libgp')
subdir('rtnorm')
