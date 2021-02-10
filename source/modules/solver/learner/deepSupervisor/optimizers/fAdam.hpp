/**************************************************************
 * A single-precision fast version of Adam for Learning
 **************************************************************/

#ifndef _KORALI_FAST_ADAM_HPP_
#define _KORALI_FAST_ADAM_HPP_

#include <vector>

namespace korali
{
/**
* @brief Class declaration for module: Adam.
*/
class fAdam
{
  public:
  /**
 * @brief Default constructor for the optimizer
 * @param nVars Variable-space dimensionality
 */
  fAdam(size_t nVars);

  /**
  * @brief Number of problem variables
  */
  size_t _nVars;

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
* @brief Beta for momentum update
*/
  float _beta1;
  /**
* @brief Beta for gradient update
*/
  float _beta2;
  /**
* @brief Learning Rate
*/
  float _eta;
  /**
* @brief Smoothing Term
*/
  float _epsilon;
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
* @brief [Internal Use] Square of gradient of function with respect to Parameters.
*/
  std::vector<float> _squaredGradient;
  /**
* @brief [Internal Use] Estimate of first moment of Gradient.
*/
  std::vector<float> _firstMoment;
  /**
* @brief [Internal Use] Bias corrected estimate of first moment of Gradient.
*/
  std::vector<float> _biasCorrectedFirstMoment;
  /**
* @brief [Internal Use] Old estimate of second moment of Gradient.
*/
  std::vector<float> _secondMoment;
  /**
* @brief [Internal Use] Bias corrected estimate of second moment of Gradient.
*/
  std::vector<float> _biasCorrectedSecondMoment;
  /**
* @brief [Termination Criteria] Specifies the minimal norm for the gradient of function with respect to Parameters.
*/
  float _minGradientNorm;
  /**
* @brief [Termination Criteria] Specifies the minimal norm for the gradient of function with respect to Parameters.
*/
  float _maxGradientNorm;

  /**
   * @brief Determines whether the module can trigger termination of an experiment run.
   * @return True, if it should trigger termination; false, otherwise.
   */
  virtual bool checkTermination();

  /**
  * @brief Takes a sample evaluation and its gradient and calculates the next set of parameters
  * @param evaluation The value of the objective function at the current set of parameters
  * @param gradient The gradient of the objective function at the current set of parameters
  */
  virtual void processResult(float evaluation, std::vector<float> &gradient);

  /**
  * @brief Restores the optimizer to the initial state
  */
  virtual void reset();

  /**
   * @brief Prints progress information
   */
  virtual void printInfo();
};

} // namespace korali

#endif // _KORALI_FAST_ADAM_HPP_
