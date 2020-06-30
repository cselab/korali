import numpy as np
import korali

from utils import univariate_gaussian_probability


class MCMCLatentSampler:

  def __init__(self, numberLatentVars, numberHyperparams, initialLatentValues,
               initialHyperparams, zeta_, S_, phi_):
    self.zeta_func = zeta_
    self.S_func = S_
    self.phi_func = phi_
    assert (
        len(initialLatentValues) == numberLatentVars
    ), "number of latent variables should match the dimension of their initial values"
    assert (
        len(initialHyperparams) == numberHyperparams
    ), "number of hyperparameters should match the dimension of their initial values"

    self.previousSampleMeans = initialLatentValues
    self.currentHyperparameters = initialHyperparams

    self.numberLatent = numberLatentVars
    self.numberHyperparameters = numberHyperparams

  def sampleLatent(self, kSample):
    # /*
    #  * probability to sample from:
    #  * p(d, z | theta) * p(theta) -- that's the (log-)posterior
    #  * - use a "Sampling" problem, with our log-posterior as "Likelihood Model" , but with the current values for theta inserted.
    # */

    hyperparameters = kSample["Hyperparameters"]
    numberSamples = kSample["Number Samples"]
    if (kSample["Number Of Latent Variables"] != self.numberLatent):
      raise ValueError(
          "Implementation error, number of latent variables at initialization does not fit to what was passed as variable"
      )

    #  *  Create one sampling experiment to sample all latent variables. After all, the latent vars are correlated /
    #     have a joint distribution .

    def probability_function(s):

      latent_vars = s["Parameters"]
      hparams = hyperparameters

      if (len(latent_vars) != self.numberLatent):
        raise ValueError(
            "Implementation error, latent variable vector had wrong size")

      if (len(hparams) != self.numberHyperparameters):
        raise ValueError(
            "Implementation error, hyperparameter vector had wrong size")

      s["Latent Variables"] = latent_vars
      s["Hyperparameters"] = hparams

      self.S_func(s)
      self.zeta_func(s)
      self.phi_func(s)

      # -> Assume these are set: sample["S"], sample["zeta"] and sample["phi"]

      _zetaValue = s["zeta"]
      _sValues = s["S"]
      _phiValues = s["phi"]
      logP_of_x = -_zetaValue + np.inner(_sValues, _phiValues)
      s["P(x)"] = logP_of_x

    # * * * * *  * * * * *  * * * * * probability_function end

    k = korali.Engine()
    e = korali.Experiment()

    # * Based on tutorial a2-sampling
    e["Problem"]["Type"] = "Sampling"
    e["Problem"]["Probability Function"] = lambda s: probability_function(s)

    for i in range(self.numberLatent):

      # Defining problem's variables
      varName = "latent_" + str(i)

      e["Variables"][i]["Name"] = varName
      e["Variables"][i]["Initial Mean"] = self.previousSampleMeans[i]

      e["Variables"][i]["Initial Standard Deviation"] = 2.0

    # Configuring the MCMC sampler parameters
    e["Solver"]["Type"] = "Sampler/MCMC"
    e["Solver"]["Burn In"] = 100
    e["Solver"]["Termination Criteria"]["Max Samples"] = 200

    # Configuring output settings
    e["File Output"]["Frequency"] = 0
    e["File Output"]["Path"] = "_korali_sampling_results"
    e["Console Output"]["Frequency"] = 0
    e["Console Output"]["Verbosity"] = "Silent"

    #k["Conduit"]["Type"] = "Concurrent"
    #k["Conduit"]["Concurrent Jobs"] = 2
    k.run(e)

    db = e["Solver"]["Sample Database"]
    samples = db[-numberSamples:]  # take samples from the end

    kSample["Samples"] = samples

    # set new "previous sample means"
    for i in range(self.numberLatent):
      self.previousSampleMeans[i] = np.sum(
          np.array(samples)[:, i]) / float(numberSamples)


class MultimodalGaussianSampler():

  def __init__(self, points_, nDimensions_, nClusters_):
    self.nDimensions = nDimensions_
    self.nClusters = nClusters_
    self.points = np.array(points_)
    self.nPoints = len(points_)

  def sampleLatent(self, k):
    # /* Sample assignments for each point separately, proportional to the resulting
    #    data likelihood, p(point, assignment | hyperparams) */

    hyperparameters = k["Hyperparameters"]
    nSamples = k["Number Samples"]
    if (k["Number Of Latent Variables"] != self.nPoints):
      raise BaseException(
          "Implementation error, number of latent variables at initialization does not fit to what was passed as data"
      )

    # get sigma
    sigma = hyperparameters[self.nClusters * self.nDimensions]

    # get vector of means
    mus = np.zeros((self.nClusters, self.nDimensions))
    for i in range(self.nClusters):
      mu = hyperparameters[i * self.nDimensions:(i + 1) * self.nDimensions]
      if (len(mu) != self.nDimensions):
        raise BaseException("Implementation error, dimensions did not match")
      mus[i] = mu

    # we sample in another order, will later transpose
    samples_transpose = np.zeros((self.nPoints, nSamples))
    for i in range(self.nPoints):

      # First, get probabilities for each cluster
      probabilities = np.zeros((self.nClusters,))
      for j in range(self.nClusters):
        mu = mus[j]
        p = univariate_gaussian_probability(mu, sigma, self.points[i])
        probabilities[j] = p

      # normalize probabilities to one
      probabilities = probabilities / np.linalg.norm(probabilities)

      pointwise_samples = np.zeros((nSamples,), int)
      for j in range(nSamples):
        # sample
        u = np.random.uniform(0, 1, 1)
        sum = 0
        for c_idx in range(self.nClusters):
          sum = sum + probabilities[c_idx]
          if (u < sum):
            # cluster c_idx has been chosen!
            pointwise_samples[j] = c_idx
            break
      samples_transpose[i] = pointwise_samples

    samples = np.transpose(samples_transpose)
    k["Samples"] = samples.tolist()
