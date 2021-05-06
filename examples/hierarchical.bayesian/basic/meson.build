e = find_program('./.test-run.py', required: true)
test('hierarchical.bayesian.basic', e,
      timeout : 1000,
      suite: 'hierarchical.bayesian',
      workdir: meson.current_source_dir(),
      depends: python_extension,
      env: nomalloc
    )
