#ifndef HAMILTONIAN_RIEMANNIAN_CONST_DIAG_H
#define HAMILTONIAN_RIEMANNIAN_CONST_DIAG_H

#include "hamiltonian_riemannian_base.hpp"
#include "modules/distribution/univariate/normal/normal.hpp"

namespace korali
{
namespace solver
{
namespace sampler
{
/**
* \class HamiltonianRiemannianConstDiag
* @brief Used for diagonal Riemannian metric.
*/
class HamiltonianRiemannianConstDiag : public HamiltonianRiemannian
{
  public:
  /**
  * @brief Constructor with State Space Dim.
  * @param stateSpaceDim Dimension of State Space.
  * @param normalGenerator Generator needed for momentum sampling.
  * @param inverseRegularizationParam Inverse regularization parameter of SoftAbs metric that controls hardness of approximation: For large values inverseMetric is closer to analytical formula (and therefore closer to degeneracy in certain cases). 
  * @param k Pointer to Korali object.
  */
  HamiltonianRiemannianConstDiag(const size_t stateSpaceDim, korali::distribution::univariate::Normal *normalGenerator, const double inverseRegularizationParam, korali::Experiment *k) : HamiltonianRiemannian{stateSpaceDim, k}
  {
    _normalGenerator = normalGenerator;
    _inverseRegularizationParam = inverseRegularizationParam;
  }

  /**
  * @brief Destructor of derived class.
  */
  ~HamiltonianRiemannianConstDiag() = default;

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
    double result = tau(momentum, inverseMetric) + 0.5 * _logDetMetric;

    return result;
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
  * @brief Calculates tau(q, p) = 0.5 * momentum^T * inverseMetric(q) * momentum.
  * @param momentum Current momentum.
  * @param inverseMetric Current inverseMetric.
  * @return Gradient of Kinetic energy with current momentum.
  */
  double tau(const std::vector<double> &momentum, const std::vector<double> &inverseMetric) override
  {
    double energy = 0.0;

    for (size_t i = 0; i < _stateSpaceDim; ++i)
    {
      energy += momentum[i] * inverseMetric[i] * momentum[i];
    }

    return 0.5 * energy;
  }

  /**
  * @brief Calculates gradient of tau(q, p) wrt. position.
  * @param momentum Current momentum.
  * @param inverseMetric Current inverseMetric.
  * @return Gradient of Kinetic energy with current momentum.
  */
  std::vector<double> dtau_dq(const std::vector<double> &momentum, const std::vector<double> &inverseMetric) override
  {
    std::vector<double> result(_stateSpaceDim, 0.0);

    return result;
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
    return U() + 0.5 * _logDetMetric;
  }

  /**
  * @brief Calculates gradient of kinetic energy.
  * @return Gradient of kinetic energy.
  */
  std::vector<double> dphi_dq() override
  {
    return dU();
  }

  /**
  * @brief Updates current position of hamiltonian.
  * @param position Current position.
  * @param metric Current metric.
  * @param inverseMetric Inverse of current metric.
  */
  void updateHamiltonian(const std::vector<double> &position, std::vector<double> &metric, std::vector<double> &inverseMetric) override
  {
    auto sample = korali::Sample();
    sample["Sample Id"] = _modelEvaluationCount;
    sample["Module"] = "Problem";
    sample["Operation"] = "Evaluate";
    sample["Parameters"] = position;

    KORALI_START(sample);
    KORALI_WAIT(sample);
    _modelEvaluationCount++;
    _currentEvaluation = KORALI_GET(double, sample, "logP(x)");

    if (samplingProblemPtr != nullptr)
    {
      samplingProblemPtr->evaluateGradient(sample);
      samplingProblemPtr->evaluateHessian(sample);
    }
    else
    {
      bayesianProblemPtr->evaluateGradient(sample);
      bayesianProblemPtr->evaluateHessian(sample);
    }

    _currentGradient = sample["grad(logP(x))"].get<std::vector<double>>();
    _currentHessian = sample["H(logP(x))"].get<std::vector<double>>();
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
  * @param momentumLeft Left vector of inner product.
  * @param momentumRight Right vector of inner product.
  * @param inverseMetric Inverse of curret metric.
  * @return inner product
  */
  double innerProduct(const std::vector<double> &momentumLeft, const std::vector<double> &momentumRight, const std::vector<double> &inverseMetric) const override
  {
    double result = 0.0;

    for (size_t i = 0; i < _stateSpaceDim; ++i)
    {
      result += momentumLeft[i] * inverseMetric[i] * momentumRight[i];
    }

    return result;
  }

  /**
  * @brief Updates Metric and Inverse Metric by using hessian.
  * @param metric Current metric.
  * @param inverseMetric Inverse of current metric.
  * @return Error code to indicate if update was successful.
  */
  int updateMetricMatricesRiemannian(std::vector<double> &metric, std::vector<double> &inverseMetric) override
  {
    auto hessian = _currentHessian;

    // constant for condition number of metric
    double detMetric = 1.0;

    for (size_t i = 0; i < _stateSpaceDim; ++i)
    {
      metric[i] = softAbsFunc(hessian[i + i * _stateSpaceDim], _inverseRegularizationParam);
      inverseMetric[i] = 1.0 / metric[i];
      detMetric *= metric[i];
    }
    _logDetMetric = std::log(detMetric);

    return 0;
  }

  /**
  * @brief Inverse regularization parameter of SoftAbs metric that controls hardness of approximation
  */
  double _inverseRegularizationParam;

  private:
  /**
  * @brief One dimensional normal generator needed for sampling of momentum from diagonal metric.
  */
  korali::distribution::univariate::Normal *_normalGenerator;
};

} // namespace sampler
} // namespace solver
} // namespace korali

#endif
