#libgp build
libgp_headers = files([
  'cg.h',
  'cov.h',
  'cov_factory.h',
  'cov_linear_ard.h',
  'cov_linear_one.h',
  'cov_matern3_iso.h',
  'cov_matern5_iso.h',
  'cov_noise.h',
  'cov_periodic.h',
  'cov_periodic_matern3_iso.h',
  'cov_prod.h',
  'cov_rq_iso.h',
  'cov_se_ard.h',
  'cov_se_iso.h',
  'cov_sum.h',
  'gp.h',
  'gp_utils.h',
  'input_dim_filter.h',
  'rprop.h',
  'sampleset.h',
])
install_headers(libgp_headers,
  install_dir: run_command(header_path, [korali_install_headers, meson.current_source_dir()]).stdout().strip()
)
include_directories('.')

libgp_sources = files([
  'cg.cc',
  'cov.cc',
  'cov_factory.cc',
  'cov_linear_ard.cc',
  'cov_linear_one.cc',
  'cov_matern3_iso.cc',
  'cov_matern5_iso.cc',
  'cov_noise.cc',
  'cov_periodic.cc',
  'cov_periodic_matern3_iso.cc',
  'cov_prod.cc',
  'cov_rq_iso.cc',
  'cov_se_ard.cc',
  'cov_se_iso.cc',
  'cov_sum.cc',
  'gp.cc',
  'gp_utils.cc',
  'input_dim_filter.cc',
  'rprop.cc',
  'sampleset.cc',
])

korali_source += libgp_headers
korali_source += libgp_sources
