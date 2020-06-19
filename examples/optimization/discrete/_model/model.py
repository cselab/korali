#!/usr/bin/env python


# Minus g09
def model(s):
  npar = 10
  res = 0.0
  v = s["Parameters"]

  for i in range(npar):
    if (i == 0 or i == 1 or i == 3 or i == 6):
      res += pow(10, 6.0 * i / npar) * round(v[i]) * round(v[i])
    else:
      res += pow(10, 6.0 * i / npar) * v[i] * v[i]

  s["F(x)"] = -res


def modelGrid(p):
  x = p["Parameters"][0]
  p["F(x)"] = -0.5 * x * x
