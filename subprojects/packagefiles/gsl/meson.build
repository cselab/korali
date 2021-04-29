project('gsl', 'c',
  meson_version : '>=0.56.0',
  default_options: ['b_ndebug=if-release']
)

# requires meson >= 0.56.0
autotools = import('unstable_external_project')

# bootstrap repo
run_command('./autogen.sh')

lib_type = get_option('default_library')
lib_opt = [
  '--prefix=@PREFIX@',
  '--libdir=@PREFIX@/@LIBDIR@',
  '--includedir=@PREFIX@/@INCLUDEDIR@',
  '--with-pic',
]
if lib_type == 'shared'
  lib_opt += '--enable-shared=yes'
  lib_opt += '--enable-static=no'
elif lib_type == 'static'
  lib_opt += '--enable-shared=no'
  lib_opt += '--enable-static=yes'
endif

gsl_project = autotools.add_project('configure',
  configure_options: lib_opt,
  verbose: true,
)

gsl_dep = declare_dependency(
  dependencies: gsl_project.dependency('gsl'),
  link_args: '-lgslcblas',
)
