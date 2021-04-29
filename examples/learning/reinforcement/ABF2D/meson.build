e = find_program('./.run_test.sh', required: true)

current_dir = meson.current_source_dir()

test('Reinforcement ABF2D', e,
      args: [current_dir],
      timeout : 100,
      suite: 'Learning'
    )