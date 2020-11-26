/** \file
* @brief Auxiliary library for Korali's essential math and time manipulation operations.
**************************************************************************************/

#ifndef _KORALI_AUXILIARS_KORALIMATH_HPP_
#define _KORALI_AUXILIARS_KORALIMATH_HPP_

#define _USE_MATH_DEFINES
#include <cmath>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_sf_gamma.h>
#include <limits>
#include <stdlib.h>
#include <string>
#include <vector>

namespace korali
{
/************************************************
 * CRC Calculation Definitions
 ************************************************/
/**
* @brief Special type for CRC calculation
*/
typedef uint8_t crc;

/**
* @brief Polynomial for CRC calculation
*/
#define POLYNOMIAL 0xD8 /* 11011 followed by 0's */

/**
* @brief Width of CRC calculation
*/
#define WIDTH (8 * sizeof(crc))

/**
* @brief Most significant bit of a CRC calculation
*/
#define TOPBIT (1 << (WIDTH - 1))

/**
* @brief Returns the sign of a given signed item
* @param val The input signed item.
* @return -1, if val is negative; +1, if val is positive; 0, if neither.
*/
template <typename T>
double sign(T val)
{
  return (T(0) < val) - (val < T(0));
}

/**
* @brief Korali's definition of a non-number
*/
const double NaN = std::numeric_limits<double>::quiet_NaN();

/**
* @brief Korali's definition of Infinity
*/
const double Inf = std::numeric_limits<double>::infinity();

/**
* @brief Korali's definition of lowest representable double
*/
const double Lowest = std::numeric_limits<double>::lowest();

/**
* @brief Korali's definition of maximum representable double
*/
const double Max = std::numeric_limits<double>::max();

/**
* @brief Korali's definition of minimum representable double
*/
const double Min = std::numeric_limits<double>::min();

/**
* @brief Korali's definition of minimum representable difference between two numbers
*/
const double Eps = std::numeric_limits<double>::epsilon();

/**
* @brief Computes: log sum_{i=1}^N x_i using the log-sum-exp trick: https://en.wikipedia.org/wiki/LogSumExp#log-sum-exp_trick_for_log-domain_calculations
* @param logValues vector of log(x_i) values
* @param n size of the vector
* @return The LSE function of the input.
*/
template <typename T>
T logSumExp(const T* logValues, const size_t& n)
{
  T maxLogValue = -Inf;
  for (size_t i = 0; i < n; i++)
   if (logValues[i] > maxLogValue)
    maxLogValue = logValues[i];

  if (std::isinf(maxLogValue) == true)
  {
    if (maxLogValue < 0)
      return -Inf;
    else
      return Inf;
  }

  T sumExpValues = 0.0;
  for (size_t i = 0; i < n; i++)
   sumExpValues += exp(logValues[i] - maxLogValue);

  return maxLogValue + log(sumExpValues);
}

/**
* @brief Computes: log sum_{i=1}^N x_i using the log-sum-exp trick: https://en.wikipedia.org/wiki/LogSumExp#log-sum-exp_trick_for_log-domain_calculations
* @param logValues vector of log(x_i) values
* @return The LSE function of the input.
*/
template <typename T>
T logSumExp(const std::vector<T>& logValues)
{
 return logSumExp(logValues.data(), logValues.size());
}

/**
* @brief Computes the L2 norm of a vector.
* @param x vector of xi values
* @return The L2 norm of the vector.
*/
double vectorNorm(const std::vector<double> &x);

/**
* @brief Computes the dot product between two vectors.
* @param x vector of xi values
* @param y vector of yi values
* @return The x . y product
*/
template <typename T>
T dotProduct(const std::vector<T> &x, const std::vector<T> &y)
{
  T dotProd = 0.0;

  for (size_t i = 0; i < x.size(); i++) dotProd += x[i] * y[i];

  return dotProd;
}

/**
* @brief Computes the log density of a normal distribution.
* @param x denisty evaluation point
* @param mean Mean of normal distribution
* @param sigma Standard Deviation of normal distribution
* @return The log density
*/
template <typename T>
T normalLogDensity(const T &x, const T &mean, const T &sigma)
{
  T norm = -0.5 * log(2 * M_PI * sigma * sigma);
  T d = (x - mean) / sigma;
  return norm - 0.5 * d * d;
}

/**
* @brief Computes the log density of the beta distribution.
* @param x denisty evaluation point
* @param mean Mean of Beta distribution
* @param sigma Standard Deviation of Beta distribution
* @return The log density
*/
template <typename T>
T betaLogDensity(const T &x, const T &mean, const T &sigma)
{
  T mu2 = mean * mean;
  T var = sigma * sigma;
  T alpha = -mean * (var + mu2 - mean) / var;
  T beta = (var + mu2 - mean * (mean - 1.0)) / sigma;

  return gsl_sf_lngamma(alpha + beta) - gsl_sf_lngamma(alpha) - gsl_sf_lngamma(beta);
}

/**
* @brief Computes the norm of the difference between two vectors.
* @param x vector of xi values
* @param y vector of yi values
* @return The L2 norm of the distance of vectors x and y.
*/
double vectorDistance(const std::vector<double> &x, const std::vector<double> &y);

/**
* @brief Checks whether at least one of the elements in the vector is not a number.
* @param x vector of xi values
* @return True, if found at least one NaN: false, otherwise.
*/
bool isanynan(const std::vector<double> &x);

/**
* @brief Obtains the timestamp containing the current data and time.
* @return String containing the timestamp.
*/
std::string getTimestamp();

/**
* @brief Obtains the hash function of timestamp containing the current data and time, for seed initialization purposes.
* @return Unsigned integer containing the hashed timestamp.
*/
size_t getTimehash();

/**
* @brief Initializes the CRC function
*/
void crcInit(void);

/**
* @brief Calculates CRC value of the given byte array.
* @param message Pointer to the start of the byte array
* @param nBytes Size of the byte array
* @return CRC value of the message
*/
crc crcFast(uint8_t const message[], size_t nBytes);

/**
* @brief Converts a decimal byte to its hexadecimal equivalent.
* @param byte single byte containing a number from 0 to 15
* @return The hexadecimal letter/number for the value
*/
char decimalToHexChar(const uint8_t byte);

/**
* @brief Converts a hexadecimal letter/number to integer
* @param x the letter/number to convert
* @return A byte with the corresponding integer from 0 to 15
*/
uint8_t hexCharToDecimal(const char x);

/**
* @brief Converts a hexadecimal string pair to integer
* @param src the source hexadecimal string format 0xFF to convert
* @return A byte with the corresponding integer from 0 to 255
*/
uint8_t hexPairToByte(const char *src);

/**
* @brief Converts an integer to its equivalent hexadecimal string
* @param dst pointer to string to save the hex string with format 0xFF.
* @param byte integer containing values from 0 to 255.
*/
void byteToHexPair(char *dst, const uint8_t byte);

/**
* @brief Checksum function that takes an array of bytes and calculates its CRC given a specific initialization seed.
* @param buffer pointer to the start of the byte array.
* @param len size of the buffer.
* @param seed initialization seed for the CRC calculation
* @return The checksum (CRC) of the buffer.
*/
size_t checksum(void *buffer, size_t len, unsigned int seed);
} // namespace korali

#endif // _KORALI_AUXILIARS_KORALIMATH_HPP_
