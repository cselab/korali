e = find_program('./.test-run.py', required: true)
test('propagation', e,
      timeout : 1000,
      suite: 'propagation',
      workdir: meson.current_source_dir(),
      depends: python_extension,
      env: nomalloc
    )
