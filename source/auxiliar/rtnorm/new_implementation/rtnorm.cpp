//  Pseudorandom numbers from a truncated Gaussian distribution.
//
//  This implements an extension of Chopin's algorithm detailed in
//  N. Chopin, "Fast simulation of truncated Gaussian distributions",
//  Stat Comput (2011) 21:275-288
//  
//  Copyright (C) 2015 Jonas Wallin
//  Copyright (C) 2012 Guillaume Dollé, Vincent Mazet
//  (LSIIT, CNRS/Université de Strasbourg)
//  Version 2012-07-04, Contact: vincent.mazet@unistra.fr
//  
//	25/10/2015:
//	- Updated using c++11 and created a class (Jonas Wallin)
//  06/07/2012:
//  - first launch of rtnorm.cpp (Guillaume Dollé, Vincent Mazet)
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
//  Depends: c++11
//  OS: Unix based system


#include <cmath>
#include <iostream>
#include <chrono>
#include "rtnorm.hpp"

#ifdef _OPENMP
#include<omp.h>
#endif

using namespace Rtnorm;
//------------------------------------------------------------
// Rejection algorithm with a truncated exponential proposal
double rtexp(std::mt19937_64 *gen_,std::uniform_real_distribution<double> *U01 , double a, double b)
{
  int stop = false;
  double twoasq = 2*pow(a,2);
  double expab = exp(-a*(b-a)) - 1;
  double z, e;

  while(!stop)
  {
    z = log(1 + (*U01)(*gen_)*expab);
    e = -log((*U01)(*gen_));
    stop = (twoasq*e > pow(z,2));
  }
  return a - z/a;
}

double rtnorm::sample(double a, double b, double mu, double sigma)
{
	double r;
	int stop = false;
	if(mu!=0 || sigma!=1)
  	{
    	a=(a-mu)/sigma;
    	b=(b-mu)/sigma;
  	}
  
 
  	if(fabs(a)>fabs(b)){
    	r = -sample(-b,-a);  

  	// If a in the right tail (a > xmax), use rejection algorithm with a truncated exponential proposal  
  	}else if(a>xmax){
    	r = sample_exp(a, b);
    	
    	
    	
    // Sample using regular Normal
	}else if(a<xmin)
  	{
    	while(!stop)
    	{
      		r = N01(rgen);
      		stop = (r>=a) && (r<=b);
    	}
  	}else 	// Chopin' algorithm
		r = sample_xmin_xmax(a, b);
	
	
	
	if(mu!=0 || sigma!=1)
    	r = r*sigma + mu;
	return r;
}

double rtnorm::sample_exp(double a, double b)
{
  int stop = false;
  double twoasq = 2*pow(a,2);
  double expab = exp(-a*(b-a)) - 1;
  double z, e;

  while(!stop)
  {
    z = log(1 + U01( rgen) * expab);
    e = -log( U01( rgen));
    stop = ( twoasq * e > pow(z,2) );
  }
  return a - z/a;
}


double rtnorm::sample_xmin_xmax(double a, double b)
{
	int stop = false;
	double r;

    // Compute ka
    i = I0 + floor(a * INVH);
    ka = Rtnorm::ncell[i];

    // Compute kb
    (b>=xmax) ?
    kb = Ntail :
    (
      i = I0 + floor(b * INVH),
      kb = Rtnorm::ncell[i]
    );

    // If |b-a| is small, use rejection algorithm with a truncated exponential proposal
    if(abs(kb-ka) < kmin)
    {
      r = sample_exp(a, b);
      stop = true;  
    }
    
    while(!stop)
    {
      // Sample integer between ka and kb
      k = floor( U01(rgen) * (kb - ka + 1 ) ) + ka;
    
      if(k == Ntail)
      {    
        // Right tail
        lbound = Rtnorm::x[xsize-1];
        z = -log( U01( rgen));
        e = -log( U01( rgen));
        z = z / lbound;

        if ( (pow(z,2) <= 2*e ) && (z < b - lbound))
        {
          // Accept this proposition, otherwise reject
          r = lbound + z;
          stop = true;
        }
      }

      else if ((k <= ka+1) || (k>=kb-1 && b<xmax))
      {
          
        // Two leftmost and rightmost regions
        sim = Rtnorm::x[k] + ( Rtnorm::x[k+1] - Rtnorm::x[k]) * U01(rgen);

        if ((sim >= a) && (sim <= b))
        {
          // Accept this proposition, otherwise reject
          simy = Rtnorm::yu[k] * U01(rgen);
          if ( (simy<yl(k)) || ( sim * sim + 2*log(simy) + ALPHA) < 0 )
          {
            r = sim;
            stop = true;
          }
        }        
      }

      else // All the other boxes
      {    
        u = U01(rgen);
        simy = Rtnorm::yu[k] * u;
        d = Rtnorm::x[k+1] - Rtnorm::x[k];
        ylk = yl(k);
        if(simy < ylk)  // That's what happens most of the time 
        {  
          r = Rtnorm::x[k] + u*d*Rtnorm::yu[k] / ylk;  
          stop = true;
        }
        else
        {
          sim = Rtnorm::x[k] + d * U01(rgen);

          // Otherwise, check you're below the pdf curve
          if((sim * sim + 2*log(simy) + ALPHA) < 0)
          {
            r = sim;
            stop = true;
          }
        }
        
      }
    }  
  

	return r;
}






#include <time.h>


void rtnorm_multi::sample(const int n, 
						  double* x, 
						  const double* a, 
						  const double* b, 
						  const double* mu, 
						  const double* sigma)
{


	int i;
	if(n > 5000){
	#pragma omp parallel for private(i)
	for(i=0; i<n; ++i){
		#ifdef _OPENMP
    		int cur_thread = omp_get_thread_num();
		#else
    		int cur_thread = 0;
		#endif
    	x[i] = rtnormstream[cur_thread].sample(a[i], 
    										   b[i], 
    										   mu[i],
    										   sigma[i]);
    }
    
    }
    else{
    
    		for(i=0; i<n; ++i){
				x[i] = rtnormstream[0].sample(a[i], 
    										   b[i], 
    										   mu[i],
    										   sigma[i]);
    		}
    										   
    	}
    
    
    
    

}



rtnorm_multi::rtnorm_multi(int NthreadsIn , uint_fast64_t seedIn )
{
	Nthreads = NthreadsIn;
	seed = seedIn;
	startup(true);
};


void rtnorm_multi::startup(int debug)
{
	#ifdef _OPENMP
   		int Max_Nthreads = omp_get_max_threads();
   		
   		if( Nthreads <= 0)
   			Nthreads = Max_Nthreads;
   		else
   			Nthreads = std::min(Nthreads, Max_Nthreads);
	#else
  			Nthreads = 1;
	#endif
	
	
	std::mt19937_64 rgen(seed);
	
	rtnormstream.reserve(Nthreads);
	
	
	for(int i=0; i<Nthreads; ++i){
    if(debug){
      rtnormstream.push_back( rtnorm(seed) );
    }else{
      rtnormstream.push_back( rtnorm( static_cast<uint_fast64_t>(rgen()) ) );
    }
  }
}

rtnorm_multi::rtnorm_multi(int NthreadsIn)
{

	Nthreads = NthreadsIn;

	using namespace std::chrono;
    auto Depoch_ns = duration_cast<nanoseconds>
      ( high_resolution_clock::now().time_since_epoch() );
    //use nanoseconds since epoch as seed
    seed = static_cast<uint_fast64_t>( Depoch_ns.count() );
    startup();
}

double rtnorm::yl(int k)
{
  if (k == 0)
    return yl0;
    
  else if(k == Ntail-1)
    return ylN;
          
  else if(k <= 1953)
    return Rtnorm::yu[k-1];
          
  else
    return Rtnorm::yu[k+1];
}

