e = find_program('./run_test.sh', required: true)

current_dir = meson.current_source_dir()

test('korali.installation', e,
      args: [current_dir],
      timeout : 1000,
      suite: 'installation'
    )