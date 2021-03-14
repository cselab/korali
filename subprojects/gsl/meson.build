project('gsl', 'c',
  version: '2.6',
  meson_version : '>=0.56.0',
  default_options: ['b_ndebug=if-release']
)

# fetch the source
_gsl_version = meson.project_version()
_r = run_command('._fetch.sh', [_gsl_version])
if _r.returncode() != 0
  error('Failed to obtain gsl source for version ' + _gsl_version)
endif

# requires meson >= 0.56.0
mod = import('unstable_external_project')

lib_type = get_option('default_library')
p = mod.add_project('configure',
  configure_options: [
  '--prefix=@PREFIX@',
  '--libdir=@PREFIX@/@LIBDIR@',
  '--includedir=@PREFIX@/@INCLUDEDIR@',
  '--with-pic',
  '--enable-shared=no',
  '--enable-static=yes',
  ]
)

gsl_dep = declare_dependency(
  dependencies: p.dependency('gsl'),
  link_args: '-lgslcblas',
)
