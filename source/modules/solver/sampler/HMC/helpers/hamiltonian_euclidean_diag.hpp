#ifndef HAMILTONIAN_EUCLIDEAN_DIAG_H
#define HAMILTONIAN_EUCLIDEAN_DIAG_H

#include "hamiltonian_euclidean_base.hpp"
#include "modules/distribution/univariate/normal/normal.hpp"

namespace korali
{
namespace solver
{
namespace sampler
{
/**
* \class HamiltonianEuclideanDiag
* @brief Used for calculating energies with unit euclidean metric.
*/
class HamiltonianEuclideanDiag : public HamiltonianEuclidean
{
  public:
  /**
  * @brief Constructor with State Space Dim.
  * @param stateSpaceDim Dimension of State Space.
  * @param k Pointer to Korali object.
  */
  HamiltonianEuclideanDiag(const size_t stateSpaceDim, korali::Experiment *k) : HamiltonianEuclidean{stateSpaceDim, k}
  {
  }

  /**
  * @brief Constructor with State Space Dim.
  * @param stateSpaceDim Dimension of State Space.
  * @param normalGenerator Generator needed for momentum sampling.
  * @param k Pointer to Korali object.
  */
  HamiltonianEuclideanDiag(const size_t stateSpaceDim, korali::distribution::univariate::Normal *normalGenerator, korali::Experiment *k) : HamiltonianEuclidean{stateSpaceDim, k}
  {
    _normalGenerator = normalGenerator;
  }

  /**
  * @brief Destructor of derived class.
  */
  ~HamiltonianEuclideanDiag() = default;

  /**
  * @brief Total energy function used for Hamiltonian Dynamics.
  * @param momentum Current momentum.
  * @param inverseMetric Inverse of current metric.
  * @return Total energy.
  */
  double H(const std::vector<double> &momentum, const std::vector<double> &inverseMetric) override
  {
    return K(momentum, inverseMetric) + U();
  }

  /**
  * @brief Kinetic energy function.
  * @param momentum Current momentum.
  * @param inverseMetric Inverse of current metric.
  * @return Kinetic energy.
  */
  double K(const std::vector<double> &momentum, const std::vector<double> &inverseMetric) override
  {
    double energy = 0.0;
    for (size_t i = 0; i < _stateSpaceDim; ++i)
    {
      energy += momentum[i] * inverseMetric[i] * momentum[i];
    }

    return 0.5 * energy;
  }

  /**
  * @brief Gradient of kintetic energy function 
  * @param momentum Current momentum.
  * @param inverseMetric Current inverseMetric.
  * @return Gradient of kinetic energy wrt. current momentum.
  */
  std::vector<double> dK(const std::vector<double> &momentum, const std::vector<double> &inverseMetric) override
  {
    std::vector<double> gradient(_stateSpaceDim, 0.0);
    for (size_t i = 0; i < _stateSpaceDim; ++i)
    {
      gradient[i] = inverseMetric[i] * momentum[i];
    }
    return gradient;
  }

  /**
  * @brief Generates sample of momentum.
  * @param metric Current metric.
  * @return Momentum sampled from normal distribution with metric as covariance matrix.
  */
  std::vector<double> sampleMomentum(const std::vector<double> &metric) const override
  {
    std::vector<double> result(_stateSpaceDim);

    for (size_t i = 0; i < _stateSpaceDim; ++i)
    {
      result[i] = std::sqrt(metric[i]) * _normalGenerator->getRandomNumber();
    }

    return result;
  }

  /**
  * @brief Calculates inner product induces by inverse metric.
  * @param leftMomentum Left vector of inner product.
  * @param rightMomentum Right vector of inner product.
  * @param inverseMetric Inverse of current metric.
  * @return inner product
  */
  double innerProduct(const std::vector<double> &leftMomentum, const std::vector<double> &rightMomentum, const std::vector<double> &inverseMetric) const override
  {
    double result = 0.0;

    for (size_t i = 0; i < _stateSpaceDim; ++i)
    {
      result += leftMomentum[i] * inverseMetric[i] * rightMomentum[i];
    }

    return result;
  }

  /**
  * @brief Updates inverse Metric by approximating the covariance matrix with the Fisher information.
  * @param samples Vector of samples. 
  * @param metric Current metric. 
  * @param inverseMetric Inverse of current metric. 
  * @return Error code of Cholesky decomposition.
  */
  int updateMetricMatricesEuclidean(const std::vector<std::vector<double>> &samples, std::vector<double> &metric, std::vector<double> &inverseMetric)
  {
    double mean, cov, sum;
    double sumOfSquares;
    double numSamples = samples.size();

    // calculate sample covariance
    for (size_t i = 0; i < _stateSpaceDim; ++i)
    {
      sum = 0.0;
      sumOfSquares = 0.0;
      for (size_t j = 0; j < numSamples; ++j)
      {
        sum += samples[j][i];
        sumOfSquares += samples[j][i] * samples[j][i];
      }
      mean = sum / (numSamples);
      cov = sumOfSquares / (numSamples)-mean * mean;
      inverseMetric[i] = cov;
      metric[i] = 1.0 / cov;
    }

    return 0;
  }

  private:
  /**
  * @brief One dimensional normal generator needed for sampling of momentum from diagonal _metric.
  */
  korali::distribution::univariate::Normal *_normalGenerator;
};

} // namespace sampler
} // namespace solver
} // namespace korali

#endif
