#!/usr/bin/env python


# Single function evaluation
def model(p):
  x = p["Parameters"][0]
  p["F(x)"] = -0.5 * x * x
