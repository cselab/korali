#ifndef LEAPFROG_H
#define LEAPFROG_H

#include "hamiltonian_base.hpp"
#include <iostream>
#include <vector>
namespace korali
{
namespace solver
{
namespace sampler
{
/**
* \class Leapfrog
* @brief Abstract base class used for time propagation according to hamiltonian dynamics via Leapfrog integration schemes.
*/
class Leapfrog
{
  protected:
  /**
  * @brief Pointer to hamiltonian object to calculate energies..
  */
  std::shared_ptr<Hamiltonian> _hamiltonian;

  public:
  /**
  * @brief Abstract base class constructor for explicit or implicit leapfrog stepper.
  * @param hamiltonian Hamiltonian of the system.
  */
  Leapfrog(std::shared_ptr<Hamiltonian> hamiltonian) : _hamiltonian(hamiltonian){};

  /**
   * @brief Default destructor
   */
  virtual ~Leapfrog() = default;

  /**
  * @brief Purely virtual stepping function of the integrator.
  * @param position Position which is evolved.
  * @param momentum Momentum which is evolved.
  * @param metric Current mentric.
  * @param inverseMetric Inverse metric.
  * @param stepSize Step Size used for Leap Frog Scheme.
  */
  virtual void step(std::vector<double> &position, std::vector<double> &momentum, std::vector<double> &metric, std::vector<double> &inverseMetric, const double stepSize) = 0;
};

} // namespace sampler
} // namespace solver
} // namespace korali
#endif
