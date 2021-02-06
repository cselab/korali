#include "fAdaBelief.hpp"
#include <cmath>
#include <stdio.h>
#include <cstdlib>

namespace korali
{
fAdaBelief::fAdaBelief(size_t nVars) : fAdam(nVars)
{
  _secondCentralMoment.resize(nVars);
  _biasCorrectedSecondCentralMoment.resize(nVars);

  reset();
}

void fAdaBelief::reset()
{
  fAdam::reset();

  for (size_t i = 0; i < _nVars; i++)
  {
    _secondCentralMoment[i] = 0.0f;
    _biasCorrectedSecondCentralMoment[i] = 0.0f;
  }
}

void fAdaBelief::processResult(float evaluation, std::vector<float> &gradient)
{
  _modelEvaluationCount++;
  _currentEvaluation = evaluation;

  _currentEvaluation = -_currentEvaluation; //minimize
  _gradientNorm = 0.0;

  _gradient = gradient;

  if (_gradient.size() != _nVars)
  {
    fprintf(stderr, "Size of sample's gradient evaluations vector (%lu) is different from the number of problem variables defined (%lu).\n", _gradient.size(), _nVars);
    std::abort();
  }

  for (size_t i = 0; i < _nVars; i++)
  {
    _gradient[i] = -_gradient[i]; // minimize
    _gradientNorm += _gradient[i] * _gradient[i];
  }
  _gradientNorm = std::sqrt(_gradientNorm);

  if (_currentEvaluation < _bestEvaluation)
    _bestEvaluation = _currentEvaluation;

  // update first and second moment estimators and bias corrected versions
  for (size_t i = 0; i < _nVars; i++)
  {
    _firstMoment[i] = _beta1 * _firstMoment[i] + (1 - _beta1) * _gradient[i];
    _biasCorrectedFirstMoment[i] = _firstMoment[i] / (1 - std::pow(_beta1, _modelEvaluationCount));
    _secondCentralMoment[i] = _beta2 * _secondCentralMoment[i] + (1 - _beta2) * (_gradient[i] - _firstMoment[i]) * (_gradient[i] - _firstMoment[i]);
    _biasCorrectedSecondCentralMoment[i] = _secondCentralMoment[i] / (1 - std::pow(_beta2, _modelEvaluationCount));
  }

  // update parameters
  for (size_t i = 0; i < _nVars; i++)
    _currentValue[i] -= _eta / (std::sqrt(_biasCorrectedSecondCentralMoment[i]) + _epsilon) * _biasCorrectedFirstMoment[i];
}

} // namespace korali
