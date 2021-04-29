#include "engine.hpp"
#include "auxiliar/fs.hpp"
#include "auxiliar/koraliJson.hpp"
#include "modules/conduit/conduit.hpp"
#include "modules/conduit/distributed/distributed.hpp"
#include "modules/experiment/experiment.hpp"
#include "modules/problem/problem.hpp"
#include "modules/solver/solver.hpp"
#include "sample/sample.hpp"
#include <omp.h>
#include <sys/stat.h>
#include <sys/types.h>

namespace korali
{
std::stack<Engine *> _engineStack;
bool isPythonActive = 0;

Engine::Engine()
{
  _cumulativeTime = 0.0;
  _thread = co_active();
  _conduit = NULL;

  // Turn Off GSL Error Handler
  gsl_set_error_handler_off();
}

void Engine::initialize()
{
  // Setting Engine configuration defaults
  if (!isDefined(_js.getJson(), "Profiling", "Detail")) _js["Profiling"]["Detail"] = "None";
  if (!isDefined(_js.getJson(), "Profiling", "Path")) _js["Profiling"]["Path"] = "./profiling.json";
  if (!isDefined(_js.getJson(), "Profiling", "Frequency")) _js["Profiling"]["Frequency"] = 60.0;
  if (!isDefined(_js.getJson(), "Conduit", "Type")) _js["Conduit"]["Type"] = "Sequential";
  if (!isDefined(_js.getJson(), "Dry Run")) _js["Dry Run"] = false;

  // Loading configuration values
  _isDryRun = _js["Dry Run"];
  _profilingPath = _js["Profiling"]["Path"];
  _profilingDetail = _js["Profiling"]["Detail"];
  _profilingFrequency = _js["Profiling"]["Frequency"];

  // Initializing experiment's configuration
  for (size_t i = 0; i < _experimentVector.size(); i++)
  {
    _experimentVector[i]->_experimentId = i;
    _experimentVector[i]->_engine = this;
    _experimentVector[i]->initialize();
    _experimentVector[i]->_isFinished = false;
  }

  // Check configuration correctness
  auto js = _js.getJson();
  try
  {
    if (isDefined(js, "Conduit")) eraseValue(js, "Conduit");
    if (isDefined(js, "Dry Run")) eraseValue(js, "Dry Run");
    if (isDefined(js, "Conduit", "Type")) eraseValue(js, "Conduit", "Type");
    if (isDefined(js, "Profiling", "Detail")) eraseValue(js, "Profiling", "Detail");
    if (isDefined(js, "Profiling", "Path")) eraseValue(js, "Profiling", "Path");
    if (isDefined(js, "Profiling", "Frequency")) eraseValue(js, "Profiling", "Frequency");
  }
  catch (const std::exception &e)
  {
    KORALI_LOG_ERROR("[Korali] Error parsing Korali Engine's parameters. Reason:\n%s", e.what());
  }

  if (isEmpty(js) == false) KORALI_LOG_ERROR("Unrecognized settings for Korali's Engine: \n%s\n", js.dump(2).c_str());
}

void Engine::start()
{
  // Checking if its a dry run and return if it is
  if (_isDryRun) return;

  // Only initialize conduit if the Engine being ran is the first one in the process
  auto conduit = dynamic_cast<Conduit *>(getModule(_js["Conduit"], _k));
  conduit->applyModuleDefaults(_js["Conduit"]);
  conduit->setConfiguration(_js["Conduit"]);
  conduit->initialize();

  // Initializing conduit server
  conduit->initServer();

  // Assigning pointer after starting workers, so they can initialize their own conduit
  _conduit = conduit;

  // Recovering Conduit configuration in case of restart
  _conduit->getConfiguration(_js.getJson()["Conduit"]);

  if (_conduit->isRoot())
  {
    // Adding engine to the stack to support Korali-in-Korali execution
    _conduit->stackEngine(this);

    // Setting base time for profiling.
    _startTime = std::chrono::high_resolution_clock::now();
    _profilingLastSave = std::chrono::high_resolution_clock::now();

    while (true)
    {
      // Checking for break signals coming from Python
      bool executed = false;
      for (size_t i = 0; i < _experimentVector.size(); i++)
        if (_experimentVector[i]->_isFinished == false)
        {
          _currentExperiment = _experimentVector[i];
          co_switch(_experimentVector[i]->_thread);
          executed = true;
          saveProfilingInfo(false);
        }
      if (executed == false) break;
    }

    _endTime = std::chrono::high_resolution_clock::now();

    saveProfilingInfo(true);
    _cumulativeTime += std::chrono::duration<double>(_endTime - _startTime).count();

    // Finalizing experiments
    for (size_t i = 0; i < _experimentVector.size(); i++) _experimentVector[i]->finalize();

    // (Workers-Side) Removing the current engine to the conduit's engine stack
    _conduit->popEngine();
  }

  // Finalizing Conduit if last engine in the stack
  _conduit->finalize();
}

void Engine::saveProfilingInfo(const bool forceSave)
{
  if (_profilingDetail == "Full")
  {
    auto currTime = std::chrono::high_resolution_clock::now();
    double timeSinceLast = std::chrono::duration<double>(currTime - _profilingLastSave).count();
    if ((timeSinceLast > _profilingFrequency) || forceSave)
    {
      double elapsedTime = std::chrono::duration<double>(currTime - _startTime).count();
      __profiler["Experiment Count"] = _experimentVector.size();
      __profiler["Elapsed Time"] = elapsedTime + _cumulativeTime;
      saveJsonToFile(_profilingPath.c_str(), __profiler);
      _profilingLastSave = std::chrono::high_resolution_clock::now();
    }
  }
}

void Engine::run(Experiment &experiment)
{
  _experimentVector.clear();
  experiment._k->_engine = this;
  _experimentVector.push_back(experiment._k);
  initialize();
  start();
}

void Engine::run(std::vector<Experiment> &experiments)
{
  _experimentVector.clear();
  for (size_t i = 0; i < experiments.size(); i++)
  {
    experiments[i]._k->_engine = this;
    _experimentVector.push_back(experiments[i]._k);
  }
  initialize();
  start();
}

void Engine::serialize(knlohmann::json &js)
{
  for (size_t i = 0; i < _experimentVector.size(); i++)
  {
    _experimentVector[i]->getConfiguration(_experimentVector[i]->_js.getJson());
    js["Experiment Vector"][i] = _experimentVector[i]->_js.getJson();
  }
}

#ifdef _KORALI_USE_MPI
long int Engine::getMPICommPointer()
{
  return (long int)(&__KoraliTeamComm);
}
#endif

knlohmann::json &Engine::operator[](const std::string &key)
{
  return _js[key];
}
knlohmann::json &Engine::operator[](const unsigned long int &key) { return _js[key]; }
pybind11::object Engine::getItem(const pybind11::object key) { return _js.getItem(key); }
void Engine::setItem(const pybind11::object key, const pybind11::object val) { _js.setItem(key, val); }

} // namespace korali

