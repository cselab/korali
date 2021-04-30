#ifndef HAMILTONIAN_BASE_H
#define HAMILTONIAN_BASE_H

#include "modules/conduit/conduit.hpp"

#include "engine.hpp"
#include "modules/experiment/experiment.hpp"
#include "modules/problem/bayesian/bayesian.hpp"
#include "modules/problem/bayesian/reference/reference.hpp"
#include "modules/problem/problem.hpp"
#include "modules/problem/sampling/sampling.hpp"
#include "sample/sample.hpp"

namespace korali
{
namespace solver
{
namespace sampler
{
/**
* \class Hamiltonian
* @brief Abstract base class for Hamiltonian objects.
*/
class Hamiltonian
{
  public:
  /**
  * @brief Default constructor.
  */
  Hamiltonian() = default;

  /**
  * @brief Constructor with State Space Dim.
  * @param stateSpaceDim Dimension of State Space.
  * @param k Pointer to Korali object.
  */
  Hamiltonian(const size_t stateSpaceDim, korali::Experiment *k) : _modelEvaluationCount(0), _stateSpaceDim{stateSpaceDim}
  {
    _k = k;
    samplingProblemPtr = dynamic_cast<korali::problem::Sampling *>(k->_problem);
    bayesianProblemPtr = dynamic_cast<korali::problem::Bayesian *>(k->_problem);

    if (samplingProblemPtr != nullptr && bayesianProblemPtr != nullptr)
      KORALI_LOG_ERROR("Problem type not compatible with Hamiltonian object. Problem type must be either 'Sampling' or 'Bayesian'.");
  };

  /**
  * @brief Destructor of abstract base class.
  */
  virtual ~Hamiltonian() = default;

  /**
  * @brief Purely abstract total energy function used for Hamiltonian Dynamics.
  * @param momentum Current momentum.
  * @param inverseMetric Current inverse of metric.
  * @return Total energy.
  */
  virtual double H(const std::vector<double> &momentum, const std::vector<double> &inverseMetric) = 0;

  /**
  * @brief Purely virtual kinetic energy function.
  * @param momentum Current momentum.
  * @param inverseMetric Current inverse of metric.
  * @return Kinetic energy.
  */
  virtual double K(const std::vector<double> &momentum, const std::vector<double> &inverseMetric) = 0;

  /**
  * @brief Purely virtual gradient of kintetic energy function.
  * @param momentum Current momentum.
  * @param inverseMetric Current inverse metric.
  * @return Gradient of Kinetic energy with current momentum.
  */
  virtual std::vector<double> dK(const std::vector<double> &momentum, const std::vector<double> &inverseMetric) = 0;

  /**
  * @brief Potential Energy function.
  * @return Potential energy.
  */
  virtual double U()
  {
    return -_currentEvaluation;
  }

  /**
  * @brief Gradient of Potential Energy function.
  * @return Gradient of Potential energy.
  */
  virtual std::vector<double> dU()
  {
    auto grad = _currentGradient;

    // negate to get dU
    std::transform(grad.cbegin(), grad.cend(), grad.begin(), std::negate<double>());

    return grad;
  }

  /**
  * @brief Purely virtual function tau(q, p) = 0.5 * momentum^T * inverseMetric(q) * momentum.
  * @param momentum Current momentum.
  * @param inverseMetric Current inverseMetric.
  * @return Gradient of Kinetic energy with current momentum.
  */
  virtual double tau(const std::vector<double> &momentum, const std::vector<double> &inverseMetric) = 0;

  /**
  * @brief Purely virtual gradient of dtau_dq(q, p) wrt. position.
  * @param momentum Current momentum.
  * @param inverseMetric Current inverseMetric.
  * @return Gradient of Kinetic energy with current momentum.
  */
  virtual std::vector<double> dtau_dq(const std::vector<double> &momentum, const std::vector<double> &inverseMetric) = 0;

  /**
  * @brief Purely virtual gradient of dtau_dp(q, p) wrt. momentum.
  * @param momentum Current momentum.
  * @param inverseMetric Current inverseMetric.
  * @return Gradient of Kinetic energy with current momentum.
  */
  virtual std::vector<double> dtau_dp(const std::vector<double> &momentum, const std::vector<double> &inverseMetric) = 0;

  /**
  * @brief Purely virtual gradient of kinetic energy.
  * @return Gradient of kinetic energy.
  */
  virtual double phi() = 0;

  /**
  * @brief Purely virtual gradient of kinetic energy.
  * @return Gradient of kinetic energy.
  */
  virtual std::vector<double> dphi_dq() = 0;

  /**
  * @brief Purely virtual, calculates inner product induces by inverse metric.
  * @param leftMomentum Left vector of inner product.
  * @param rightMomentum Right vector of inner product.
  * @param inverseMetric Inverse of current metric.
  * @return inner product
  */
  virtual double innerProduct(const std::vector<double> &leftMomentum, const std::vector<double> &rightMomentum, const std::vector<double> &inverseMetric) const = 0;

  /**
  * @brief Updates current position of hamiltonian.
  * @param position Current position.
  * @param metric Current metric.
  * @param inverseMetric Inverse of current metric.
  */
  virtual void updateHamiltonian(const std::vector<double> &position, std::vector<double> &metric, std::vector<double> &inverseMetric)
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
      samplingProblemPtr->evaluateGradient(sample);
    else
      bayesianProblemPtr->evaluateGradient(sample);

    _currentGradient = sample["grad(logP(x))"].get<std::vector<double>>();
  }

  /**
  * @brief Purely virtual function to generates momentum vector.
  * @param metric Current metric.
  * @return Momentum sampled from normal distribution with metric as covariance matrix.
  */
  virtual std::vector<double> sampleMomentum(const std::vector<double> &metric) const = 0;

  /**
  * @brief Computes NUTS criterion on euclidean domain.
  * @param positionLeft Leftmost position.
  * @param momentumLeft Leftmost momentum.
  * @param positionRight Rightmost position.
  * @param momentumRight Rightmost momentum.
  * @return Returns criterion if tree should be further increased.
  */
  bool computeStandardCriterion(const std::vector<double> &positionLeft, const std::vector<double> &momentumLeft, const std::vector<double> &positionRight, const std::vector<double> &momentumRight) const
  {
    std::vector<double> tmpVector(_stateSpaceDim, 0.0);

    std::transform(std::begin(positionRight), std::cend(positionRight), std::cbegin(positionLeft), std::begin(tmpVector), std::minus<double>());
    double dotProductLeft = std::inner_product(std::cbegin(tmpVector), std::cend(tmpVector), std::cbegin(momentumLeft), 0.0);
    double dotProductRight = std::inner_product(std::cbegin(tmpVector), std::cend(tmpVector), std::cbegin(momentumRight), 0.0);

    return (dotProductLeft >= 0) && (dotProductRight >= 0);
  }

  /**
  * @brief Updates Inverse Metric by approximating the covariance matrix with the Fisher information.
  * @param samples Vector of samples. 
  * @param metric Current metric. 
  * @param inverseMetric Inverse of current metric. 
  * @return Error code of Cholesky decomposition.
  */
  virtual int updateMetricMatricesEuclidean(const std::vector<std::vector<double>> &samples, std::vector<double> &metric, std::vector<double> &inverseMetric)
  {
    return -1;
  };

  /**
  * @brief Updates Metric and Inverse Metric by using hessian.
  * @param metric Current metric.
  * @param inverseMetric Inverse of current metric.
  * @return Error code to indicate if update was successful.
  */
  virtual int updateMetricMatricesRiemannian(std::vector<double> &metric, std::vector<double> &inverseMetric)
  {
    return 0;
  };

  /**
  * @brief Number of model evaluations.
  */
  size_t _modelEvaluationCount;

  protected:
  /**
  @brief Pointer to the korali experiment.
  */
  korali::Experiment *_k;

  /**
  @brief Pointer to the sampling problem (might be NULL)
  */
  korali::problem::Sampling *samplingProblemPtr;

  /**
  @brief Pointer to the Bayesian problem (might be NULL)
  */
  korali::problem::Bayesian *bayesianProblemPtr;

  /**
  @brief Current evaluation of objective (return value of sample evaluation).
  */
  double _currentEvaluation;

  /**
  * @brief Current gradient of objective (return value of sample evaluation).
  */
  std::vector<double> _currentGradient;

  /**
  * @brief State Space Dimension needed for Leapfrog integrator.
  */
  size_t _stateSpaceDim;
};

} // namespace sampler
} // namespace solver
} // namespace korali

#endif
