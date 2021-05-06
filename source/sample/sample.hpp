/** \file
* @brief Contains the definition of a Korali Sample
*****************************************************************************************************/

#ifndef __KORALI_SAMPLE_HPP_
#define __KORALI_SAMPLE_HPP_

#include "auxiliar/koraliJson.hpp"
#include "auxiliar/libco/libco.h"
#include "auxiliar/logger.hpp"
#include "auxiliar/py2json.hpp"
#include <queue>
#include <string>

#undef _POSIX_C_SOURCE
#undef _XOPEN_SOURCE

namespace korali
{
class Experiment;
class Engine;

/**
 * @brief Macro to get information from a sample. Checks for the existence of the path and produces detailed information on failure.
 */
#define KORALI_GET(TYPE, SAMPLE, ...) \
  SAMPLE.get<TYPE>(__FILE__, __LINE__, __VA_ARGS__);

/**
 * @brief Macro to send message updates to the engine
 */
#define KORALI_SEND_MSG_TO_ENGINE(MESSAGE) \
  _k->_engine->_conduit->sendMessageToEngine(MESSAGE);

/**
 * @brief Macro to recv message updates from the engine
 */
#define KORALI_RECV_MSG_FROM_ENGINE() \
  _k->_engine->_conduit->recvMessageFromEngine();

/**
* @brief Execution states of a given sample.
*/
enum class SampleState
{
  uninitialized = 1,
  initialized = 2,
  running = 3,
  waiting = 4,
  finished = 5
};

/**
* \class Sample
* @brief Contains input/output data to computational models.
*/
class Sample
{
  public:
  /**
 * @brief Pointer to the C++ object containing the sample.
 * Necessary for integration with Python, because Python only passes objects by reference, and we need to
 * access the original pointer when working on the C++ side. Therefore, we need to store the pointer as a variable.
 */
  Sample *_self;

  /**
  * @brief Queue of messages sent from the sample to the engine
  */
  std::queue<knlohmann::json> _messageQueue;

  /**
  * @brief Pointer to global parameters
  */
  knlohmann::json *_globals;

  /**
  * @brief Current state of the sample
  */
  SampleState _state;

  /**
  * @brief User-Level thread (coroutine) containing the CPU execution state of the current Sample.
  */
  cothread_t _sampleThread;

  /**
  * @brief User-Level thread (coroutine) containing the CPU execution state of the calling worker.
  */
  cothread_t _workerThread;

  /**
  * @brief Storage to keep the iD of the worker processing this sample.
  */
  size_t _workerId;

  /**
  * @brief Determines whether the thread memory has been allocated.
  * Necessary to make sure we do not double-allocate or free unallocated space when re-executing sample.
  */
  bool _isAllocated;

  /**
  * @brief JSON object containing the sample's configuration and input/output data.
  */
  KoraliJson _js;

  /**
  * @brief Constructs Sample. Stores its own pointer, sets ID to zero, state as uninitialized, and isAllocated to false.
  */
  Sample();

  ~Sample();

  /**
  * @brief Runs a computational model by reinterpreting a numerical pointer to a function(sample) object to an actual function pointer and calls it.
  * @param functionPosition Number containing a pointer to a function.
  */
  void run(size_t functionPosition);

  /**
  * @brief Handles the execution thread of individual samples on the worker's side
  */
  void sampleLauncher();

  /**
  * @brief Returns results to the worker without finishing the execution of the computational model.
  */
  void update();

  /**
  * @brief Returns global parameters broadcasted by the problem
  * @return The global parameters
  */
  knlohmann::json &globals();

  /**
  * @brief Checks whether the sample contains the given key.
  * @param key Key (String) to look for.
  * @return True, if it is contained; false, otherwise.
  */
  bool contains(const std::string &key);

  /**
  * @brief Accesses the value of a given key in the sample.
  * @param key Key (String) to look for.
  * @return JSON object for the given key.
  */
  knlohmann::json &operator[](const std::string &key);

  /**
   * @brief Accesses the value of a given key in the sample.
   * @param key Key (number) to look for.
   * @return JSON object for the given key.
   */
  knlohmann::json &operator[](const unsigned long int &key);

  /**
  * @brief Gets the value of a given key in the sample.
  * @param key Key (pybind11 object) to look for.
  * @return Pybind11 object for the given key.
  */
  pybind11::object getItem(const pybind11::object key);

  /**
  * @brief Sets the value of a given key in the sample.
  * @param val Value to assign.
  * @param key Key (pybind11 object) to look for.
  */
  void setItem(const pybind11::object key, const pybind11::object val);

  /**
  * @brief Gets and dequeues a pending message, if exists.
  * @param message The message (json object) to overwrite, if a message exists.
  * @return True, if message found; false, if no message was found.
  */
  bool retrievePendingMessage(knlohmann::json &message);

  /**
   * @brief Retrieves an element from the sample information
   * @param fileName where the error occurred, given by the __FILE__ macro
   * @param lineNumber number where the error occurred, given by the __LINE__ macro
   * @param key a list of keys describing the full path to traverse
   * @return Requested value
   */
  template <class T, typename... Key>
  T get(const char fileName[], int lineNumber, const Key &... key)
  {
    if (isDefined(_self->_js.getJson(), key...) == false)
    {
      Logger::logError(fileName, lineNumber, "Requesting non existing value %s from sample.\n", getPath(key...).c_str());
    }

    try
    {
      return getValue(_self->_js.getJson(), key...);
    }
    catch (std::exception &e)
    {
      Logger::logError(fileName, lineNumber, "Missing or incorrect value %s for the sample.\n + Cause: %s\n", getPath(key...).c_str(), e.what());
    }
  }
};

} // namespace korali

#endif // __KORALI_SAMPLE_HPP_
