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


#ifndef __RTNORNM_HPP
#define __RTNORNM_HPP

#include <vector>
#include <random>
#include "rtnorm_constants.hpp"




namespace Rtnorm{
//------------------------------------------------------------
// Class for Pseudorandom numbers from a truncated Gaussian distribution
// rntorm.sample()->
// The Gaussian has parameters mu (default 0) and sigma (default 1)
// and is truncated on the interval [a,b].
// 

double qnorm5(double p, double mu, double sigma, int lower_tail, int log_p);
class rtnorm{
private:
	//------------------------------------------------------------
	// CONSTANTS:::
	//------------------------------------------------------------
  double xmin = -2.00443204036;                 // Left bound
  double xmax =  3.48672170399;                 // Right bound
  int kmin = 5;                                 // if kb-ka < kmin then use a rejection algorithm
  double INVH = 1631.73284006;                  // = 1/h, h being the minimal interval range
  int I0 = 3271;                                // = - floor(x(0)/h)
  double ALPHA = 1.837877066409345;             // = log(2*pi)
  int xsize=sizeof(Rtnorm::x)/sizeof(double);   // Length of table x
  double sq2 = 7.071067811865475e-1;            // = 1/sqrt(2)
  double sqpi = 1.772453850905516;              // = sqrt(pi)

  double  z, e, ylk, simy, lbound, u, d, sim, p;
  int i, ka, kb, k;
  
  
  
  
  int Ntail = 4001;   // Index of the right tail
  double yl0 = 0.053513975472;                  // y_l of the leftmost rectangle
  double ylN = 0.000914116389555;               // y_l of the rightmost rectangle

	//------------------------------------------------------------
	// RANDOM NUMBER GENERATORS
	//------------------------------------------------------------
  //A random-generator
  std::mt19937_64 rgen;  
  //A U(0,1)-distribution
  std::uniform_real_distribution<double> U01;
  //A UN0,1)-distribution
  std::normal_distribution<double>       N01;


	/*
		Internal function used in Chopin's algorithm
	
	*/
	double yl(int );

public:
	// init
	rtnorm() : rgen(), U01(0.0, 1.0), N01(0.0, 1.0){};
	explicit rtnorm(uint_fast64_t seed) : rgen(seed), U01(0.0, 1.0), N01(0.0, 1.0) {};
	
	
	/*
		Generates a sample from truncated Normal
		@param a      left limit
		@param b      right limit
		@param mu     mean
		@param sigma  standrad deviation
		@out returns a sample from tN(a,b,mu,sigma)
	*/ 
	double sample(double a, double b, double mu = 0., double sigma = 1.);
	
	/*
		Generates a sample from truncated Normal (0,1) using 
		rejection with expontial random variable
		@param a      left limit
		@param b      right limit
		@out returns a sample from tN(a,b,0,1)
	*/ 
	double sample_exp(double a, double b);
	
	/*
		Generates a sample from truncated Normal (0,1) using 
		Chopin's algorithm
		@param a      left limit (xmin < a < xmax)
		@param b      right limit
		@out returns a sample from tN(a,b,0,1)
	*/ 
	double sample_xmin_xmax(double a, double b);

  
};

//------------------------------------------------------------
// Wrapper class for rtnorm used for openmp support
// 
class rtnorm_multi{

	private:
		std::vector<rtnorm> rtnormstream; // vector containing rtnorms


		// internal function called with startup
		void startup(int debug = false);

	public:
		// init
		rtnorm_multi(int NthreadsIn = -1);
		// init debug
		rtnorm_multi(int NthreadsIn , uint_fast64_t seedIn );
		
	/*
		Generates a sample from truncated Normal
		@param n      length of of the vectors
		@param x      output
		@param a      vector of left limit
		@param b      vector of right limit
		@param mu     vector of mean
		@param sigma  vector of standrad deviation
		@out returns vector of sample from tN(a,b,mu,sigma)
	*/ 		
		void sample(const int n, 
					double *x, 
					const double* a, 
					const double* b, 
					const double* mu, 
					const double* sigma);
		
		uint_fast64_t seed;
		int Nthreads;
		
};
}
#endif //__RTNORNM_HPP
