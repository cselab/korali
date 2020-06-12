
========================================================
SAEM (Stochastic Approximation Expectation Maximization)
========================================================



This is an implementation of the *Stochastic Approximation Expectation Maximization*
algorithm. See for example `this page <http://wiki.webpopix.org/index.php/The_SAEM_algorithm_for_estimating_population_parameters>`_,
or chapter 9 of `Lavielle's book <http://www.cmap.polytechnique.fr/~lavielle/book.html>`_ for reference.

It is a stochastic variant of the expectation maximization algorithm. Expectation maximization assumes we have a probability distribution over a set of observed data, :math:`X = (x_i)_i`, and latent variables, :math:`\theta`. The distribution is parameterized by :math:`\psi`:

:math:`p = p(X, \theta | \psi)`

Often one has the case :math:`p = \prod_i q(x_i, \theta | \psi)`, where :math:`q` is the probability of one data point.



**Or rather:** Expectation maximization *works for any optimization problem* with two distinct sets of variables, :math:`h_1` and :math:`h_2`, to optimize for. But it is most useful if p is easy to optimize for one variable, say :math:`h_2 := \psi`, whenever the other variable, :math:`h_1 := \theta`, is known. This is often the case in latent variable problems.



*Stochastic approximation* EM approximates the E-step, where :math:`p(\theta | x, \psi)` is calculated, in a specific way through sampling.



For SAEM to work, the probability distribution must be from the   `exponential family <https://en.wikipedia.org/wiki/Exponential_family>`_.
Most of the frequently used distributions belong to the exponential family: See `this table <https://en.wikipedia.org/wiki/Exponential_family#Table_of_distributions>`_.

Usage:
======
See tutorial `basic/11.latent.variables` for an example. 

SAEM can so far only be used with problems of type 'Bayesian/Latent/ExponentialLatent', which imposes the exponential family type for the distribution.

Configuration and Solver Settings
---------------------------------

.. code-block:: python

  
  k = korali.Engine()
  e = korali.Experiment()

  e["Problem"]["Type"] = "Bayesian/Latent/ExponentialLatent"
  e["Problem"]["S Of Likelihood Model"] = ... # a function
  e["Problem"]["Zeta Of Likelihood Model"] = ... # a function
  e["Problem"]["Phi Of Likelihood Model"] = ... # a function
  e["Problem"]["S Dimension"] = ... # depends on S and Phi
  e["Problem"]["Latent Variable Sampler"] = ...# a user-defined sampler
  
  e["Solver"]["Type"] = "SAEM"
  e["Solver"]["Number Samples Per Step"] = 100 
  e["Solver"]["Termination Criteria"]["Max Generations"] = 100

  ... # then, define the variables

  k.run(e)



See `ExponentialLatent <../../problem/bayesian/latent/exponentialLatent/README.rst>`_ for details of the problem parameters.

Variable-Specific Settings
--------------------------

- Each variable needs an `initial value`.

- As `ExponentialLatent` is a `Bayesian` problem, each variable requires a prior distribution, although this would not be necessary for SAEM. SAEM throughout uses (log-) likelihood, not the (log-) posterior, therefore your choice of prior should not have any influence on the result.
  *Note, in case this behavior is ever changed: To ensure that the choice of prior does not influence results, choose a uniform distribution for hyperparameters. (You need to specify lower and upper bounds for them anyway.) Priors for latent variables are not part of the latent variable distribution and will/should always be ignored.* 
- Other parameters required for the `ExponentialLatent` problem: `Bayesian Type` to mark variables as latent vs. hyperparameter; and `upper bound`, `lower bound` for hyperparameter variables.

Termination Criteria
--------------------

For example: 

.. code-block:: python

    e["Solver"]["Termination Criteria"]["Max Generations"] = 100


Currently only the standard termination criteria are supported. 