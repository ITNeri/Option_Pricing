# Option_Pricing
American, Asian, European and barrier option pricing based on BSM model or Monte Carlo simulation

## Table of Contents
- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Reference List](#reference-list)
- [Maintainer](#maintainer)
- [License](#license)

## Background  
1. After inputting basic parameters (e.g. k, s, r, sig(vol), dt), this project can give users option price for different types of options. To build the models, I have quoted some theories and formulas, including Black Scholes Option Pricing Model and Monte Carlo Simulations  

2. Now, the following types of options are available:  
(1) American option
(2) Asian option
(3) European option
(4) Barrier option

## Install
Python 3.X should be installed on your machine.

## Usage
Import different files to run the code:  
1. American option:  
(1) BSM Model with Least Squares Monte Carlo:  
   `<from American_option import american_option_lsm>`
            
2. Asian option:  
  (1) Monte Carlo simulation  
  `<from Asian_option import asian_option_mc>`
  
3. European option:   
  (1) BSM Model  
  `<from European_option import black_scholes_model>`  
  (2) Monte Carlo simulation  
  `<from European_option import monte_carlo_simulation>`
  
4. Barrier option:  
  (1)BSM Model  
  `<from barrier_option import bsm_barrier_option>`  
  (2) Monte Carlo simulation  
  `<from barrier_option import mc_barrier_option>`


## Reference list
GlassermanPaul. (2003). Monte Carlo Methods in Financial Engineering. New York: Springer.

Haug, E. G. (2018). The Complete Guide to Option Pricing Formulas (2nd ed.). Shanghai: Mc Graw Hill Education.

Hull, J. (2014). Options, Futures and Other Derivatives (9th ed.). Beijing: China Machine Press

Longstaff, F., Longstaff, F. A., Schwartz, E., & Schwartz, E. S. (2001). Valuing American options by simulation: a simple least-squares approach. Review of Financial Studies,  14(1). https://doi-org.uoelibrary.idm.oclc.org/10.1093/rfs/14.1.113

Xiao, Y.W. (2019). Essentials of Stochastic Calculus for Finance. Shanghai: Fudan University Press.

Zhang, G.P. (2014). Exotic Options: A Guide to Second Generation Options. Beijing: China Machine Press.

## Maintainer
@ITNeri

## License
[MIT](https://github.com/ITNeri/Option_Pricing/blob/main/license.txt)
