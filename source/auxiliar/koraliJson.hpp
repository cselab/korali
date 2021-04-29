/** \file
* @brief Contains the koraliJson class, which supports JSON objects within Korali classes
******************************************************************************/

#ifndef _KORALI_AUXILIARS_KORALIJSON_HPP_
#define _KORALI_AUXILIARS_KORALIJSON_HPP_

#include "auxiliar/jsonInterface.hpp"
#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>

/**
* \namespace korali
* @brief The Korali namespace includes all Korali-specific functions, variables, and modules.
*/
namespace korali
{
class Sample;

/**
* \class KoraliJson
* @brief This class encapsulates a JSON object, making it compatible with Korali C++ objects and Pybind11
*/
class KoraliJson
{
  public:
  KoraliJson();

  /**
 * @brief Container for the JSON object
 */
  knlohmann::json _js;

  /**
 * @brief Pointer that stores the current access position of the JSON object.
 *  It advances with getItem, and resets upon setJson or finding a native data type (not a path).
 */
  knlohmann::json *_opt;

  /**
  * @brief Function to obtain the JSON object.
  * @return A reference to the JSON object.
  */
  knlohmann::json &getJson();

  /**
   * @brief Function to make a copy of the JSON object
   * @param dst destination js
   */
  void getCopy(knlohmann::json &dst) const;

  /**
  * @brief Function to set the JSON object.
  * @param js The input JSON object.
 */
  void setJson(knlohmann::json &js);

  /**
  * @brief Function to obtain a serialized string of the JSON object.
  * @return A serialized string of the JSON object.
  */
  std::string get();

  /**
  * @brief Function to replace the JSON object by deserializing a JSON string
  * @param js The input serialized JSON object.
 */
  void set(const std::string &js);

  /**
  * @brief Gets an item from the JSON object at the current pointer position.
  * @param key A pybind11 object acting as JSON key (number or string).
  * @return A pybind11 object
 */
  pybind11::object getItem(const pybind11::object key);

  /**
  * @brief Sets an item on the JSON object at the current pointer position.
  * @param key A pybind11 object acting as JSON key (number or string).
  * @param val The value of the item to set.
 */
  void setItem(const pybind11::object key, const pybind11::object val);

  /**
  * @brief C++ wrapper for the getItem operator.
  * @param key A C++ string acting as JSON key.
  * @return The referenced JSON object content.
 */
  knlohmann::json &operator[](const std::string &key);

  /**
  * @brief C++ wrapper for the getItem operator.
  * @param key A C++ integer acting as JSON key.
  * @return The referenced JSON object content.
 */
  knlohmann::json &operator[](const unsigned long int &key);

  /**
  * @brief Indicates whether the JSON object contains the given path.
  * @param key key A C++ string acting as JSON key.
  * @return true, if path is found; false, otherwise.
 */
  bool contains(const std::string &key);

  /**
   * @brief Advances the JSON object pointer, given the key
   * @param key A C++ string acting as JSON key.
  */
  void traverseKey(pybind11::object key);
};

} // namespace korali
#endif // _KORALI_AUXILIARS_KORALIJSON_HPP_
