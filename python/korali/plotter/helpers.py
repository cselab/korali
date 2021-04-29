import os
import json
import colorsys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm


# Get a list of evenly spaced colors in HLS huse space.
def hlsColors(num, h=0.01, l=0.6, s=0.65):
  hues = np.linspace(0, 1, num + 1)[:-1]
  hues += h
  hues %= 1
  hues -= hues.astype(int)
  palette = [list(colorsys.hls_to_rgb(h_i, l, s)) for h_i in hues]
  return palette


# Finds the continuous segments of colors and returns those segment
def findContiguousColors(y, threshold, clow, chigh):
  colors = []
  for val in y:
    if (val < 0):
      colors.append(clow)
    else:
      colors.append(chigh)
  segs = []
  curr_seg = []
  prev_color = ''
  for c in colors:
    if c == prev_color or prev_color == '':
      curr_seg.append(c)
    else:
      segs.append(curr_seg)
      curr_seg = []
      curr_seg.append(c)
      curr_seg.append(c)
    prev_color = c
  segs.append(curr_seg)
  return segs


# Plots abs(y-threshold) in two colors
#   clow for y < threshold and chigh else
def drawMulticoloredLine(ax, x, y, threshold, clow, chigh, lab):
  segments = findContiguousColors(y, threshold, clow, chigh)
  start = 0
  absy = [abs(val) for val in y]
  labelled = set()
  for seg in segments:
    end = start + len(seg)
    if seg[0] in labelled:
      l, = ax.plot(x[start:end], absy[start:end], c=seg[0])
    else:
      l, = ax.plot(x[start:end], absy[start:end], c=seg[0], label=lab)
      labelled.add(seg[0])
    start = end - 1
