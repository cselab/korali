korali_gen_variable = find_program('../../tools/build/build_variables_header.py')
header_install_dir = run_command(header_path, [korali_install_headers, meson.current_source_dir()]).stdout().strip()

gen_variable = custom_target('gen_variable',
    output: ['variable.hpp'],
    input: [files([
      'variable._hpp',
    ]), korali_source_config],
    command: [korali_gen_variable, '--input', '@INPUT@', '--output', '@OUTPUT@'],
    install: true,
    install_dir: header_install_dir,
)
korali_source += gen_variable
