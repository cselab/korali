e = find_program('./.test-run.py', required: true)
test('study.cases.lighthouse', e,
      timeout : 1000,
      suite: 'study.cases',
      workdir: meson.current_source_dir(),
      depends: python_extension,
      env: nomalloc
    )
