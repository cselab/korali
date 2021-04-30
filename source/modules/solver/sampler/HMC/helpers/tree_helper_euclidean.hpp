#ifndef TREE_HELPER_EUCLIDEAN_H
#define TREE_HELPER_EUCLIDEAN_H

#include "tree_helper_base.hpp"
namespace korali
{
namespace solver
{
namespace sampler
{
/**
* \struct TreeHelperEuclidean
* @brief Euclidean helper class for long argument list of buildTree
*/
struct TreeHelperEuclidean : public TreeHelper
{
  /**
    * @brief Computes No U-Turn Sampling (NUTS) criterion
    * @param hamiltonian Hamiltonian object of system
    * @return Returns of tree should be built further.
    */
  bool computeCriterion(const Hamiltonian &hamiltonian) const override
  {
    return hamiltonian.computeStandardCriterion(qLeftOut, pLeftOut, qRightOut, pRightOut);
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
    KORALI_LOG_ERROR("Wrong tree building criterion used in NUTS.");
    return false;
  }
};

} // namespace sampler
} // namespace solver
} // namespace korali

#endif
