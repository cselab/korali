#ifndef HAMILTONIAN_EUCLIDEAN_DENSE_H
#define HAMILTONIAN_EUCLIDEAN_DENSE_H

#include "hamiltonian_euclidean_base.hpp"
#include "modules/distribution/multivariate/normal/normal.hpp"

#include <gsl/gsl_linalg.h>
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_multimin.h>
#include <gsl/gsl_sort_vector.h>
#include <gsl/gsl_statistics.h>

namespace korali
{
namespace solver
{
namespace sampler
{
/**
* \class HamiltonianEuclideanDense
* @brief Used for calculating energies with euclidean metric.
*/
class HamiltonianEuclideanDense : public HamiltonianEuclidean
{
  public:
  /**
  * @brief Constructor with State Space Dim.
  * @param stateSpaceDim Dimension of State Space.
  * @param metric Metric of space.
  * @param multivariateGenerator Generator needed for momentum sampling.
  * @param k Pointer to Korali object.
  */
  HamiltonianEuclideanDense(const size_t stateSpaceDim, korali::distribution::multivariate::Normal *multivariateGenerator, const std::vector<double> &metric, korali::Experiment *k) : HamiltonianEuclidean{stateSpaceDim, k}
  {
    _multivariateGenerator = multivariateGenerator;
    _multivariateGenerator->_meanVector = std::vector<double>(stateSpaceDim, 0.);
    _multivariateGenerator->_sigma = metric;
    gsl_matrix_view sigView = gsl_matrix_view_array(&_multivariateGenerator->_sigma[0], _stateSpaceDim, _stateSpaceDim);

    // Cholesky Decomp
    int err = gsl_linalg_cholesky_decomp(&sigView.matrix);
    if (err == 0)
    {
      _multivariateGenerator->updateDistribution();
    }
  }

  /**
  * @brief Destructor of derived class.
  */
  ~HamiltonianEuclideanDense() = default;

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
      for (size_t j = 0; j < _stateSpaceDim; ++j)
      {
        energy += momentum[i] * inverseMetric[i * _stateSpaceDim + j] * momentum[j];
      }
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
    double gradi = 0.0;

    for (size_t i = 0; i < _stateSpaceDim; ++i)
    {
      gradi = 0.0;
      for (size_t j = 0; j < _stateSpaceDim; ++j)
      {
        gradi += inverseMetric[i * _stateSpaceDim + j] * momentum[j];
      }
      gradient[i] = gradi;
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
    std::vector<double> result(_stateSpaceDim, 0.0);
    _multivariateGenerator->getRandomVector(&result[0], _stateSpaceDim);
    return result;
  }

  /**
  * @brief Calculates inner product induced by inverse metric.
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
      for (size_t j = 0; j < _stateSpaceDim; ++j)
      {
        result += leftMomentum[i] * inverseMetric[i * _stateSpaceDim + j] * rightMomentum[j];
      }
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
  int updateMetricMatricesEuclidean(const std::vector<std::vector<double>> &samples, std::vector<double> &metric, std::vector<double> &inverseMetric) override
  {
    double sumk, sumi, sumOfSquares;
    double meank, meani, cov;
    double numSamples = samples.size();

    // calculate sample covariance
    for (size_t i = 0; i < _stateSpaceDim; ++i)
    {
      for (size_t k = i; k < _stateSpaceDim; ++k)
      {
        sumk = 0.;
        sumi = 0.;
        sumOfSquares = 0.;
        for (size_t j = 0; j < numSamples; ++j)
        {
          sumi += samples[j][i];
          sumk += samples[j][k];
          sumOfSquares += samples[j][i] * samples[j][k];
        }
        meank = sumk / numSamples;
        meani = sumi / numSamples;
        cov = sumOfSquares / numSamples - meani * meank;
        inverseMetric[i * _stateSpaceDim + k] = cov;
        inverseMetric[k * _stateSpaceDim + i] = cov;
      }
    }

    // update Metric to be consisitent with Inverse Metric
    int err = invertMatrix(inverseMetric, metric);
    if (err > 0) return err;

    std::vector<double> sig = metric;
    gsl_matrix_view sigView = gsl_matrix_view_array(&sig[0], _stateSpaceDim, _stateSpaceDim);

    // Cholesky Decomp
    err = gsl_linalg_cholesky_decomp(&sigView.matrix);
    if (err == 0)
    {
      _multivariateGenerator->_sigma = sig;
      _multivariateGenerator->updateDistribution();
    }

    return err;
  }

  protected:
  // inverts mat via cholesky decomposition and writes inverted Matrix to inverseMat

  /**
  * @brief Inverts s.p.d. matrix via Cholesky decomposition.
  * @param matrix Input matrix interpreted as square symmetric matrix.
  * @param inverseMat Result of inversion.
  * @return Error code of Cholesky decomposition used to invert matrix.
  */
  int invertMatrix(const std::vector<double> &matrix, std::vector<double> &inverseMat)
  {
    const size_t dim = (size_t)std::sqrt(matrix.size());
    gsl_matrix_view invView = gsl_matrix_view_array(&inverseMat[0], dim, dim);
    gsl_matrix_const_view matView = gsl_matrix_const_view_array(&matrix[0], dim, dim);

    gsl_permutation *p = gsl_permutation_alloc(dim);
    int s;

    gsl_matrix *luMat = gsl_matrix_alloc(dim, dim);
    gsl_matrix_memcpy(luMat, &matView.matrix);
    gsl_linalg_LU_decomp(luMat, p, &s);
    int err = gsl_linalg_LU_invert(luMat, p, &invView.matrix);

    // free up memory of gsl matrix
    gsl_permutation_free(p);
    gsl_matrix_free(luMat);

    return err;
  }

  private:
  /**
  * @brief Multivariate normal generator needed for sampling of momentum from dense metric.
  */
  korali::distribution::multivariate::Normal *_multivariateGenerator;
};

} // namespace sampler
} // namespace solver
} // namespace korali

#endif
