//  Pseudorandom numbers from a truncated Gaussian distribution.
//
//  This implements an extension of Chopin's algorithm detailed in
//  N. Chopin, "Fast simulation of truncated Gaussian distributions",
//  Stat Comput (2011) 21:275-288
//  
//  Copyright (C) 2012 Guillaume Dollé, Vincent Mazet
//  (LSIIT, CNRS/Université de Strasbourg)
//  Version 2012-07-04, Contact: vincent.mazet@unistra.fr
//  
//  06/07/2012:
//  - first launch of rtnorm.cpp
//  
//  Licence: GNU General Public License Version 2
//  This program is free software; you can redistribute it and/or modify it
//  under the terms of the GNU General Public License as published by the
//  Free Software Foundation; either version 2 of the License, or (at your
//  option) any later version. This program is distributed in the hope that
//  it will be useful, but WITHOUT ANY WARRANTY; without even the implied
//  warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details. You should have received a
//  copy of the GNU General Public License along with this program; if not,
//  see http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
//  
//  Depends: LibGSL
//  OS: Unix based system


#include <cmath>
#include <iostream>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_sf_erf.h>

#include "rtnorm.hpp"

int N = 4001;   // Index of the right tail

//------------------------------------------------------------
// Pseudorandom numbers from a truncated Gaussian distribution
// The Gaussian has parameters mu (default 0) and sigma (default 1)
// and is truncated on the interval [a,b].
// Returns the random variable x and its probability p(x).
std::pair<double, double> rtnorm(
    gsl_rng *gen,
    double a,
    double b,
    const double mu,
    const double sigma)
{
  // Design variables
  double xmin = -2.00443204036;                 // Left bound
  double xmax =  3.48672170399;                 // Right bound
  int kmin = 5;                                 // if kb-ka < kmin then use a rejection algorithm
  double INVH = 1631.73284006;                  // = 1/h, h being the minimal interval range
  int I0 = 3271;                                // = - floor(x(0)/h)
  double ALPHA = 1.837877066409345;             // = log(2*pi)
  int xsize=sizeof(Rtnorm::x)/sizeof(double);   // Length of table x
  int stop = false;
  double sq2 = 7.071067811865475e-1;            // = 1/sqrt(2)
  double sqpi = 1.772453850905516;              // = sqrt(pi)

  double r, z, e, ylk, simy, lbound, u, d, sim, Z, p;
  int i, ka, kb, k;
  
  // Scaling
  if(mu!=0 || sigma!=1)
  {
    a=(a-mu)/sigma;
    b=(b-mu)/sigma;
  }
  
  //-----------------------------
  
  // Check if a < b
  if(a>=b)
  {
    std::cerr<<"*** B must be greater than A ! ***"<<std::endl;
    exit(1);
  }

  // Check if |a| < |b|
  else if(fabs(a)>fabs(b))
    r = -rtnorm(gen,-b,-a).first;  // Pair (r,p)

  // If a in the right tail (a > xmax), use rejection algorithm with a truncated exponential proposal  
  else if(a>xmax)
    r = rtexp(gen,a,b);

  // If a in the left tail (a < xmin), use rejection algorithm with a Gaussian proposal
  else if(a<xmin)
  {
    while(!stop)
    {
      r = gsl_ran_gaussian(gen,1);
      stop = (r>=a) && (r<=b);
    }
  }

  // In other cases (xmin < a < xmax), use Chopin's algorithm
  else
  {
    // Compute ka
    i = I0 + floor(a*INVH);
    ka = Rtnorm::ncell[i];

    // Compute kb
    (b>=xmax) ?
    kb = N :
    (
      i = I0 + floor(b*INVH),
      kb = Rtnorm::ncell[i]
    );

    // If |b-a| is small, use rejection algorithm with a truncated exponential proposal
    if(abs(kb-ka) < kmin)
    {
      r = rtexp(gen,a,b);
      stop = true;  
    }
    
    while(!stop)
    {
      // Sample integer between ka and kb
      k = floor(gsl_rng_uniform(gen) * (kb-ka+1)) + ka;
    
      if(k == N)
      {    
        // Right tail
        lbound = Rtnorm::x[xsize-1];
        z = -log(gsl_rng_uniform(gen));
        e = -log(gsl_rng_uniform(gen));
        z = z / lbound;

        if ((pow(z,2) <= 2*e) && (z < b-lbound))
        {
          // Accept this proposition, otherwise reject
          r = lbound + z;
          stop = true;
        }
      }

      else if ((k <= ka+1) || (k>=kb-1 && b<xmax))
      {
          
        // Two leftmost and rightmost regions
        sim = Rtnorm::x[k] + (Rtnorm::x[k+1]-Rtnorm::x[k]) * gsl_rng_uniform(gen);

        if ((sim >= a) && (sim <= b))
        {
          // Accept this proposition, otherwise reject
          simy = Rtnorm::yu[k]*gsl_rng_uniform(gen);
          if ( (simy<yl(k)) || (sim * sim + 2*log(simy) + ALPHA) < 0 )
          {
            r = sim;
            stop = true;
          }
        }        
      }

      else // All the other boxes
      {    
        u = gsl_rng_uniform(gen);
        simy = Rtnorm::yu[k] * u;
        d = Rtnorm::x[k+1] - Rtnorm::x[k];
        ylk = yl(k);
        if(simy < ylk)  // That's what happens most of the time 
        {  
          r = Rtnorm::x[k] + u*d*Rtnorm::yu[k]/ylk;  
          stop = true;
        }
        else
        {
          sim = Rtnorm::x[k] + d * gsl_rng_uniform(gen);

          // Otherwise, check you're below the pdf curve
          if((sim * sim + 2*log(simy) + ALPHA) < 0)
          {
            r = sim;
            stop = true;
          }
        }
        
      }
    }  
  }
  
  //-----------------------------

  // Scaling
  if(mu!=0 || sigma!=1)
    r = r*sigma + mu;
  
  // Compute the probability
  Z = sqpi *sq2 * sigma * ( gsl_sf_erf(b*sq2) - gsl_sf_erf(a*sq2) );
  p = exp(-pow((r-mu)/sigma,2)/2) / Z; 

  return std::pair<double,double>(r,p);  
}

//------------------------------------------------------------
// Compute y_l from y_k
double yl(int k)
{
  double yl0 = 0.053513975472;                  // y_l of the leftmost rectangle
  double ylN = 0.000914116389555;               // y_l of the rightmost rectangle
  
  if (k == 0)
    return yl0;
    
  else if(k == N-1)
    return ylN;
          
  else if(k <= 1953)
    return Rtnorm::yu[k-1];
          
  else
    return Rtnorm::yu[k+1];
}

//------------------------------------------------------------
// Rejection algorithm with a truncated exponential proposal
double rtexp(gsl_rng *gen, double a, double b)
{
  int stop = false;
  double twoasq = 2*pow(a,2);
  double expab = exp(-a*(b-a)) - 1;
  double z, e;

  while(!stop)
  {
    z = log(1 + gsl_rng_uniform(gen)*expab);
    e = -log(gsl_rng_uniform(gen));
    stop = (twoasq*e > pow(z,2));
  }
  return a - z/a;
}

