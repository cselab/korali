# generated with `tools/build/korali_gen_target.py`
# If you modify this file, you likely need to modify all other
# generated targets as well.  See the generator this file was
# created with.
header_install_dir = run_command(header_path, [korali_install_headers, meson.current_source_dir()]).stdout().strip()

gen_gru_cx76lN = custom_target('gen_gru_cx76lN',
    output: ['gru.cpp', 'gru.hpp'],
    input: files([
      'gru._cpp',
      'gru._hpp',
      'gru.config',
    ]),
    command: [korali_gen, '--input', '@INPUT0@', '@INPUT1@', '--config', '@INPUT2@', '--output', '@OUTPUT@'],
    install: true,
    install_dir: [false, header_install_dir],
)
korali_source += gen_gru_cx76lN
korali_source_config += files('gru.config')