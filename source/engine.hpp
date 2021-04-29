#ifndef _KORALI_ENGINE_HPP_
#define _KORALI_ENGINE_HPP_

/** \file
* @brief Include header for the Korali Engine
*/

#include "config.hpp"
#include "modules/conduit/conduit.hpp"
#include "modules/conduit/distributed/distributed.hpp"
#include "modules/experiment/experiment.hpp"
#include <chrono>
#include <map>
#include <stack>
#include <vector>

namespace korali
{
class Sample;

/**
  * @brief A Korali Engine initializes the conduit and experiments, and guides their execution.
 */
class Engine : public Module
{
  public:
  Engine();

  /**
    * @brief A pointer to the execution conduit. Shared among all experiments in the engine.
    */
  Conduit *_conduit;

  /**
   * @brief Verbosity level of the Engine ('Silent', 'Minimal' (default), 'Normal' or 'Detailed').
  */
  std::string _verbosityLevel;

  /**
    * @brief Stores the list of experiments to run.
    */
  std::vector<Experiment *> _experimentVector;

  /**
    * @brief Stores the main execution thread (coroutine).
    */
  cothread_t _thread;

  /**
   * @brief Saves the output path for the profiling information file
   */
  std::string _profilingPath;

  /**
  * @brief Specifies how much detail will be saved in the profiling file (None, Full)
  */
  std::string _profilingDetail;

  /**
  * @brief Specifies every how many generation will the profiling file be updated
  */
  double _profilingFrequency;

  /**
  * @brief Stores the timepoint of the last time the profiling information was saved.
  */
  std::chrono::time_point<std::chrono::high_resolution_clock> _profilingLastSave;

  /**
  * @brief Saves the profiling information to the specified path
  * @param forceSave Saves even if the current generation does not divide _profilingFrequency. Reserved for last generation.
  */
  void saveProfilingInfo(const bool forceSave = false);

  /**
   * @brief Initialization stage of the Korali Engine
   */
  void initialize() override;

  /**
   * @brief Stores a set experiments into the experiment list and runs them to completion.
   * @param experiments Set of experiments.
   */
  void run(std::vector<Experiment> &experiments);

  /**
   * @brief Stores a single experiment into the experiment list and runs it to completion.
   * @param experiment The experiment to run.
   */
  void run(Experiment &experiment);

  /**
   * @brief Runs the stored list of experiments.
   */
  void start();

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
   * @brief Stores the JSON based configuration for the engine.
  */
  KoraliJson _js;

  /**
   * @brief Determines whether this is a dry run (no conduit initialization nor execution)
  */
  bool _isDryRun;

  /**
  * @brief (Worker) Stores a pointer to the current Experiment being processed
  */
  Experiment *_currentExperiment;

  /**
   * @brief Returns the worker teams MPI communication pointer (Distributed Conduit only).
   * @return Numerical pointer to the MPI communicator
   */
  static long int getMPICommPointer();

  /**
   * @brief Serializes Engine's data into a JSON object.
   * @param js Json object onto which to store the Engine data.
   */
  void serialize(knlohmann::json &js);

  /**
   * @brief Deserializes JSON object and returns a Korali Engine
   * @param js Json object onto which to store the Engine data.
   * @return The Korali Engine
   */
  static Engine *deserialize(const knlohmann::json &js);
};

/**
* @brief Flag indicating that Korali has been called from Korali
*/
extern bool isPythonActive;

/**
* @brief Stack storing pointers to different Engine execution levels
*/
extern std::stack<Engine *> _engineStack;
} // namespace korali

#endif
