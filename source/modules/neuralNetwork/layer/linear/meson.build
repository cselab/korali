# generated with `tools/build/korali_gen_target.py`
# If you modify this file, you likely need to modify all other
# generated targets as well.  See the generator this file was
# created with.
header_install_dir = run_command(header_path, [korali_install_headers, meson.current_source_dir()]).stdout().strip()

gen_linear_ccIbcN = custom_target('gen_linear_ccIbcN',
    output: ['linear.cpp', 'linear.hpp'],
    input: files([
      'linear._cpp',
      'linear._hpp',
      'linear.config',
    ]),
    command: [korali_gen, '--input', '@INPUT0@', '@INPUT1@', '--config', '@INPUT2@', '--output', '@OUTPUT@'],
    install: true,
    install_dir: [false, header_install_dir],
)
korali_source += gen_linear_ccIbcN
korali_source_config += files('linear.config')