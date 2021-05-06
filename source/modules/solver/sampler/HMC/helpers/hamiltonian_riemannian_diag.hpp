#ifndef HAMILTONIAN_RIEMANNIAN_DIAG_H
#define HAMILTONIAN_RIEMANNIAN_DIAG_H

#include "hamiltonian_riemannian_base.hpp"
#include "modules/distribution/univariate/normal/normal.hpp"

namespace korali
{
namespace solver
{
namespace sampler
{
/**
* \class HamiltonianRiemannianDiag
* @brief Used for diagonal Riemannian metric.
*/
class HamiltonianRiemannianDiag : public HamiltonianRiemannian
{
  public:
  /**
  * @brief Constructor with State Space Dim.
  * @param stateSpaceDim Dimension of State Space.
  * @param normalGenerator Generator needed for momentum sampling.
  * @param inverseRegularizationParam Inverse regularization parameter of SoftAbs metric that controls hardness of approximation: For large values inverseMetric is closer to analytical formula (and therefore closer to degeneracy in certain cases). 
  * @param k Pointer to Korali object.
  */
  HamiltonianRiemannianDiag(const size_t stateSpaceDim, korali::distribution::univariate::Normal *normalGenerator, const double inverseRegularizationParam, korali::Experiment *k) : HamiltonianRiemannian{stateSpaceDim, k}
  {
    _normalGenerator = normalGenerator;
    _inverseRegularizationParam = inverseRegularizationParam;
  }

  /**
  * @brief Destructor of derived class.
  */
  ~HamiltonianRiemannianDiag() = default;

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
    double tau = 0.0;

    for (size_t i = 0; i < _stateSpaceDim; ++i)
    {
      tau += momentum[i] * inverseMetric[i] * momentum[i];
    }

    return 0.5 * tau;
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
    std::vector<double> gradU = dU();
    std::vector<double> hessian = hessianU();

    for (size_t j = 0; j < _stateSpaceDim; ++j)
    {
      result[j] = 0.0;
      for (size_t i = 0; i < _stateSpaceDim; ++i)
      {
        result[j] += hessian[i * _stateSpaceDim + j] * taylorSeriesTauFunc(gradU[i], _inverseRegularizationParam) * momentum[i] * momentum[i];
      }
    }

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
    std::vector<double> result = dK(momentum, inverseMetric);

    return result;
  }

  /**
  * @brief Purely virtual gradient of phi(q) = 0.5 * logDetMetric(q) + U(q) used for Hamiltonian Dynamics.
  * @return Gradient of Kinetic energy with current momentum.
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
    std::vector<double> result(_stateSpaceDim, 0.0);
    std::vector<double> gradU = dU();
    std::vector<double> hessian = hessianU();

    std::vector<double> dLogDetMetric_dq(_stateSpaceDim, 0.0);

    for (size_t j = 0; j < _stateSpaceDim; ++j)
    {
      dLogDetMetric_dq[j] = 0.0;
      for (size_t i = 0; i < _stateSpaceDim; ++i)
      {
        dLogDetMetric_dq[j] += 2.0 * hessian[i * _stateSpaceDim + j] * taylorSeriesPhiFunc(gradU[i], _inverseRegularizationParam);
      }
    }

    for (size_t j = 0; j < _stateSpaceDim; ++j)
    {
      result[j] = gradU[j] + 0.5 * dLogDetMetric_dq[j];
    }

    return result;
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

    // constant for condition number of metric
    _logDetMetric = 0.0;
    for (size_t i = 0; i < _stateSpaceDim; ++i)
    {
      metric[i] = softAbsFunc(_currentGradient[i] * _currentGradient[i], _inverseRegularizationParam);
      inverseMetric[i] = 1.0 / metric[i];
      _logDetMetric += std::log(metric[i]);
    }

    return;
  }

  /**
  * @brief Generates sample of momentum.
  * @param metric Current metric.
  * @return Sample of momentum from normal distribution with covariance matrix metric. Only variance taken into account with diagonal metric.
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
  * @param inverseMetric Inverse of current metric.
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
  * @brief Inverse regularization parameter of SoftAbs metric that controls hardness of approximation
  */
  double _inverseRegularizationParam;

  private:
  /**
  * @brief Helper function f(x) = 1/x - alpha * x / (sinh(alpha * x^2) * cosh(alpha * x^2)) for SoftAbs metric.
  * @param x Point of evaluation.
  * @param alpha Hyperparameter.
  * @return function value at x.
  */
  double taylorSeriesPhiFunc(const double x, const double alpha)
  {
    double result;

    if (std::abs(x * alpha) < 0.5)
    {
      double a3 = 2.0 / 3.0;
      double a7 = -14.0 / 45.0;
      double a11 = 124.0 / 945.0;

      result = a3 * std::pow(x, 3) * std::pow(alpha, 2) + a7 * std::pow(x, 7) * std::pow(alpha, 4) + a11 * std::pow(x, 11) * std::pow(alpha, 6);
    }
    else
    {
      result = 1.0 / x - alpha * x / (std::sinh(alpha * x * x) * std::cosh(alpha * x * x));
    }

    return result;
  }

  /**
  * @brief Helper function f(x) = 1/x * (alpha / cosh(alha * x^2)^2 - tanh(alpha * x^2) / x^2) for SoftAbs metric.
  * @param x Point of evaluation.
  * @param alpha Hyperparameter.
  * @return function value at x.
  */
  double taylorSeriesTauFunc(const double x, const double alpha)
  {
    double result;

    if (std::abs(x * alpha) < 0.5)
    {
      double a3 = -2.0 / 3.0;
      double a7 = 8.0 / 15.0;
      double a11 = -34.0 / 105.0;

      result = a3 * std::pow(x, 3) * std::pow(alpha, 3) + a7 * std::pow(x, 7) * std::pow(alpha, 5) + a11 * std::pow(x, 11) * std::pow(alpha, 7);
    }
    else
    {
      result = 1.0 / x * (alpha / (std::cosh(alpha * x * x) * std::cosh(alpha * x * x)) - std::tanh(alpha * x * x) / (x * x));
    }

    return result;
  }

  /**
  * @brief One dimensional normal generator needed for sampling of momentum from diagonal metric.
  */
  korali::distribution::univariate::Normal *_normalGenerator;
};

} // namespace sampler
} // namespace solver
} // namespace korali

#endif
