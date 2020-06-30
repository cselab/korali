***********************************
Exponential Latent Variable Problem
***********************************

(It's not as bad as it sounds.)

In a Bayesian *latent variable* problem, the model includes a set of unobserved variables, in addition to the variables parameterizing the distribution that we want to estimate.

That is, we have a probability distribution of the following form:
 :math:`p( d, z  | \psi )`

Here, d are observed data points, z the latent variables, and :math:`\psi` the distribution parameters (aka hyperparameters).

**Exponential family distribution requirement:**

We restrict the probability distribution to be from the `exponential family <https://en.wikipedia.org/wiki/Exponential_family>`_,
that is, it must be possible to bring it into the following form:
:math:`p( d, z  | \psi )  = exp\{-\zeta(\psi)  + S(d, \psi) * \phi(\psi) \}`


One goal is to find :math:`\psi`, as the value that maximizes its a-posteriori probability:
:math:`\psi^* = argmax_{\psi} \int_{z} p(\psi, z | d)  dz =  argmax_{\psi} \int_{z} \frac{p(d, z | \psi) p(\psi)}{p(d)} dz`

p(d) does not depend on z or :math:`\psi`, so we can ignore p(d) and maximize the unnormalized probability,
:math:`argmax_{\psi} \int_{z} p(d, z | \psi) p(\psi) dz`.

This can, for example, be solved by the expectation maximization algorithm.


Configuration
-------------

Functions composing the log-likelihood: S, phi, zeta
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
S, zeta, phi are functions that should be passed by the user. They take as argument a "sample" object and return nothing; they internally set result variables of the sample.

How to define a function that takes as argument a "sample", and how to, internally, set the necessary result values?
The sample object acts similar to a dictionary. You can access the variable values as "Hyperparameters" and "Latent Variables", set the result by setting, respectively, "S", "phi" and "zeta". "S" and "psi" need to be vector-valued, even if they only have one dimension.  See for example tutorial `basic/11.latent.variables` and its model definition in `model/model.py`.

For example, in Python:

.. code-block:: python

    def model_zeta(s):
       x = s["Hyperparameters"][0]
       s["zeta"] = -0.5*x*x


In C++:

.. code-block:: c++

    #include "korali.hpp"
    void model_zeta(korali::Sample& s)
    {
      float x = s["Hyperparameters"][0];
      s["zeta"] = -0.5*x*x;
    }


**Important notes:**

Note the capital `S`, but lower case in `zeta` and `phi`.

You probably noticed that *nowhere did we make use of the data points*. Data points are given and fixed, therefore they can (and need to) be inserted into the probability-defining functions:math:`S` directly. (phi and zeta do not depend on the data points d.)

Finally: After implementing S, phi and zeta, it is advisable to test the distribution defined by them. Mistakes happen easily.  See for example the tutorial `basic/11.latent.variables`, there is such a test in `model/test_model.py`.



Defining a sampler
~~~~~~~~~~~~~~~~~~~

For use with the SAEM solver, latent variable problems need to define a *sampler*. This *sampler* needs to return samples of latent variables :math:`z` , according to its distribution :math:`p(z | d, \psi )`. Here again, the data :math:`d` is assumed given and *you* are responsible for including it in the sampling probability.

Note: Often you do not need a normalized probability for sampling. The probability given :math:`d` is proportional to the likelihood of (:math:`z, d`) when :math:`\psi` is given - that is, just sample :math:`z` from :math:`p(d, z | \psi)`.

See also the samplers defined in tutorial `basic/11.latent.variables`, in `model/tutorial_samplers.py`.

**How-To**

.. code-block:: python

    def my_sampler(sample):
        # ...
        return


A sampler is a function that takes one parameter, a `korali.Sample`, and sets the field `"Samples"` for that sample. (Note the term collision.) It returns nothing.

The sampler needs to read the fields `"Hyperparameters"` and `"Number Samples"`. `"Hyperparameters"` will be needed to calculate the distribution to sample from;  `"Number Samples"`  tells the sampler how many samples to return.

.. code-block:: python

    def my_sampler(sample):
        hyperparameters = sample["Hyperparameters"]
        nSamples = sample["Number Samples"]
        #
        # ... do something
        #
        sample["Samples"] = your_generated_samples.tolist()
        return


-  `"Hyperparameters"`: A 1-dimensional vector of hyperparameters. Variables have the same order as the order you specified when defining the variables of your experiment. For example `e["Variables"][2]` is the third variable. To make it easier to know the position of each variable in `sample["Hyperparameters"]`: When you set up the experiment, define all hyperparameters before your latent variables.
- `"Number Samples"`: An integer, how many latent-variable vectors to sample.
- `"Samples"`: Needs to be a list of lists, or a list of 1-D Numpy arrays. Viewed as an array, it has shape `nr_samples` x `nr_latent_variables`. Each item in the list is one sample.



Problem Settings
~~~~~~~~~~~~~~~~~

To summarize, the following fields need to be set for a `Latent` problem:

.. code-block:: python

    e = korali.Experiment()

    # S, phi and zeta functions as described above:
    e["Problem"][ "S Of Likelihood Model" ] = ...
    e["Problem"][ "Zeta Of Likelihood Model" ] = ...
    e["Problem"][ "Phi Of Likelihood Model" ] = ...

    # Whatever dimension your S and zeta return:
    e["Problem"]["S Dimension"]

    # a "sampler" function as described above:
    e["Probelm"]["Latent Variable Sampler" ]




Variable-Specific Settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~

For each variable you define, you need to set

.. code-block:: python

    e["Variable"][your_index][ "Bayesian Type" ] = "Latent"
    # or:
    e["Variable"][your_index][ "Bayesian Type" ] = "Hyperparameter"

to select what role this variable takes in the problem.

For use with SAEM, for hyperparameters, the following attributes need to be set as well:

.. code-block:: python

    e["Variable"][your_index]["Upper Bound"] = ...
    e["Variable"][your_index]["Lower Bound"] = ...


This is for the M-step of SAEM, where CMAES is run internally to optimize the hyperparameters.