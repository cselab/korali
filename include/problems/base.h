#ifndef _KORALI_BASEPROBLEM_H_
#define _KORALI_BASEPROBLEM_H_

#include "json.hpp"

namespace Korali::Problem
{

class Base
{
 public:

 Base();
 virtual double evaluateFitness(double* sample) = 0;
 virtual void initialize();

 // Serialization Methods
 virtual nlohmann::json getConfiguration();
 virtual void setConfiguration(nlohmann::json js);
};

} // namespace Korali


#endif // _KORALI_BASEPROBLEM_H_
