# generated with `tools/build/korali_gen_target.py`
# If you modify this file, you likely need to modify all other
# generated targets as well.  See the generator this file was
# created with.
header_install_dir = run_command(header_path, [korali_install_headers, meson.current_source_dir()]).stdout().strip()

gen_sampler_eKxDJF = custom_target('gen_sampler_eKxDJF',
    output: ['sampler.cpp', 'sampler.hpp'],
    input: files([
      'sampler._cpp',
      'sampler._hpp',
      'sampler.config',
    ]),
    command: [korali_gen, '--input', '@INPUT0@', '@INPUT1@', '--config', '@INPUT2@', '--output', '@OUTPUT@'],
    install: true,
    install_dir: [false, header_install_dir],
)
korali_source += gen_sampler_eKxDJF
korali_source_config += files('sampler.config')