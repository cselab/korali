e = find_program('./.test-run.py', required: true)
test('integration', e,
      timeout : 1000,
      suite: 'integration',
      workdir: meson.current_source_dir(),
      depends: python_extension,
      env: nomalloc
    )
