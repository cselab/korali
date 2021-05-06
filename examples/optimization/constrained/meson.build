e = find_program('./.test-run.py', required: true)
test('optimization.constrained', e,
      timeout : 1000,
      suite: 'optimization',
      workdir: meson.current_source_dir(),
      depends: python_extension,
      env: nomalloc
    )
