Latent Space Optimization
==================================================================

Here we optimize a model with the solver `SA-EM`  to solve two different problems. Both aim to find the parameters for a probability distribution, that maximize the likelihood of a set of observed points :math:`X = \{x_i\}_i`,  :math:`x_i \in \mathbb{R}^n`.

1. **Simple problem:** 
   The probability distribution is a simple Gaussian in :math:`\mathbb{R}^n` , with mean :math:`\mu` and covariance :math:`\sigma^2\mathbb{I}_n`:
   :math:`p(X | \mu, \sigma) = \prod_i \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x_i-\mu)^2}{2\sigma^2}}`
   We use :math:`\mu \in \mathbb{R}^n` as "latent variable" :math:`\theta` and :math:`\sigma \in \mathbb{R}` as hyperparameter :math:`\psi`.  This shows that SA-EM works also for two arbitrary sets of hyperparameters, without latent variables in the typical sense.
2. **Clustering problem:** 
   We have a mixture of Gaussians, with :math:`C` clusters with different means :math:`\mu_c \in \mathbb{R}^n` and equal covariance  :math:`\sigma^2\mathbb{I}_n`,  :math:`\sigma \in \mathbb{R}` . That is, given cluster assignments :math:`c_i` ( :math:`x_i` belongs to cluster :math:`c_i \in \{1, ... C\}`), the joint probability is:
   :math:`p(X | c_1, ... c_N, \mu_1, ... \mu_C, \sigma) = \prod_i  \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x_i-\mu_{c_i})^2}{2\sigma^2}}`.
   Here, latent variables are the assignments :math:`c_i \in \{1, ... C\}, i \in {1, ..., N}` where :math:`N` is the number of data points. As hyperparameters we have :math:`C` means :math:`\mu_c`, and a single :math:`\sigma \in \mathbb{R}` defining the covariance.



Code files
----------

- :code:`run-saem.py` and :code:`run-saem-gaussian-mixture.py`: Contain the main code, defining the experiment to run.
- :code:`model/model.py` :  Defines the probability distributions, in exponential form
- :code:`model/tutorial_samplers.py` :  Implements sampling of latent variables from the distributions defined in :code:`model/model.py`.
- :code:`model/load_data.py` :  Functionality to read the data points from :code:`data_single.in` and :code:`data_multiple.in` . Data points need to be considered in both sampling and when defining the probability distributions.

-----------------------------------

- :code:`model/generate_data.py` :  Run this to re-generate data points. Writes points sampled from a single Gaussian into :code:`data_single.in` and points sampled from a multi-modal Gaussian into :code:`data_multiple.in`. You can change the dimension, number of clusters, number of points, mean vectors and standard deviation.
- :code:`model/test_model.py` :  For completeness: Tests that ensure correctness of the distributions defined in :code:`model/model.py`.




How to run the example
----------------------

In a shell from this directory (inside :code:`11.latent.variables`), type
.. code-block::

    $ python3 run-saem.py

to run the simple example. Or:

.. code-block::

    $ python3 run-saem-gaussian-mixture.py


for the clustering example.

This should output information about the process and result of the optimization.  



Code explanation
----------------

This section explains what happens in :code:`run-saem.py`.

First, we import our model definition (the parameterized probability distribution) as well as the sampler we want to use. We also need to import Korali and Numpy:

.. code-block:: python

    import sys
    sys.path.append('./model')
    from model.model import *
    from model.tutorial_samplers import *

    import numpy as np # we use numpy for random initializations
    import korali


Computational Model
~~~~~~~~~~~~~~~~~~~

In the main function, we then initialize the distribution, by creating an object of our class :code:`ExampleDistribution1`. It defines S, zeta and phi which already include data points read from :code:`data_single.in`:

.. code-block:: python

    def main():
        # Initialize the distribution
        distrib1 = ExampleDistribution1()

        distrib1_S = lambda s: distrib1.S(s)
        distrib1_zeta = lambda s: distrib1.zeta(s)
        distrib1_phi = lambda s: distrib1.phi(s)




The Sampler
~~~~~~~~~~~~

Then, we initialize the sampler which is managed by our class :code:`MCMCLatentSampler`:

.. code-block:: python

    # distrib1._p is a wrapper for the data points stored in data_single.in :
    d1_numberLatentVars = distrib1._p.nDimensions 
    d1_numberHyperparams = 1

    initialSigma = 4 
    # Choose random initial values for the variables used in sampling 
    d1_initialLatentValues = np.random.normal(0, 0.5, (d1_numberLatentVars,))
    d1_initialHyperparams = np.array([initialSigma])

    # Create an instance of our sampler class
    gaussian_sampler_obj = MCMCLatentSampler( d1_numberLatentVars, d1_numberHyperparams, 
                                            d1_initialLatentValues, d1_initialHyperparams, 
                                            distrib1_zeta,  distrib1_S, distrib1_phi)

    # This will be passed as sampler to Korali:
    sampling_function =  lambda sample:  gaussian_sampler_obj.sampleLatent(sample)




Defining the Experiment
~~~~~~~~~~~~~~~~~~~~~~~

We create a Korali engine and an experiment, and then configure the :code:`Problem` of our experiment:

.. code-block:: python

    k = korali.Engine()
    e = korali.Experiment()

    e["Problem"]["Type"] = "Bayesian/Latent"  # We need a "latent" problem
    e["Problem"]["S Of Likelihood Model"] = distrib1_S 
    e["Problem"]["Zeta Of Likelihood Model"] = distrib1_zeta
    e["Problem"]["Phi Of Likelihood Model"] = distrib1_phi
    e["Problem"]["S Dimension"] = 1  
    # distrib1_S and distrib1_phi create "S" and "phi" vectors (lists) of
    #   dimension 1. See comments in `model.py` for details about the 
    #   distribution.
    e["Problem"]["Latent Variable Sampler"] = sampling_function


The Solver
~~~~~~~~~~

We select SA-EM as solver, set the number of samples that the E-step should use in each generation, and decide to only optimize for 100 generations:   

.. code-block:: python

    e["Solver"]["Type"] = "SAEM"
    e["Solver"]["Number Samples Per Step"] = 100
    e["Solver"]["Termination Criteria"]["Max Generations"] = 100


Variables and Prior Distributions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As first variable, we define the standard deviatino :math:`\sigma`. We tell Korali that this is a "Hyperparameter" (as opposed to a latent variable).
We limit :math:`\sigma` to lie within [0, 15].
We also need to select a prior distribution (defined further below), because :code:`Latent` is a Bayesian problem; however, SAEM does not use a prior (so we could select an arbitrary prior).

.. code-block:: python

    e["Variables"][0]["Name"] = "sigma"
    e["Variables"][0]["Bayesian Type"] = "Hyperparameter"
    e["Variables"][0]["Prior Distribution"] = "Uniform 0"
    e["Variables"][0]["Initial Value"] = 5.0  # Initial hyperparameter value
    e["Variables"][0]["Upper Bound"] = 15
    e["Variables"][0]["Lower Bound"] = 0


We then define one variable for each coordinate of :math:`\mu`, the "latent variable". Variables in Korali are scalar variables, that is, to represent a vector-valued quantity, we define a separate variable for each dimension.

.. code-block:: python

    for i in range(distrib1._p.nDimensions):
        e["Variables"][1 + i]["Name"] = "mu" + str(i)
        # This tells Korali that we want to treat mu_i as latent variable:
        e["Variables"][1 + i]["Bayesian Type"] = "Latent"
        e["Variables"][1 + i]["Prior Distribution"] = "Uniform 1"
        e["Variables"][1 + i]["Initial Value"] = 0


Finally, we also need to define (unused) prior distributions: 

.. code-block:: python

    e["Distributions"][0]["Name"] = "Uniform 0"
    e["Distributions"][0]["Type"] = "Univariate/Uniform"
    e["Distributions"][0]["Minimum"] = 0
    e["Distributions"][0]["Maximum"] = 5

    e["Distributions"][1]["Name"] = "Uniform 1"
    e["Distributions"][1]["Type"] = "Univariate/Uniform"
    e["Distributions"][1]["Minimum"] = -5
    e["Distributions"][1]["Maximum"] = 5


Running the Optimization
~~~~~~~~~~~~~~~~~~~~~~~~

Finally, we call the :code:`run()` routine to run the optimization, to find the best value for :math:`\sigma` (and an approximation-by-sampling of :math:`\mu`):

.. code-block:: python

    k.run(e)


And then we wait for the result. This experiment can take a while, because of the MCMC sampling that is run every generation. The final output should look similar to this:   

.. code-block::

    [Korali] SAEM finished correctly.
    [Korali] Termination Criterion Met: Solver['Max Generations'] = 100.
    [Korali] Final hyperparameters:
    [Korali] sigma : 0.60
    [Korali] -- Final latent variable sample values :
    [Korali]  mu0 : 2.20 +- 0.02
    [Korali]  mu1 : 2.06 +- 0.03
    [Korali] Final loglikelihood: -4.6e+01%
    [Korali] Final best loglikelihood: -4.6e+01%
    [Korali] Final Generation: 100
    [Korali] Elapsed Time: 169.675s



The second experiment, :code:`run-saem-gaussian-mixture`, runs faster since it uses a much simpler sampler.

