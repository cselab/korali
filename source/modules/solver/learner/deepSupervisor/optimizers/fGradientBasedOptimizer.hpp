/**************************************************************
 * A single-precision fast version of GRADIENT_BASED_OPTIMIZER for Learning
 **************************************************************/

#ifndef _KORALI_FAST_GRADIENT_BASED_OPTIMIZER_HPP_
#define _KORALI_FAST_GRADIENT_BASED_OPTIMIZER_HPP_

#include <vector>

namespace korali
{
/**
* @brief Class declaration for module: GRADIENT_BASED_OPTIMIZER.
*/
class fGradientBasedOptimizer
{
  public:
  /**
 * @brief Default constructor for the optimizer
 * @param nVars Variable-space dimensionality
 */
  fGradientBasedOptimizer(size_t nVars)
  {
    // Variable Parameters
    _currentGeneration = 1;
    _nVars = nVars;
    _initialValues.resize(_nVars, 0.0);
    _currentValue.resize(_nVars, 0.0);
    _gradient.resize(_nVars, 0.0);
    _modelEvaluationCount = 0;
  }

  /**
  * @brief Default destructor to avoid warnings
  */
  virtual ~fGradientBasedOptimizer() = default;

  /**
  * @brief Number of problem variables
  */
  size_t _nVars;

  /**
  * @brief Learning Rate
  */
  float _eta;

  /**
  * @brief Decay for gradient update
  */
  float _decay;

  /**
   * @brief Counter for the current generation
   */
  size_t _currentGeneration;

  /**
   * @brief Initial values for the variables
   */
  std::vector<float> _initialValues;

  /**
   * @brief Indicates how many generations to run
   */
  size_t _maxGenerations;

  /**
  * @brief Keeps track of how many model evaluations performed
  */
  size_t _modelEvaluationCount;

  /**
* @brief [Internal Use] Current value of parameters.
*/
  std::vector<float> _currentValue;
  /**
* @brief [Internal Use] Function evaluation for the current parameters.
*/
  float _currentEvaluation;
  /**
* @brief [Internal Use] Smaller function evaluation
*/
  float _bestEvaluation;
  /**
* @brief [Internal Use] Gradient of Function with respect to Parameters.
*/
  std::vector<float> _gradient;

  /**
   * @brief Determines whether the module can trigger termination of an experiment run.
   * @return True, if it should trigger termination; false, otherwise.
   */
  virtual bool checkTermination() = 0;

  /**
  * @brief Takes a sample evaluation and its gradient and calculates the next set of parameters
  * @param evaluation The value of the objective function at the current set of parameters
  * @param gradient The gradient of the objective function at the current set of parameters
  */
  virtual void processResult(float evaluation, std::vector<float> &gradient) = 0;

  /**
  * @brief Restores the optimizer to the initial state
  */
  virtual void reset() = 0;

  /**
   * @brief Prints progress information
   */
  virtual void printInfo() = 0;
};

} // namespace korali

#endif // _KORALI_FAST_GRADIENT_BASED_OPTIMIZER_HPP_
