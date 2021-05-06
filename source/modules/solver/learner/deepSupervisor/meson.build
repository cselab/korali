# generated with `tools/build/korali_gen_target.py`
# If you modify this file, you likely need to modify all other
# generated targets as well.  See the generator this file was
# created with.
header_install_dir = run_command(header_path, [korali_install_headers, meson.current_source_dir()]).stdout().strip()

gen_deepSupervisor_N7SDAT = custom_target('gen_deepSupervisor_N7SDAT',
    output: ['deepSupervisor.cpp', 'deepSupervisor.hpp'],
    input: files([
      'deepSupervisor._cpp',
      'deepSupervisor._hpp',
      'deepSupervisor.config',
    ]),
    command: [korali_gen, '--input', '@INPUT0@', '@INPUT1@', '--config', '@INPUT2@', '--output', '@OUTPUT@'],
    install: true,
    install_dir: [false, header_install_dir],
)
korali_source += gen_deepSupervisor_N7SDAT
korali_source_config += files('deepSupervisor.config')