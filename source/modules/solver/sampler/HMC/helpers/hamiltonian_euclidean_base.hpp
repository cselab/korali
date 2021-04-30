#ifndef HAMILTONIAN_EUCLIDEAN_BASE_H
#define HAMILTONIAN_EUCLIDEAN_BASE_H

#include "hamiltonian_base.hpp"
#include "modules/conduit/conduit.hpp"

#include "engine.hpp"
#include "modules/experiment/experiment.hpp"
#include "modules/problem/problem.hpp"
#include "modules/solver/sampler/MCMC/MCMC.hpp"
#include "sample/sample.hpp"

namespace korali
{
namespace solver
{
namespace sampler
{
/**
* \class HamiltonianEuclidean
* @brief Abstract base class for Euclidean Hamiltonian objects.
*/
class HamiltonianEuclidean : public Hamiltonian
{
  public:
  /**
  * @brief Default constructor.
  */
  HamiltonianEuclidean() = default;

  /**
  * @brief Constructor with State Space Dim.
  * @param stateSpaceDim Dimension of State Space.
  * @param k Pointer to Korali object.
  */
  HamiltonianEuclidean(const size_t stateSpaceDim, korali::Experiment *k) : Hamiltonian{stateSpaceDim, k} {}

  /**
  * @brief Destructor of abstract base class.
  */
  virtual ~HamiltonianEuclidean() = default;

  /**
  * @brief Calculates tau(q, p) = 0.5 * momentum^T * inverseMetric(q) * momentum.
  * @param momentum Current momentum.
  * @param inverseMetric Current inverseMetric.
  * @return Gradient of Kinetic energy with current momentum.
  */
  double tau(const std::vector<double> &momentum, const std::vector<double> &inverseMetric) override
  {
    return K(momentum, inverseMetric);
  }

  /**
  * @brief Calculates gradient of tau(q, p) wrt. position.
  * @param momentum Current momentum.
  * @param inverseMetric Current inverseMetric.
  * @return Gradient of Kinetic energy with current momentum.
  */
  std::vector<double> dtau_dq(const std::vector<double> &momentum, const std::vector<double> &inverseMetric) override
  {
    return std::vector<double>(_stateSpaceDim, 0.0);
  }

  /**
  * @brief Calculates gradient of tau(q, p) wrt. momentum.
  * @param momentum Current momentum.
  * @param inverseMetric Current inverseMetric.
  * @return Gradient of Kinetic energy with current momentum.
  */
  std::vector<double> dtau_dp(const std::vector<double> &momentum, const std::vector<double> &inverseMetric) override
  {
    return dK(momentum, inverseMetric);
  }

  /**
  * @brief Calculates gradient of kinetic energy.
  * @return Gradient of kinetic energy.
  */
  double phi() override
  {
    return U();
  }

  /**
  * @brief Calculates gradient of kinetic energy.
  * @return Gradient of kinetic energy.
  */
  std::vector<double> dphi_dq() override
  {
    return dU();
  }
};

} // namespace sampler
} // namespace solver
} // namespace korali

#endif
