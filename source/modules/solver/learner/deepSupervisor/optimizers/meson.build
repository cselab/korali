deep_learner_optimizer_header = files([
  'fAdaBelief.hpp',
  'fAdagrad.hpp',
  'fAdam.hpp',
  'fCMAES.hpp',
  'fGradientBasedOptimizer.hpp',
  'fMadGrad.hpp',
  'fRMSProp.hpp'
])
install_headers(deep_learner_optimizer_header,
  install_dir: run_command(header_path, [korali_install_headers, meson.current_source_dir()]).stdout().strip()
)

deep_learner_optimizer_source = files([
  'fAdaBelief.cpp',
  'fAdagrad.cpp',
  'fAdam.cpp',
  'fCMAES.cpp',
  'fMadGrad.cpp',
  'fRMSProp.cpp'
])

korali_source += deep_learner_optimizer_header
korali_source += deep_learner_optimizer_source
