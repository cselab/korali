e = find_program('./.test-run.py', required: true)
test('features.save.results', e,
      timeout : 100,
      suite: 'features',
      workdir: meson.current_source_dir(),
      depends: python_extension,
      env: nomalloc
    )
