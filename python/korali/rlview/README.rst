.. _korali-rlview:

*************************************
Korali RL Viewer
*************************************

Usage
========================

Plots the result of RL experiments and allows for comparing multiple results simultaneously. 

Syntax: :code:`python3 -m korali.rlview [--dir (RESULTS_DIR1 RESULTS_DIR2 ...)] [--minReward 1.00] [--maxReward 1.00] [--updateFrequency 1.00] [--test] [--check]`

Where:

  - :code:`--dir` specifies the source path(s) of Korali results to plot, separated by space. By default: :code:`_korali_result/`
  - :code:`--minReward` specifies the lower bound on the y-axis (reward)
  - :code:`--minReward` specifies the upper bound on the y-axis (reward)
  - :code:`--updateFrequency` specifies the how often should the plotter show live updates
  - :code:`--test` verifies that the tool works, without plotting to screen.
  - :code:`--check` verifies that the tool is correctly installed, for testing purposes.
