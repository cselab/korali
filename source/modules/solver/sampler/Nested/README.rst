***************
Nested Sampling
***************

This is an implementation of the *Nested Sampling* by John Skilling,
as published in `https://projecteuclid.org/euclid.ba/1340370944`.

The implementation of the *Multi Ellipse* proposal distribution is based on
the work of Feroz et. al. `https://academic.oup.com/mnras/article/398/4/1601/981502`.

Our version of the Multi Nest algorithm includes two changes that significantly
improved the efficiency of the algorithm:

    - to cluster the samples we only use k-means clustering without reassigning
      the samples based on the weighted Mahalanobis distance.

    - the initial means of the k-means are set at the endpoints of the main-axes
      of the ellipsoid. the main-axes are chosen randomly, proportional to their
      length (eigen values)

    - ellispoids bounding cluster of samples less than the number of variables 
      plus one are initiated without covariances instead of rejecting them
