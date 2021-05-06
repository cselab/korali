#ifndef LEAPFROG_IMPLICIT_H
#define LEAPFROG_IMPLICIT_H

#include "engine.hpp"
#include "hamiltonian_base.hpp"
#include "hamiltonian_riemannian_base.hpp"
#include "leapfrog_base.hpp"

#include <limits>

namespace korali
{
namespace solver
{
namespace sampler
{
/**
* \class LeapfrogImplicit
* @brief Used for time propagation according to hamiltonian dynamics via implicit Leapfrog integration.
*/
class LeapfrogImplicit : public Leapfrog
{
  private:
  /**
  * @brief Maximum fixed point iterations during each step.
  */
  size_t _maxNumFixedPointIter;

  public:
  /**
  * @brief Constructor for implicit leapfrog stepper.
  * @param maxNumFixedPointIter Maximum fixed point iterations.
  * @param hamiltonian Hamiltonian of the system.
  */
  LeapfrogImplicit(size_t maxNumFixedPointIter, std::shared_ptr<Hamiltonian> hamiltonian) : Leapfrog(hamiltonian), _maxNumFixedPointIter(maxNumFixedPointIter){};
  /**
  * @brief Implicit Leapfrog stepping scheme used for evolving Hamiltonian Dynamics.
  * @param position Position which is evolved.
  * @param momentum Momentum which is evolved.
  * @param metric Current metric.
  * @param inverseMetric Inverse of current metric.
  * @param stepSize Step Size used for Leap Frog Scheme.
  */
  void step(std::vector<double> &position, std::vector<double> &momentum, std::vector<double> &metric, std::vector<double> &inverseMetric, const double stepSize) override
  {
    size_t dim = momentum.size();
    double delta = 1e-6 * stepSize;

    // half step of momentum
    _hamiltonian->updateHamiltonian(position, metric, inverseMetric);
    std::vector<double> dphi_dq = _hamiltonian->dphi_dq();
    for (size_t i = 0; i < dim; ++i)
    {
      momentum[i] = momentum[i] - stepSize / 2.0 * dphi_dq[i];
    }

    std::vector<double> rho = momentum;
    std::vector<double> momentumPrime(dim);
    double deltaP;

    size_t numIter = 0;
    do
    {
      deltaP = 0.0;
      _hamiltonian->updateHamiltonian(position, metric, inverseMetric);
      std::vector<double> dtau_dq = _hamiltonian->dtau_dq(position, inverseMetric);
      for (size_t i = 0; i < dim; ++i)
      {
        momentumPrime[i] = rho[i] - stepSize / 2.0 * dtau_dq[i];
      }

      // find max delta
      for (size_t i = 0; i < dim; ++i)
      {
        if (std::abs(momentum[i] - momentumPrime[i]) > deltaP)
        {
          deltaP = std::abs(momentum[i] - momentumPrime[i]);
        }
      }

      momentum = momentumPrime;
      ++numIter;

    } while (deltaP > delta && numIter < _maxNumFixedPointIter);

    std::vector<double> positionPrime(dim);
    std::vector<double> sigma = position;
    double deltaQ;

    numIter = 0;
    do
    {
      deltaQ = 0.0;
      _hamiltonian->updateHamiltonian(sigma, metric, inverseMetric);
      std::vector<double> dtau_dp_sigma = _hamiltonian->dtau_dp(momentum, inverseMetric);
      _hamiltonian->updateHamiltonian(position, metric, inverseMetric);
      std::vector<double> dtau_dp_q = _hamiltonian->dtau_dp(momentum, inverseMetric);
      for (size_t i = 0; i < dim; ++i)
      {
        positionPrime[i] = sigma[i] + stepSize / 2.0 * dtau_dp_sigma[i] + stepSize / 2.0 * dtau_dp_q[i];
      }

      // find max delta
      for (size_t i = 0; i < dim; ++i)
      {
        if (std::abs(position[i] - positionPrime[i]) > deltaQ)
        {
          deltaQ = std::abs(position[i] - positionPrime[i]);
        }
      }

      position = positionPrime;
      ++numIter;
    } while (deltaQ > delta && numIter < _maxNumFixedPointIter);

    _hamiltonian->updateHamiltonian(position, metric, inverseMetric);
    std::vector<double> dtau_dq = _hamiltonian->dtau_dq(momentum, inverseMetric);
    for (size_t i = 0; i < dim; ++i)
    {
      momentum[i] = momentum[i] - stepSize / 2.0 * dtau_dq[i];
    }

    dphi_dq = _hamiltonian->dphi_dq();
    for (size_t i = 0; i < dim; ++i)
    {
      momentum[i] = momentum[i] - stepSize / 2.0 * dphi_dq[i];
    }
  }
};

} // namespace sampler
} // namespace solver
} // namespace korali

#endif
