/**************************************************************
 * A single-precision fast version of Adam for Learning
 **************************************************************/

#ifndef _KORALI_FAST_ADAM_HPP_
#define _KORALI_FAST_ADAM_HPP_

#include "fGradientBasedOptimizer.hpp"
#include <vector>

namespace korali
{
/**
* @brief Class declaration for module: Adam.
*/
class fAdam : public fGradientBasedOptimizer
{
  public:
    virtual ~fAdam(){}
  /**
 * @brief Default constructor for the optimizer
 * @param nVars Variable-space dimensionality
 */
  fAdam(size_t nVars);

  /**
* @brief Beta for momentum update
*/
  float _beta1;
  /**
* @brief Beta for gradient update
*/
  float _beta2;

  /**
* @brief Smoothing Term
*/
  float _epsilon;

  /**
* @brief [Internal Use] Estimate of first moment of Gradient.
*/
  std::vector<float> _firstMoment;
  /**
* @brief [Internal Use] Old estimate of second moment of Gradient.
*/
  std::vector<float> _secondMoment;
  /**
* @brief [Termination Criteria] Specifies the minimal norm for the gradient of function with respect to Parameters.
*/
  float _minGradientNorm;
  /**
* @brief [Termination Criteria] Specifies the minimal norm for the gradient of function with respect to Parameters.
*/
  float _maxGradientNorm;

  virtual bool checkTermination() override;
  virtual void processResult(float evaluation, std::vector<float> &gradient) override;
  virtual void reset() override;
  virtual void printInfo() override;
};

} // namespace korali

#endif // _KORALI_FAST_ADAM_HPP_
