/** \file
* @brief Contains auxiliar functions for JSON object manipulation
******************************************************************************/

#pragma GCC diagnostic ignored "-Wparentheses"

#ifndef _KORALI_AUXILIARS_JSONINTERFACE_HPP_
#define _KORALI_AUXILIARS_JSONINTERFACE_HPP_

#include "auxiliar/json.hpp"
#include "auxiliar/logger.hpp"
#include <string>

/**
* \namespace korali
* @brief The Korali namespace includes all Korali-specific functions, variables, and modules.
*/
namespace korali
{
/**
  * @brief Checks whether the JSON object is empty.
  * @param js The JSON object to check.
  * @return true, if it's empty; false, otherwise.
 */
bool isEmpty(const knlohmann::json &js);

/**
  * @brief Checks whether the JSON object is of elemental type (number or string).
  * @param js The JSON object to check.
  * @return true, if it's elemental; false, otherwise.
 */
bool isElemental(const knlohmann::json &js);

/**
  * @brief Function made exclusively made to avoid warnings on getting the last element of variadic template arguments
  * @param x is the element to get the pointer from
  * @return The element's pointer
 */
template <typename T>
T *getPointer(T &x)
{
  return &x;
}

/**
  * @brief Deletes a value on a given JS given a string containing the full path
  * @param js The JSON object to modify.
  * @param key a list of keys describing the full path to traverse
 */
template <typename T, typename... Key>
void eraseValue(T &js, const Key &... key)
{
  auto *tmp = &js;
  auto *prv = &js;

  bool result = true;
  decltype(tmp->begin()) it;
  (((result && ((it = tmp->find(key)) == tmp->end()) ? (result = false) : (prv = tmp, tmp = &*it, true))), ...);

  const auto *lastKey = (getPointer(key), ...);

  if (result == true)
    prv->erase(*lastKey);
  else
  {
    std::string keyString(*lastKey);
    KORALI_LOG_ERROR(" + Could not find key '%s' to erase.\n", keyString.c_str());
  }
}

/**
  * @brief Merges the values of two JSON objects recursively and applying priority.
  * @param dest the JSON object onto which the changes will be made. Values here have priority (are not replaced).
  * @param defaults the JSON object that applies onto the other. Values here have no priority (they will not replace)
*/
void mergeJson(knlohmann::json &dest, const knlohmann::json &defaults);

/**
  * @brief Checks whether a given key is present in the JSON object.
  * @param js The JSON object to check.
  * @param key a list of keys describing the full path to traverse
  * @return true, if the path defined by settings is found; false, otherwise.
*/
template <typename T, typename... Key>
bool isDefined(T &js, const Key &... key)
{
  auto *tmp = &js;
  bool result = true;
  decltype(tmp->begin()) it;
  ((result && ((it = tmp->find(key)) == tmp->end() ? (result = false) : (tmp = &*it, true))), ...);
  return result;
}

/**
  * @brief Returns a value on a given object given a string containing the full path
  * @param js The source object to read from.
  * @param key a list of keys describing the full path to traverse
  * @return Object of the requested path
 */
template <typename T, typename... Key>
T getValue(T &js, const Key &... key)
{
  auto *tmp = &js;
  auto *prv = &js;

  bool result = true;
  decltype(tmp->begin()) it;
  (((result && ((it = tmp->find(key)) == tmp->end()) ? (result = false) : (prv = tmp, tmp = &*it, true))), ...);

  const auto *lastKey = (getPointer(key), ...);

  if (result == true)
  {
    return (*prv)[*lastKey];
  }
  else
  {
    std::string keyString(*lastKey);
    KORALI_LOG_ERROR("Could not find key '%s' to return.\n", keyString.c_str());
  }
}

/**
  * @brief Returns a string out of a list of keys showing
  * @param key a list of keys describing the full path to traverse
  * @return The string with a printed key sequence
 */
template <typename... Key>
std::string getPath(const Key &... key)
{
  std::string path;

  ((path += std::string("[\"") + std::string(key) + std::string("\"]")), ...);

  return path;
}

/**
  * @brief Loads a JSON object from a file.
  * @param dst The JSON object to overwrite.
  * @param fileName The path to the json file to load and parse.
  * @return true, if file was found; false, otherwise.
*/
bool loadJsonFromFile(knlohmann::json &dst, const char *fileName);

/**
  * @brief Saves a JSON object to a file.
  * @param fileName The path to the file onto which to save the JSON object.
  * @param js The input JSON object.
  * @return 0 if successful, otherwise if not.
*/
int saveJsonToFile(const char *fileName, const knlohmann::json &js);

} // namespace korali
#endif // _KORALI_AUXILIARS_JSONINTERFACE_HPP_
