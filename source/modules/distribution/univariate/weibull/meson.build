# generated with `tools/build/korali_gen_target.py`
# If you modify this file, you likely need to modify all other
# generated targets as well.  See the generator this file was
# created with.
header_install_dir = run_command(header_path, [korali_install_headers, meson.current_source_dir()]).stdout().strip()

gen_weibull_qur8ON = custom_target('gen_weibull_qur8ON',
    output: ['weibull.cpp', 'weibull.hpp'],
    input: files([
      'weibull._cpp',
      'weibull._hpp',
      'weibull.config',
    ]),
    command: [korali_gen, '--input', '@INPUT0@', '@INPUT1@', '--config', '@INPUT2@', '--output', '@OUTPUT@'],
    install: true,
    install_dir: [false, header_install_dir],
)
korali_source += gen_weibull_qur8ON
korali_source_config += files('weibull.config')