#include "fAdam.hpp"
#include <cmath>
#include <stdio.h>
#include <cstdlib>

namespace korali
{
fAdam::fAdam(size_t nVars)
{
  // Variable Parameters
  _currentGeneration = 1;
  _nVars = nVars;
  _initialValues.resize(_nVars, 0.0);
  _currentValue.resize(_nVars, 0.0);
  _gradient.resize(_nVars, 0.0);
  _squaredGradient.resize(_nVars, 0.0);
  _firstMoment.resize(_nVars, 0.0);
  _biasCorrectedFirstMoment.resize(_nVars, 0.0);
  _secondMoment.resize(_nVars, 0.0);
  _biasCorrectedSecondMoment.resize(_nVars, 0.0);

  // Defaults
  _beta1 = 0.9f;
  _beta2 = 0.999f;
  _eta = 0.001;
  _epsilon = 1e-08f;
  _modelEvaluationCount = 0;

  // Termination Criteria
  _maxGenerations = 10000000;
  _minGradientNorm = 1e-16f;
  _maxGradientNorm = 1e+16f;

  reset();
}

void fAdam::reset()
{
  _currentGeneration = 1;
  _modelEvaluationCount = 0;

  for (size_t i = 0; i < _nVars; i++)
    if (std::isfinite(_initialValues[i]) == false)
    {
      fprintf(stderr, "Initial Value of variable \'%lu\' not defined (no defaults can be calculated).\n", i);
      std::abort();
    }

  for (size_t i = 0; i < _nVars; i++)
    _currentValue[i] = _initialValues[i];

  for (size_t i = 0; i < _nVars; i++)
  {
    _firstMoment[i] = 0.0f;
    _biasCorrectedFirstMoment[i] = 0.0f;
    _secondMoment[i] = 0.0f;
    _biasCorrectedSecondMoment[i] = 0.0f;
  }

  _bestEvaluation = +std::numeric_limits<float>::infinity();
  _gradientNorm = 1.0f;
}

void fAdam::processResult(float evaluation, std::vector<float> &gradient)
{
  _modelEvaluationCount++;
  _currentEvaluation = evaluation;

  _currentEvaluation = -_currentEvaluation; //minimize
  _gradientNorm = 0.0f;

  _gradient = gradient;

  if (_gradient.size() != _nVars)
  {
    fprintf(stderr, "Size of sample's gradient evaluations vector (%lu) is different from the number of problem variables defined (%lu).\n", _gradient.size(), _nVars);
    std::abort();
  }

  for (size_t i = 0; i < _nVars; i++)
  {
    _gradient[i] = -_gradient[i]; // minimize
    _squaredGradient[i] = _gradient[i] * _gradient[i];
    _gradientNorm += _squaredGradient[i];
  }
  _gradientNorm = sqrtf(_gradientNorm);

  if (_currentEvaluation < _bestEvaluation)
    _bestEvaluation = _currentEvaluation;

  // update first and second moment estimators and bias corrected versions
  for (size_t i = 0; i < _nVars; i++)
  {
    _firstMoment[i] = _beta1 * _firstMoment[i] + (1.0f - _beta1) * _gradient[i];
    _biasCorrectedFirstMoment[i] = _firstMoment[i] / (1.0f - std::pow(_beta1, _modelEvaluationCount));
    _secondMoment[i] = _beta2 * _secondMoment[i] + (1.0f - _beta2) * _squaredGradient[i];
    _biasCorrectedSecondMoment[i] = _secondMoment[i] / (1.0f - std::pow(_beta2, _modelEvaluationCount));
  }

  // update parameters
  for (size_t i = 0; i < _nVars; i++)
  {
    _currentValue[i] -= _eta / (std::sqrt(_biasCorrectedSecondMoment[i]) + _epsilon) * _biasCorrectedFirstMoment[i];
  }
}

bool fAdam::checkTermination()
{
  if ((_currentGeneration > 1) && (_gradientNorm <= _minGradientNorm)) return true;
  if ((_currentGeneration > 1) && (_gradientNorm >= _maxGradientNorm)) return true;
  if (_currentGeneration >= _maxGenerations) return true;

  return false;
}

void fAdam::printInfo()
{
  printf("x = [ ");
  for (size_t k = 0; k < _nVars; k++) printf(" %.5le  ", _currentValue[k]);
  printf(" ]\n");

  printf("F(X) = %le \n", _currentEvaluation);

  printf("DF(X) = [ ");
  for (size_t k = 0; k < _nVars; k++) printf(" %.5le  ", _gradient[k]);
  printf(" ]\n");

  printf("|DF(X)| = %le \n", _gradientNorm);
}

} // namespace korali
