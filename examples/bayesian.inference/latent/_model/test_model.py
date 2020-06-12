#
#   ! Run this from the tutorial's main directory, from 11.latent.variables - else you get path errors
#
#   Test whether the distribution parameterized by S, zeta and phi in model.py is correct or not.
#
# import korali # No: circumvent using korali here, use dicts instead of samples
import numpy as np
import pdb

from load_data import *
from model import *
from utils import *


def test_distribution_1():
  raise NotImplementedError


# int test_distribution_1()[
#
#     # initialize the distribution
#     ExampleDistribution1 distrib1 = ExampleDistribution1();
#     std.function<void(korali.Sample& s)> distrib1_S = [&distrib1](korali.Sample& s) -> void [
#     	distrib1.S(s); ] ;
#     std.function<void(korali.Sample& s)> distrib1_zeta = [&distrib1](korali.Sample& s) -> void [
#     	distrib1.zeta(s); ] ;
#     std.function<void(korali.Sample& s)> distrib1_phi = [&distrib1](korali.Sample& s) -> void [
#     	distrib1.phi(s); ] ;
#
#
#     int nClusters = 1;
#     int nDimensions = distrib1._p.nDimensions; # 2
#     int d2_numberLatentVars = 1;
#     int d2_numberHyperparams =  1;
#
#      # Some value pairs:
#     std.vector<double> mu0 = [0, 0];
#     std.vector<double> mu1 = [2, 2];
#     std.vector<double> mu2 = [-0.5, 10];
#     double sigma = 1.0;
#     std.vector<std.vector<double> > hyperparams;
#     std.vector<std.vector<double> > mus;
#     std.vector<std.vector<std.vector<double> > > points;
#     # /* The test inputs*/
#     hyperparams.append([sigma]);
#     mus.append(mu0);
#     points.append( [
#         [0, 0]
#         ]);
#     hyperparams.append([0.2]);
#     mus.append(mu0);
#     points.append( [
#         [0, 0], [0.5, 0.25], [-1, 0.01]
#         ]);
#     hyperparams.append([0.5]);
#     mus.append(mu2);
#     points.append( [
#         [0, 9], [0.9, 10.5]
#         ]);
#     hyperparams.append([4.]);
#     mus.append(mu1);
#     points.append( [
#         [0, 9], [0.9, 10.5], [4.0, 4.01], [3., 2.5], [-0.5, 1.9], [-0.5, 1.9]
#         ]);
#
#
#     double p;
#     double p_from_model_direct;
#     double _zetaValue;
#     std.vector<double> _sValues;
#     std.vector<double> _phiValues;
#     auto e_ptr = korali.Experiment();
#     auto e = *e_ptr;
#     delete e_ptr;
#     auto eng = korali.Engine();
#     korali.Sample* k_ptr;
#     korali.Sample k;
#     std.vector<std.vector<double> > current_points;
#     std.vector<double > mu_vector;
#
#
#
#     for (int i = 0; i < hyperparams.size(); i++)[
#         # /* reference probability */
#         current_points = points[i];
#         sigma = hyperparams[i][0];
#         # * extract mu vectors from hyperparameters
#         mu_vector = mus[i];
#
#         p = 1;
#         for (std.vector<double> pt : current_points)[
#             double p_single = univariate_gaussian_probability(mu_vector, sigma, pt);
#             p *= p_single;
#         ]
#
#         reset_points(distrib1._p, current_points, std.vector<int>(current_points.size(), 0), nClusters );
#
#         # /* Update S, zeta, phi to the set of points (needed?)*/
#         distrib1_S = [&distrib1](korali.Sample& s) -> void [
#     	    distrib1.S(s); ] ;
#         distrib1_zeta = [&distrib1](korali.Sample& s) -> void [
#     	    distrib1.zeta(s); ] ;
#         distrib1_phi = [&distrib1](korali.Sample& s) -> void [
#     	    distrib1.phi(s); ] ;
#
#         # /* Use the distributions S, zeta and phi functions to calculate the probability */
#         k_ptr = korali.Sample();
#         k = *k_ptr;
#         k["Latent Variables"] = mu_vector;
#         k["Hyperparameters"] = hyperparams[i];
#
#
#         distrib1_S(k);
#         distrib1_zeta(k);
#         distrib1_phi(k);
#
#         double _zetaValue = k["zeta"].get<double>();
#         _sValues = k["S"].get<std.vector<double> >();
#         _phiValues = k["phi"].get<std.vector<double> >();
#
#         p_from_model_direct =  std.exp( - _zetaValue
#                                                  + std.inner_product(std.begin(_sValues), std.end(_sValues),
#                                                                                     std.begin(_phiValues), 0.0) );
#
#         assert (std.abs(p - p_from_model_direct) < 0.1*p);
#         delete k_ptr;
#
#     ]
#
#     return 0;
# ]

# # /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */


def test_distribution_2():
  # Initialize the distribution
  distrib2 = ExampleDistribution2()

  nClusters = distrib2._p.nClusters  # 2
  nDimensions = distrib2._p.nDimensions  # 2
  d2_numberLatentVars = distrib2._p.nPoints  # one for each datapoint
  d2_numberHyperparams = distrib2._p.nDimensions * distrib2._p.nClusters + 1

  # Some value pairs:
  sigma = 1.0
  assignments = []
  hyperparams = []
  points = []
  # # /* The test inputs*/
  assignments.append([0])
  hyperparams.append([0, 0, 2, 2, sigma])  # (mu1, mu2, sigma)
  points.append([[0, 0]])
  assignments.append([0, 1])
  hyperparams.append([0, 0, 2, 2, sigma])  # (mu1, mu2, sigma)
  points.append([[2, 2], [0, 0]])
  assignments.append([0])
  hyperparams.append([0, 0, 2, 2, 0.5])  # (mu1, mu2, sigma)
  points.append([[0, 0]])
  assignments.append([1, 1])
  hyperparams.append([0, 0, 2, 2, 0.5])  # (mu1, mu2, sigma)
  points.append([[1.5, 2.25], [-0.5, 2]])
  assignments.append([0, 0, 0, 1, 1, 2])
  hyperparams.append([-1.5, 0, 20., 5., 3.0, 3.5, 7.5])  # (mu1, mu2, sigma)
  points.append([[1.5, -1.5], [-0.5, 2], [
      -5.,
      7.,
  ], [22.0, 10.3], [17.5, 30.], [0.0, 7.2]])

  for i in range(len(assignments)):
    current_points = points[i]
    sigma = hyperparams[i][-1]
    # * extract mu vectors from hyperparameters
    nClusters = int((len(hyperparams[i]) - 1) / nDimensions)
    mu_vectors_concat = hyperparams[i][:-1]
    mu_vectors = np.array(mu_vectors_concat).reshape((nClusters, -1))
    assert mu_vectors.shape[1] == nDimensions

    p = multivariate_gaussian_probability(mu_vectors, nDimensions,
                                          assignments[i], nClusters, sigma,
                                          current_points)

    distrib2._p.reset_points(current_points, assignments[i], nClusters)

    # /* Use the distributions S, zeta and phi functions to calculate the probability */
    k = {}
    k["Latent Variables"] = assignments[i]
    k["Hyperparameters"] = hyperparams[i]

    distrib2.S(k)
    distrib2.zeta(k)
    distrib2.phi(k)

    _zetaValue = k["zeta"]
    _sValues = k["S"]
    _phiValues = k["phi"]

    p_from_model_direct = np.exp(-_zetaValue + np.inner(_sValues, _phiValues))

    assert (np.abs(p - p_from_model_direct) < 0.1 * p)

  return True


if __name__ == '__main__':
  success = test_distribution_2()
  assert success
  print("OK")
