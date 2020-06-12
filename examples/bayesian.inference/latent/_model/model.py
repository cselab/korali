import load_data
import numpy as np

# Model 1:
# A single Gaussian distribution, with
# Hyperparameter = sigma, the standard deviation, and
# Latent variable = mu, the mean. Assume a uniform prior distribution of the mean in [0,1].
# Assume the probability of mu is supported in [-20, 20]^nDimensions.
#
#
#
# Model 2:
# Assume we have two gaussian distributions with peaks around two means, and identical
# covariance = sigma.
# Hyperparameters:
#     mu1, mu2 (vectors) and sigma (just one single 1-d variable) (in this order)
# Latent variables:
#     Assignment of each data point to the modes


class ExponentialFamilyDistribution():

  def __init__(self):
    self._p = None
    self.sufficientStatisticsDimension = None

  def S(self, sample):
    raise NotImplementedError

  def zeta(self, sample):
    raise NotImplementedError

  def phi(self, sample):
    raise NotImplementedError


class ExampleDistribution1(ExponentialFamilyDistribution):
  #  Take the hyperparameter as sigma of a normal distribution, and the mean mu as latent variable

  def __init__(self):
    self._p = load_data.UnivariateData()
    self.sufficientStatisticsDimension = 1
    self.mu_lower_bound = -20
    self.mu_upper_bound = 20
    assert self.mu_upper_bound > self.mu_lower_bound
    self.mu_range = self.mu_upper_bound - self.mu_lower_bound

  def S(self, sample):
    mu_vector = np.array(sample["Latent Variables"])
    assert all([len(mu_vector) == len(pt) for pt in self._p.points])
    in_valid_range = True
    for mu_coord in mu_vector:
      if ((mu_coord < self.mu_lower_bound) or (mu_coord > self.mu_upper_bound)):
        in_valid_range = False
        sample["S"] = [-np.inf]
        return

    # log(p) = -n*log(sigma*sqrt(pi*2)) - 0.5(x - mu)^2 * 1/sigma^2
    vector_distances = [pt - mu_vector for pt in self._p.points]
    squared_distance_per_point = [
        np.inner(dist, dist) for dist in vector_distances
    ]
    sample["S"] = [-np.sum(squared_distance_per_point)]

  def zeta(self, sample):
    hyperparams = sample["Hyperparameters"]
    sigma = hyperparams[0]
    log_hypercube_volume = self._p.nPoints * np.log(self.mu_range)
    #  \__ to get a normalized distribution in both x and mu, need to multiply P by a uniform distribution in mu
    # n*log(sigma * sqrt(pi * 2))
    n = self._p.nDimensions
    sample["zeta"] = n * np.log(
        sigma * np.sqrt(2 * np.pi)) * self._p.nPoints + log_hypercube_volume

  def phi(self, sample):
    hyperparams = sample["Hyperparameters"]
    sigma = hyperparams[0]
    # * 1/(2 * sigma^2)
    sample["phi"] = [0.5 / sigma**2]

    # /*Model 2:
    #     Assume we have two gaussian distributions with peaks around two means, and identical
    #     covariance = sigma.
    #     Hyperparameters:
    #         mu1, mu2 and sigma (in this order)
    #     Latent variables:
    #         Assignment of each data point to the modes
    #
    #     So,
    #       log(p) = sum_i [log(2*pi*sigma)*dim/2] - sum_i [  |x_i|^2  - <2*mu_c(i), x_i>  +  |mu_c(i)|^2  ]/(2*sigma^2)
    #
    #       ->
    #          zeta(sigma, mu1, mu2) = N * dim * log(2*pi*sigma)*1/2
    #          S(x1, c(1), ... xN, c(N))
    #                     = sum_i [vec(-|x_i|^2, delta(ci=1), delta(ci=2), x_i * delta(ci=1), x_i * delta(ci=2) ) ]
    #          phi(sigma, mu1, mu2)
    #                     = vec(1, -|mu1|^2, -|mu2|^2, 2 * mu1^T, 2 * mu2^T) * 1/(2*sigma)
    #
    # */


class ExampleDistribution2(ExponentialFamilyDistribution):

  def __init__(self):
    self._p = load_data.MultivariateData()
    self.sufficientStatisticsDimension = 1 + self._p.nClusters + self._p.nClusters * self._p.nDimensions

  def S(self, sample):
    # /* For two clusters:
    #     S(x1, c(1), ... xN, c(N))
    #                     = sum_i [- vec(|x_i|^2, delta(ci=1), delta(ci=2), x_i * delta(ci=1), x_i * delta(ci=2) ) ]*/
    assignments = sample["Latent Variables"]
    if (len(assignments) != self._p.nPoints):
      raise ValueError(
          "Latent variables should be exactly the cluster assignments, so there is one for each point in the sample."
      )

    S_dim = 1 + self._p.nDimensions * self._p.nClusters + self._p.nClusters
    S_vec = np.zeros((S_dim,), float)
    in_valid_range = True
    for a in assignments:
      if (a <= -0.5 or a >= self._p.nClusters - 0.51):
        in_valid_range = False
        S_vec[0] = np.array([-np.inf])
        sample["S"] = S_vec.tolist()
        return
    for i in range(self._p.nPoints):
      pt = self._p.points[i]
      S_vec[0] -= np.inner(pt, pt)
      cluster = int(np.round(assignments[i]))
      S_vec[cluster + 1] += 1
      mu_ci_location = self._p.nClusters + 1 + cluster * self._p.nDimensions
      S_vec[mu_ci_location:mu_ci_location + self._p.nDimensions] += pt

    sample["S"] = S_vec.tolist()

  def zeta(self, sample):
    hyperparams = sample["Hyperparameters"]
    if (len(hyperparams) != self._p.nDimensions * self._p.nClusters + 1):
        raise ValueError(
                "Hyperparameters should be one mean vector per cluster, plus a 1D variable sigma. The dimension of the hyperparameter vector did not match this."
        )

    sigma = hyperparams[self._p.nClusters * self._p.nDimensions]

    # dim * N * log(sigma*sqrt(pi*2))
    sample["zeta"] = self._p.nDimensions * self._p.nPoints * np.log(
        sigma*np.sqrt(2*np.pi))


  def phi(self, sample):
    hyperparams = sample["Hyperparameters"]
    sigma = hyperparams[self._p.nClusters * self._p.nDimensions]

    if (len(hyperparams) != self._p.nDimensions * self._p.nClusters + 1):
      raise ValueError(
            "Hyperparameters should be one mean vector per cluster, plus a 1D variable sigma. The dimension of the hyperparameter vector did not match this."
      )

    mus = []
    for i in range(self._p.nClusters):
      mu = hyperparams[i * self._p.nDimensions : (i + 1) * self._p.nDimensions]
      mus.append(mu)

    # /* For two variables:
    #       phi(sigma, mu1, mu2) = vec(1, -|mu1|^2, -|mu2|^2, mu1^T, mu2^T) * 1/(2*sigma)  */
    phi_dim = 1 + self._p.nDimensions * self._p.nClusters + self._p.nClusters
    phi = np.zeros((phi_dim,))
    phi[0] = 1.0
    for i in range(self._p.nClusters):
      phi[i + 1] = - np.inner(mus[i], mus[i])
      start_idx = 1 + self._p.nClusters + i * self._p.nDimensions
      phi[start_idx : start_idx + len(mus[0]) ] = np.array(mus[i]) * 2

    phi *= 1. / (2 * sigma ** 2)

    sample["phi"] = phi.tolist()
