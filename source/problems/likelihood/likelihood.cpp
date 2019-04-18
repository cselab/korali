#include "korali.h"

/************************************************************************/
/*                  Constructor / Destructor Methods                    */
/************************************************************************/

Korali::Problem::Likelihood::Likelihood(nlohmann::json& js) : Korali::Problem::Base::Base(js)
{
 setConfiguration(js);
}

Korali::Problem::Likelihood::~Likelihood()
{

}

/************************************************************************/
/*                    Configuration Methods                             */
/************************************************************************/

nlohmann::json Korali::Problem::Likelihood::getConfiguration()
{
 auto js = this->Korali::Problem::Base::getConfiguration();

 js["Objective"] = "Likelihood";

 for (size_t i = 0; i < _referenceDataSize; i++) js["Reference Data"][i] = _referenceData[i];

 return js;
}

void Korali::Problem::Likelihood::setConfiguration(nlohmann::json& js)
{
 auto ref = consume(js, { "Reference Data" }, KORALI_ARRAY);
 _referenceDataSize = ref.size();
 _referenceData = (double*) calloc (_referenceDataSize, sizeof(double));
 for (size_t i = 0; i < _referenceDataSize; i++) _referenceData[i] = ref[i];

 if (_referenceDataSize == 0)
 {
  fprintf(stderr, "[Korali] Error: No Reference Data set for Likelihood.\n");
  exit(-1);
 }
}

/************************************************************************/
/*                    Functional Methods                                */
/************************************************************************/

double Korali::Problem::Likelihood::evaluateFitness(double* sample)
{

 if (_k->_statisticalParameterCount != 1)
 {
  fprintf(stderr, "[Korali] Error: Likelihood problem requires 1 statistical parameter.\n");
  exit(-1);
 }

 if (_model != KORALI_MULTIPLE)
 {
  fprintf(stderr, "[Korali] Error: Incorrect model for the Likelihood problem.\n");
  exit(-1);
 }

 if (isSampleOutsideBounds(sample)) return -DBL_MAX;

 double sigma = sample[_k->_computationalParameterCount];
 double fitnessData[_referenceDataSize];

 std::vector<double> vec;
 for (size_t i = 0; i < _k->N; i++) vec.push_back(sample[i]);

 std::vector<double> vec2;
 for (size_t i = 0; i < _referenceDataSize; i++) vec2.push_back(0);

 _k->_modelMultiple(vec, vec2);

 for (size_t i = 0; i < _referenceDataSize; i++) fitnessData[i] = vec2[i];

 return -Korali::Parameter::Gaussian::logLikelihood(sigma, _referenceDataSize, _referenceData, fitnessData);
}

