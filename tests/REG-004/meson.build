e = find_program('./run_test.sh', required: true)

current_dir = meson.current_source_dir()

test('solvers.corner.cases', e,
      args: [current_dir],
      timeout : 1000,
      suite: 'regression',
      env: nomalloc
    )
