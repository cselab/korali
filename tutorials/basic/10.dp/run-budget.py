#!/usr/bin/env python3
import math

# Starting Korali's Engine
import korali
k = korali.Engine()
budget = 1

evalFunctions = [
  lambda x : 2*x,
  lambda x : -30*x*x + 17.63*x
  ]

N = len(evalFunctions)

def rewardFunction(k):
  # Determining current recursion depth
  i = k["Current Depth"]
  
  # Checking if policy passes constraints
  sum = 0
  for decision in k["Policy"]: sum = sum + decision[0]

  if (i < N-1):
   if (sum >  budget): 
    k["Cost Evaluation"] = math.inf
    return
    
  else: 
   if (sum != budget): 
    k["Cost Evaluation"] = math.inf
    return 
    
  # The constraints are satisfied, evaluate reward model
  x = k["Policy"][i][0]
  k["Cost Evaluation"] = -evalFunctions[i](x)
  
# Creating new experiment
e = korali.Experiment()

# Configuring Problem
e["Problem"]["Type"] = "DynamicProgramming"
e["Problem"]["Cost Function"] = rewardFunction

# Defining the problem's variables.
e["Variables"][0]["Name"] = "X"
e["Variables"][0]["Lower Bound"] = 0.0
e["Variables"][0]["Upper Bound"] = 1.0
e["Variables"][0]["Interval Count"] = 100

# Configuring the discretizer solver's parameters
e["Solver"]["Type"] = "RecursiveDiscretizer"
e["Solver"]["Termination Criteria"]["Recursion Depth"] = N

# Running Korali
k.run(e)

print('Qmax: ' + str(e["Results"]["Optimal Policy"]))
print('F(Qmax) = ' + str(-e["Results"]["Policy Evaluation"]))
