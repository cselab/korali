# generated with `tools/build/korali_gen_target.py`
# If you modify this file, you likely need to modify all other
# generated targets as well.  See the generator this file was
# created with.
header_install_dir = run_command(header_path, [korali_install_headers, meson.current_source_dir()]).stdout().strip()

gen_AdaBelief_yLo419 = custom_target('gen_AdaBelief_yLo419',
    output: ['AdaBelief.cpp', 'AdaBelief.hpp'],
    input: files([
      'AdaBelief._cpp',
      'AdaBelief._hpp',
      'AdaBelief.config',
    ]),
    command: [korali_gen, '--input', '@INPUT0@', '@INPUT1@', '--config', '@INPUT2@', '--output', '@OUTPUT@'],
    install: true,
    install_dir: [false, header_install_dir],
)
korali_source += gen_AdaBelief_yLo419
korali_source_config += files('AdaBelief.config')