#include "korali.h"
#include "model/directModel.h"

int main(int argc, char* argv[])
{
 auto k = Korali::Engine();

 k["Problem"] = "Direct Evaluation";
 k["Solver"]  = "DE";
 k["Verbosity"] = "Detailed";

 k["Variables"][0]["Name"] = "X";
 k["Variables"][0]["DE"]["Lower Bound"] = -10.0;
 k["Variables"][0]["DE"]["Upper Bound"] = +10.0;

 k["DE"]["Sample Count"] = 32;

 k["DE"]["Termination Criteria"]["Max Generations"]["Value"] = 100;
 k.setModel([](Korali::ModelData& d) { directModel(d.getVariables(), d.getResults()); });
 k.run();
}
