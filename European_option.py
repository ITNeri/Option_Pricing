import numpy as np
from math import exp, sqrt, log
import random
from scipy.stats.distributions import norm

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


def black_scholes_model(s0, k, r, sig, dt):
    d1 = (log(s0 / k) + (r + sig ** 2 / 2) * dt) / (sig * sqrt(dt))
    d2 = d1 - sig * sqrt(dt)
    call_bs = s0 * exp(-r * dt) * norm.cdf(d1) - k * exp(-r * dt) * norm.cdf(d2)
    put_bs = k * exp(-r * dt) * norm.cdf(-d2) - s0 * exp(-r * dt) * norm.cdf(-d1)
    return {'call_BS': call_bs, 'put_BS': put_bs}


def monte_carlo_simulation(s0, k, r, sig, dt, m, n):
    list_1 = []  # call option value list
    list_2 = []  # put option value list
    delta_t = dt / m  # length of time interval

    for i in range(0, n):
        path = [s0]
        for j in range(0, m):
            path.append(path[-1] * exp((r - 0.5 * sig ** 2) * delta_t + (sig * sqrt(delta_t) * random.gauss(0, 1))))

        put_value = max(k - path[-1], 0)
        call_value = max(path[-1] - k, 0)
        list_2.append(put_value)
        list_1.append(call_value)
    p = np.average(list_2)
    c = np.average(list_1)
    return {'call_MC': c, 'put_MC': p}


'''
trial:
a = black_scholes_model(5200, 5200, 0.03, 0.25, 0.08)
b = monte_carlo_simulation(5200, 5200, 0.03, 0.25, 0.08, 20, 2000000)

print(a)
print(b)
'''