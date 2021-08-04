#-*-conding:utf-8-*-

from math import exp, sqrt
import random
import numpy as np

'''
Parameters:
s0 = initial stock price
k = strike price
r = risk-less short rate
sig = volatility of stock value
dt = t/T = time to maturity
m = the number of path nodes
n = the number of simulation
'''


def asian_option_mc(s0, k, r, dt, sig, m, n):
    # It is an arithmetic solution by using Monte Carlo method
    delta_t = dt / m  # length of time interval
    c = []
    p = []
    for i in range(0, n):
        s = [s0]
        for j in range(0, m):
            s.append(s[-1] * exp((r - 0.5 * sig ** 2) * delta_t + (sig * sqrt(delta_t) * random.gauss(0, 1))))

        avg = np.mean(s)
        c.append(max((avg - k), 0))
        p.append(max((k - avg), 0))

    c_value = np.mean(c) * exp(-r * dt)
    c_standard_error = np.std(c) / np.sqrt(n)

    p_value = np.mean(p) * exp(-r * dt)
    p_standard_error = np.std(p) / np.sqrt(n)

    return {'call_MC': c_value, 'standard error(c)': c_standard_error, 'put_MC': p_value,
            'standard error(p)': p_standard_error}


'''
trial:
print(asian_option_mc(5200, 5200, 0.03, 1, 0.25, 100, 20000))
'''
