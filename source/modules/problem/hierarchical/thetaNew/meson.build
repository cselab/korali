# generated with `tools/build/korali_gen_target.py`
# If you modify this file, you likely need to modify all other
# generated targets as well.  See the generator this file was
# created with.
header_install_dir = run_command(header_path, [korali_install_headers, meson.current_source_dir()]).stdout().strip()

gen_thetaNew_TekxdD = custom_target('gen_thetaNew_TekxdD',
    output: ['thetaNew.cpp', 'thetaNew.hpp'],
    input: files([
      'thetaNew._cpp',
      'thetaNew._hpp',
      'thetaNew.config',
    ]),
    command: [korali_gen, '--input', '@INPUT0@', '@INPUT1@', '--config', '@INPUT2@', '--output', '@OUTPUT@'],
    install: true,
    install_dir: [false, header_install_dir],
)
korali_source += gen_thetaNew_TekxdD
korali_source_config += files('thetaNew.config')