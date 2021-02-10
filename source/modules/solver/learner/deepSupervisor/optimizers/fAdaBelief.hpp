/**************************************************************
 * A single-precision fast version of AdaBelief for Learning
 **************************************************************/

#ifndef _KORALI_FAST_ADABELIEF_HPP_
#define _KORALI_FAST_ADABELIEF_HPP_

#include "fAdam.hpp"

namespace korali
{
/**
* @brief Class declaration for module: AdaBelief.
*/
class fAdaBelief : public fAdam
{
  public:
  /**
 * @brief Default constructor for the optimizer
 * @param nVars Variable-space dimensionality
 */
  fAdaBelief(size_t nVars);

  /**
 * @brief [Internal Use] Old estimate of second moment of Gradient.
 */
  std::vector<float> _secondCentralMoment;

  void processResult(float evaluation, std::vector<float> &gradient) override;
  void reset() override;
};

} // namespace korali

#endif // _KORALI_FAST_ADABELIEF_HPP_
