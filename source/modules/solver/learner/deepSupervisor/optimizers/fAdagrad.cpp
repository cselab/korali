#include "fAdagrad.hpp"
#include <cmath>
#include <cstdlib>
#include <stdio.h>

namespace korali
{
fAdagrad::fAdagrad(size_t nVars) : fGradientBasedOptimizer(nVars)
{
  // Defaults
  _eta = 0.001f;
  _epsilon = 1e-08f;

  _s.resize(nVars);
  reset();
}

void fAdagrad::reset()
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
  {
    _currentValue[i] = _initialValues[i];
    _s[i] = 0.0f;
  }

  _bestEvaluation = +std::numeric_limits<float>::infinity();
}

void fAdagrad::processResult(float evaluation, std::vector<float> &gradient)
{
  if (gradient.size() != _nVars)
  {
    fprintf(stderr, "Size of sample's gradient evaluations vector (%lu) is different from the number of problem variables defined (%lu).\n", gradient.size(), _nVars);
    std::abort();
  }

  for (size_t i = 0; i < _nVars; i++)
  {
    _s[i] = _s[i] + (gradient[i] * gradient[i]);
    _currentValue[i] = _currentValue[i] + (_eta / std::sqrt(_s[i] + _epsilon)) * gradient[i];
  }

  _modelEvaluationCount++;
}

bool fAdagrad::checkTermination()
{
  if (_currentGeneration >= _maxGenerations) return true;

  return false;
}

void fAdagrad::printInfo()
{
  printf("x = [ ");
  for (size_t k = 0; k < _nVars; k++) printf(" %.5le  ", _currentValue[k]);
  printf(" ]\n");

  printf("F(X) = %le \n", _currentEvaluation);

  printf("DF(X) = [ ");
  for (size_t k = 0; k < _nVars; k++) printf(" %.5le  ", _gradient[k]);
  printf(" ]\n");
}

} // namespace korali
