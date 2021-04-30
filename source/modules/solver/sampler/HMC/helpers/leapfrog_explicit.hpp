#ifndef LEAPFROG_EXPLICIT_H
#define LEAPFROG_EXPLICIT_H

#include "hamiltonian_base.hpp"
#include "leapfrog_base.hpp"

namespace korali
{
namespace solver
{
namespace sampler
{
/**
* \class LeapfrogExplicit
* @brief Used for time propagation according to hamiltonian dynamics via explicit Leapfrog integration.
*/
class LeapfrogExplicit : public Leapfrog
{
  public:
  /**
  * @brief Constructor for explicit leapfrog stepper.
  * @param hamiltonian Hamiltonian of the system.
  */
  LeapfrogExplicit(std::shared_ptr<Hamiltonian> hamiltonian) : Leapfrog(hamiltonian){};

  /**
   * @brief Default destructor
   */
  virtual ~LeapfrogExplicit() = default;

  /**
  * @brief Explicit Leapfrog stepping scheme used for evolving Hamiltonian Dynamics.
  * @param position Position which is evolved.
  * @param momentum Momentum which is evolved.
  * @param metric Current metric.
  * @param inverseMetric Inverse of current metric.
  * @param stepSize Step Size used for Leap Frog Scheme.
  */
  void step(std::vector<double> &position, std::vector<double> &momentum, std::vector<double> &metric, std::vector<double> &inverseMetric, const double stepSize) override
  {
    _hamiltonian->updateHamiltonian(position, metric, inverseMetric);
    std::vector<double> dU = _hamiltonian->dU();

    for (size_t i = 0; i < dU.size(); ++i)
    {
      momentum[i] -= 0.5 * stepSize * dU[i];
    }

    // would need to update in Riemannian case
    std::vector<double> dK = _hamiltonian->dK(momentum, metric);

    for (size_t i = 0; i < dK.size(); ++i)
    {
      position[i] += stepSize * dK[i];
    }

    _hamiltonian->updateHamiltonian(position, metric, inverseMetric);
    dU = _hamiltonian->dU();

    for (size_t i = 0; i < dU.size(); ++i)
    {
      momentum[i] -= 0.5 * stepSize * dU[i];
    }
  }
};

} // namespace sampler
} // namespace solver
} // namespace korali

#endif
