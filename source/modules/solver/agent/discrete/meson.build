# generated with `tools/build/korali_gen_target.py`
# If you modify this file, you likely need to modify all other
# generated targets as well.  See the generator this file was
# created with.
header_install_dir = run_command(header_path, [korali_install_headers, meson.current_source_dir()]).stdout().strip()

gen_discrete_zYo8HI = custom_target('gen_discrete_zYo8HI',
    output: ['discrete.cpp', 'discrete.hpp'],
    input: files([
      'discrete._cpp',
      'discrete._hpp',
      'discrete.config',
    ]),
    command: [korali_gen, '--input', '@INPUT0@', '@INPUT1@', '--config', '@INPUT2@', '--output', '@OUTPUT@'],
    install: true,
    install_dir: [false, header_install_dir],
)
korali_source += gen_discrete_zYo8HI
korali_source_config += files('discrete.config')