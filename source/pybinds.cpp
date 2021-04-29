#include "engine.hpp"
#include "auxiliar/koraliJson.hpp"
#include "modules/experiment/experiment.hpp"
#include "sample/sample.hpp"

using namespace korali;

PYBIND11_MODULE(libkorali, m)
{
#ifdef _KORALI_USE_MPI
  m.def("getMPICommPointer", &Engine::getMPICommPointer, pybind11::return_value_policy::reference);
#endif

  pybind11::class_<Engine>(m, "Engine")
    .def(pybind11::init<>())
    .def("run", [](Engine &k, Experiment &e) {
      isPythonActive = true;
      k.run(e);
    })
    .def("run", [](Engine &k, std::vector<Experiment> &e) {
      isPythonActive = true;
      k.run(e);
    })
    .def("__getitem__", pybind11::overload_cast<pybind11::object>(&Engine::getItem), pybind11::return_value_policy::reference)
    .def("__setitem__", pybind11::overload_cast<pybind11::object, pybind11::object>(&Engine::setItem), pybind11::return_value_policy::reference);

  pybind11::class_<KoraliJson>(m, "koraliJson")
    .def("get", &KoraliJson::get)
    .def("set", &KoraliJson::set)
    .def("__getitem__", pybind11::overload_cast<pybind11::object>(&KoraliJson::getItem), pybind11::return_value_policy::reference)
    .def("__setitem__", pybind11::overload_cast<pybind11::object, pybind11::object>(&KoraliJson::setItem), pybind11::return_value_policy::reference);

  pybind11::class_<Sample>(m, "Sample")
    .def("__getitem__", pybind11::overload_cast<pybind11::object>(&Sample::getItem), pybind11::return_value_policy::reference)
    .def("__setitem__", pybind11::overload_cast<pybind11::object, pybind11::object>(&Sample::setItem), pybind11::return_value_policy::reference)
    .def("update", &Sample::update);

  pybind11::class_<Experiment>(m, "Experiment")
    .def(pybind11::init<>())
    .def("__getitem__", pybind11::overload_cast<pybind11::object>(&Experiment::getItem), pybind11::return_value_policy::reference)
    .def("__setitem__", pybind11::overload_cast<pybind11::object, pybind11::object>(&Experiment::setItem), pybind11::return_value_policy::reference)
    .def("loadState", &Experiment::loadState)
    .def("getEvaluation", &Experiment::getEvaluation);
}
