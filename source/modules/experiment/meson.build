# generated with `tools/build/korali_gen_target.py`
# If you modify this file, you likely need to modify all other
# generated targets as well.  See the generator this file was
# created with.
header_install_dir = run_command(header_path, [korali_install_headers, meson.current_source_dir()]).stdout().strip()

gen_experiment_6A005v = custom_target('gen_experiment_6A005v',
    output: ['experiment.cpp', 'experiment.hpp'],
    input: files([
      'experiment._cpp',
      'experiment._hpp',
      'experiment.config',
    ]),
    command: [korali_gen, '--input', '@INPUT0@', '@INPUT1@', '--config', '@INPUT2@', '--output', '@OUTPUT@'],
    install: true,
    install_dir: [false, header_install_dir],
)
korali_source += gen_experiment_6A005v
korali_source_config += files('experiment.config')