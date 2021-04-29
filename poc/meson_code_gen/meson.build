project('Meson-code-gen', 'cpp',
  version: '0.0',
  default_options: ['b_ndebug=if-release']
)

pymodule = import('python')
python = pymodule.find_installation('python3', required: true)

# XXX: [fabianw@mavt.ethz.ch; 2021-01-29] Generating build targets like this
# does not work because `output` requires to take a single filename and not a
# path with separators.  This enforces an opaque build definition.  The loop
# approach below violates this principle.

# generate sources and headers
_r = run_command('source/list_deps.py') # get task list
_generator = files('source/generator.py')
_gen_header_dep = []
_gen_source_dep = []
_gen_count = 0
_gen_target = 'auto_gen_target_@0@_@1@'
foreach triplet: _r.stdout().strip().split('\n')
  items = triplet.split()

  # header
  _hpp_out = join_paths((items[0] + '.hpp').split('/'))
  _gen_header_dep += custom_target(
    _gen_target.format('hpp', _gen_count),
    output: _hpp_out,
    input: [_generator, files(items[1], items[3])],
    command: [python, '@INPUT0@', '--input', '@INPUT1@', '--config', '@INPUT2@', '--output', '@OUTPUT@']
  )

  # source
  _cpp_out = join_paths((items[0] + '.cpp').split('/'))
  _gen_source_dep += custom_target(
    _gen_target.format('cpp', _gen_count),
    output: _cpp_out,
    input: [_generator, files(items[2], items[3])],
    command: [python, '@INPUT0@', '--input', '@INPUT1@', '--config', '@INPUT2@', '--output', '@OUTPUT@']
  )

  _gen_count += 1
endforeach

subdir('source')
