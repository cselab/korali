e = find_program('./.run_test.sh', required: true)

current_dir = meson.current_source_dir()

test('RBC Relax', e,
      args: [current_dir],
      timeout : 100,
      suite: 'Study Cases'
    )