
Inference with Reference Data
==================================

In this tutorial we show how to **optimize** and **sample** the posterior
distribution of a Bayesian inference problem. 

Problem Description
---------------------------

In this example we will solve the inverse problem of estimating the Variables
of a linear model using noisy data. We consider the computational model,

.. math::

  f(x;\vartheta) = \vartheta_0 + \vartheta_1 x \,,

for :math:`x\in\mathbb{R}`. We assume the following error model,

.. math::

  y = f(x;\vartheta) + \varepsilon \,,


with :math:`\varepsilon` a random variable that follows normal distribution with zero
mean and :math:`\sigma` standard deviation. This assumption leads to the likelihood
function,

.. math::

   p(y|\varphi,x) = \mathcal{N} ( \,y \,| \, f(x;\vartheta), \sigma^2 \,) \,.

where :math:`\varphi=(\vartheta,\sigma)` is the parameter vector that contains the
computational variables and the variables of the statistical model.

The data on which we condition our posterior distribution is defined in the model (see source code).

We call this data set :math:`d=\{x_i,y_i\}_{i=1}^5`. Assuming that each datum is
independent, the likelihood of $d$ under the linear model is given by

.. math::

   p(y|\vartheta,x) = \prod_{i=1}^6 \mathcal{N} ( \,y_i \,| \, f(x_i,\vartheta), \sigma^2 \,) \,.

In order to identify the distribution of :math:`\varphi` conditioned on the observations :math:`d`
we use Bayes' theorem

.. math::

   p(\varphi | y,x) = \frac{ p(y|\varphi,x) \, p(\varphi) }{ p(y) } \, .


As a prior information we choose the uniform distribution in  :math:`[-5,5]` for :math:`\vartheta`
and the uniform distribution in :math:`[0,10]` for :math:`\sigma`.


The Objective Function
---------------------------

Create a folder named `model`. Inside, create a file with name `posteriorModel.py` and paste the following code,

.. code-block:: python

    #!/usr/bin/env python

    def model( s, x ):

        v1 = s["Parameters"][0]
        v2 = s["Parameters"][1]

        result = [ ]
        for i in range(len(x)):
          result.append(v1*x[i] + v2)

        s["Reference Evaluations"] = result

This function corresponds implements the computational model that corresponds to :math:`f(x\vartheta) = \vartheta_0 + \vartheta_1 x`. Note: The following might be outdated: The object `s` must be of type `Korali::modelData` This class provides the methods `getParameter` and `addResult`. For a detailed presentation see [here]

In the same file add the following functions that return the data presented in the table above,

.. code-block:: python

    def getReferenceData():
      y=[]
      y.append(3.2069);
      y.append(4.1454);
      y.append(4.9393);
      y.append(6.0588);
      y.append(6.8425);
      return y

    def getReferencePoints():
      x=[]
      x.append(1.0);
      x.append(2.0);
      x.append(3.0);
      x.append(4.0);
      x.append(5.0);
      return x

Optimization with CMA-ES
---------------------------


First, open a file and import the korali module

.. code-block:: python

    #!/usr/bin/env python3
    import korali

Import the computational model,

.. code-block:: python

    import sys
    sys.path.append('./model')
    from posteriorModel import *

The Korali Experiment Object
-----------------------------------

Next we construct a `Korali.Experiment` object and set the computational model, where we already pass the data,

.. code-block:: python

    e = korali.Experiment()
    e["Problem"]["Computational Model"] = lambda sampleData: model(sampleData, getReferencePoints())

The reference points `x` returned by `getReferencePoints()` correspond to the *input* variables of the model. The function that
is passed to Korali should not have an argument for `x`. We have to create an intermediate
lambda function that will hide `x` from korali.

.. code-block:: python

    lambda sampleData: model(sampleData, getReferencePoints())

The Problem Type
---------------------------

The `Type` of the `Problem` is characterized as `Bayesian`

.. code-block:: python

    e["Problem"]["Type"] = "Evaluation/Bayesian/Inference/Reference"

When the Type is `Bayesian` we must set the type of likelihood and provide a vector with the `Reference Data` to Korali,

.. code-block:: python

    e["Problem"]["Likelihood Model"] = "Additive Normal"
    e["Problem"]["Reference Data"] = getReferenceData()

The Variables
---------------------------

We define two `Variables` of type `Computational` that correspond to :math:`\vartheta_0` and :math:`\vartheta_1`. The prior distribution of both is set to `Uniform`.

.. code-block:: python

    e["Variables"][0]["Name"] = "a"
    e["Variables"][0]["Bayesian Type"] = "Computational"
    e["Variables"][0]["Prior Distribution"] = "Uniform 0"
    e["Variables"][0]["Initial Mean"] = +0.0
    e["Variables"][0]["Initial Standard Deviation"] = +1.0

    e["Variables"][1]["Name"] = "b"
    e["Variables"][1]["Bayesian Type"] = "Computational"
    e["Variables"][1]["Prior Distribution"] = "Uniform 1"
    e["Variables"][1]["Initial Mean"] = +0.0
    e["Variables"][1]["Initial Standard Deviation"] = +1.0


The last parameter we add is of `Type` `Statistical` and corresponds to the variable
:math:`\sigma` in the likelihood function,

.. code-block:: python

    e["Variables"][2]["Name"] = "Sigma"
    e["Variables"][2]["Bayesian Type"] = "Statistical"
    e["Variables"][2]["Prior Distribution"] = "Uniform 2"
    e["Variables"][2]["Initial Mean"] = +2.5
    e["Variables"][2]["Initial Standard Deviation"] = +0.5


The Solver
---------------------------
Next, we choose the solver `CMA-ES`, the population size to be `24`.

.. code-block:: python

    e["Solver"]["Type"] = "Optimizer/CMAES"
    e["Solver"]["Population Size"] = 24

And activating one of its available termination criteria.

.. code-block:: python

    e["Solver"]["Termination Criteria"]["Max Generations"] = 100

We also need to configure the problem's random distributions, which we referred to when defining our variables,

.. code-block:: python

    e["Distributions"][0]["Name"] = "Uniform 0"
    e["Distributions"][0]["Type"] = "Univariate/Uniform"
    e["Distributions"][0]["Minimum"] = -5.0
    e["Distributions"][0]["Maximum"] = +5.0

    e["Distributions"][1]["Name"] = "Uniform 1"
    e["Distributions"][1]["Type"] = "Univariate/Uniform"
    e["Distributions"][1]["Minimum"] = -5.0
    e["Distributions"][1]["Maximum"] = +5.0

    e["Distributions"][2]["Name"] = "Uniform 2"
    e["Distributions"][2]["Type"] = "Univariate/Uniform"
    e["Distributions"][2]["Minimum"] = 0.0
    e["Distributions"][2]["Maximum"] = +5.0

For a detailed description of CMA-ES settings see :ref:`CMAES <module-solver-optimizer-cmaes>`

Finally, we configure the output, and then need to add a call to the run() routine to start the Korali engine.

.. code-block:: python

    e["File Output"]["Frequency"] = 5
    e["Console Output"]["Frequency"] = 5

    k = korali.Engine()
    k.run(e)

Running
---------------------------
We are now ready to run our example: `./run-cmaes.py`
The results are saved in the folder `_korali_result/`.



Plotting
---------------------------
You can see the results of CMA-ES by running the command, `python3 -m korali.plotter --dir _korali_result_cmaes`


Sampling with TMCMC
---------------------------

To sample the posterior distribution, we set the solver to `TMCMC` sampler and set a few settings,

.. code-block:: python

    e["Solver"]["Type"] = "Sampler/TMCMC"
    e["Solver"]["Population Size"] = 5000

For a detailed description of the TMCMC settings see :ref:`TMCMC <module-solver-sampler-tmcmc>`

Finally, we need to add a call to the run() routine to start the Korali engine.

.. code-block:: python

    k.run(e)

Running
---------------------------

We are now ready to run our example: `./run-tmcmc.py`

The results are saved in the folder `_korali_result/`.

Plottting
---------------------------

You can see a histogram of the results by running the command `python3 -m korali.plotter --dir _korali_result_tmcmc`


Sampling with Nested Sampling
-----------------------------

To sample the posterior distribution with the Nested sampler wa set a few settings,

.. code-block:: python

    e["Solver"]["Type"] = "Sampler/Nested"
    e["Solver"]["Number Live Points"] = 1500
    e["Solver"]["Resampling Method"] = "Ellipse" # (Default)

or instead use Mulit Ellipsoidal Sampling

.. code-block:: python
 
    e["Solver"]["Type"] = "Sampler/Nested"
    e["Solver"]["Number Live Points"] = 1500
    e["Solver"]["Resampling Method"] = "Multi Ellipse"


For a detailed description of the Nested Sampling settings see :ref:`Nested <module-solver-sampler-nested>`

Finally, we need to add a call to the run() routine to start the Korali engine.

.. code-block:: python

    k.run(e)

Running
---------------------------

We are now ready to run our example: `./run-nested.py` respectively `./run-multinest.py`


Plottting
---------------------------

You can see a histogram of the results by running the command `python3 -m korali.plotter --dir _korali_result_nested`
