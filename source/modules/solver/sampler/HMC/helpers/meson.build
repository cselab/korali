hmc_helpers_header = files([
 'hamiltonian_base.hpp',
 'hamiltonian_riemannian_base.hpp',
 'leapfrog_base.hpp',
 'tree_helper_euclidean.hpp',
 'hamiltonian_euclidean_base.hpp',
 'hamiltonian_riemannian_const_dense.hpp',
 'leapfrog_explicit.hpp',
 'tree_helper_riemannian.hpp',
 'hamiltonian_euclidean_dense.hpp',
 'hamiltonian_riemannian_const_diag.hpp',
 'leapfrog_implicit.hpp',
 'hamiltonian_euclidean_diag.hpp',
 'hamiltonian_riemannian_diag.hpp',
 'tree_helper_base.hpp'
])

install_headers(hmc_helpers_header,
  install_dir: run_command(header_path, [korali_install_headers, meson.current_source_dir()]).stdout().strip()
)

korali_source += hmc_helpers_header
