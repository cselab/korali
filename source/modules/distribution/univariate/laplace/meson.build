# generated with `tools/build/korali_gen_target.py`
# If you modify this file, you likely need to modify all other
# generated targets as well.  See the generator this file was
# created with.
header_install_dir = run_command(header_path, [korali_install_headers, meson.current_source_dir()]).stdout().strip()

gen_laplace_cDXAf0 = custom_target('gen_laplace_cDXAf0',
    output: ['laplace.cpp', 'laplace.hpp'],
    input: files([
      'laplace._cpp',
      'laplace._hpp',
      'laplace.config',
    ]),
    command: [korali_gen, '--input', '@INPUT0@', '@INPUT1@', '--config', '@INPUT2@', '--output', '@OUTPUT@'],
    install: true,
    install_dir: [false, header_install_dir],
)
korali_source += gen_laplace_cDXAf0
korali_source_config += files('laplace.config')