e = find_program('./.test-run.py', required: true)
test('learning.surrogates.optimization', e,
      timeout : 1000,
      suite: 'learning',
      workdir: meson.current_source_dir(),
      depends: python_extension,
      env: nomalloc
    )
