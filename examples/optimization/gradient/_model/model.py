#!/usr/bin/env python


# Function and Gradient function evaluation
def model_with_gradient(p):
  X = p["Parameters"]
  gradient = []
  evaluation = 0
  for x in X:
    evaluation += -0.5 * x * x
    gradient.append(-x)

  p["F(x)"] = evaluation
  p["Gradient"] = gradient
