e = find_program('./.test-run.py', required: true)
test('statistics.markov.chain', e,
      timeout : 1000,
      suite: 'statistics',
      workdir: meson.current_source_dir(),
      depends: python_extension,
      env: nomalloc
    )
