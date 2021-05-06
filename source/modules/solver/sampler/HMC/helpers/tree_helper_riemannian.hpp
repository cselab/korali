#ifndef TREE_HELPER_RIEMANNIAN_H
#define TREE_HELPER_RIEMANNIAN_H

#include "tree_helper_base.hpp"
namespace korali
{
namespace solver
{
namespace sampler
{
/**
* \struct TreeHelperRiemannian
* @brief Riemmanian helper class for long argument list of buildTree
*/
struct TreeHelperRiemannian : public TreeHelper
{
  /**
    * @brief Computes No U-Turn Sampling (NUTS) criterion.
    * @param hamiltonian Hamiltonian object of system.
    * @return Returns of tree should be built further.
    */
  bool computeCriterion(const Hamiltonian &hamiltonian) const override
  {
    KORALI_LOG_ERROR("Wrong tree building criterion used in NUTS.");
    return false;
  }

  /**
    * @brief Computes No U-Turn Sampling (NUTS) criterion.
    * @param hamiltonian Hamiltonian object of system.
    * @param momentumStart Starting momentum of trajectory.
    * @param momentumEnd Ending momentum of trajsectory.
    * @param inverseMetric Inverse of current metric.
    * @param rho Sum of momenta encountered in trajectory.
    * @return Returns of tree should be built further.
    */
  bool computeCriterion(const Hamiltonian &hamiltonian, const std::vector<double> &momentumStart, const std::vector<double> &momentumEnd, const std::vector<double> &inverseMetric, const std::vector<double> &rho) const override
  {
    size_t dim = rho.size();
    std::vector<double> tmpVectorOne(dim, 0.0);
    std::transform(std::cbegin(rho), std::cend(rho), std::cbegin(momentumStart), std::begin(tmpVectorOne), std::minus<double>());

    std::vector<double> tmpVectorTwo(dim, 0.0);
    std::transform(std::cbegin(rho), std::cend(rho), std::cbegin(momentumStart), std::begin(tmpVectorTwo), std::minus<double>());

    double innerProductStart = hamiltonian.innerProduct(momentumStart, momentumStart, inverseMetric);
    double innerProductEnd = hamiltonian.innerProduct(momentumEnd, momentumEnd, inverseMetric);

    return innerProductStart > 0.0 && innerProductEnd > 0.0;
  }
};

} // namespace sampler
} // namespace solver
} // namespace korali

#endif
