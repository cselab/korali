e = find_program('./.test-run.py', required: true)
test('sampling', e,
      timeout : 1000,
      suite: 'sampling',
      workdir: meson.current_source_dir(),
      depends: python_extension,
      env: nomalloc
    )
