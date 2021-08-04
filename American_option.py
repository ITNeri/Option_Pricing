#-*-conding:utf-8-*-

from math import exp, sqrt
import numpy as np
import random
import pandas as pd
import statsmodels.api as sm


'''
Parameters:
payoff: "c"(call) or "p"(put)
s0 = initial stock price
k = strike price
r = risk-less short rate
dt = t/T = time to maturity
sig = volatility of stock value
m = the number of path nodes
n = the number of simulation
'''


def american_option_lsm(payoff, s0, k, r, dt, sig, m, n):
    
    # ===========================================================================================
    # BSM Model with Least Squares Monte Carlo
    # Reference article: Valuing American Options by Simulation: A Simple Least-Squares Approach
    # ===========================================================================================

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    delta_t = dt / m  # length of time interval

    # stock price path
    s = pd.DataFrame(np.zeros(n) + s0)  # first column = initial stock price; total rows = n

    for i in range(0, n):
        for j in range(0, m):
            s.loc[i, (j + 1)] = s.loc[i, j] * np.exp(
                (r - 0.5 * sig ** 2) * delta_t + (sig * sqrt(delta_t) * random.gauss(0, 1)))

    s.columns = list(range(m + 1))  # set column's title (time)
    s.index = s.index + 1  # rows start at 1

    if payoff == "c":
        s['payoff'] = s[m] - k  # it refers to payoff at maturity
        s['payoff'] = s['payoff'].apply(lambda x: max(x, 0))  # payoff(call) = max(s-k,0) = intrinsic_value
    else:
        s['payoff'] = k - s[m]
        s['payoff'] = s['payoff'].apply(lambda x: max(x, 0))  # payoff(put) = max(k-s,0) = intrinsic_value

    s['value_at_maturity'] = s['payoff']  # last day cash flow
    s['optional_execution_time'] = m

    # regression
    discount_factor = exp(-r * delta_t)

    for g in range(m - 1, 1, -1):
        x_regression = []
        y_regression = []
        x_list = s[g].tolist()
        y_prepare = s['value_at_maturity'].tolist()
        optional_time_list = s['optional_execution_time'].tolist()

        # function: least squares fitting
        for z in range(0, n):
            if y_prepare[z] > 0:
                x_regression.append(x_list[z])
                factors = (m + 1) - optional_time_list[z]  # discount times
                y_regression.append(y_prepare[z] * discount_factor ** factors)
        x_regression_2 = [h ** 2 for h in x_regression]
        df = pd.DataFrame({"x1": x_regression, "x2": x_regression_2, "y": y_regression})
        x_total = df[['x1', 'x2']]
        y_total = df['y']
        x_total = sm.add_constant(x_total)
        model = sm.OLS(y_total, x_total).fit()

        # E[Y|X]=c+bx+ax^2
        parameters = model.params
        c = parameters['const']
        b = parameters['x1']
        a = parameters['x2']

        # determine continuation and exercise value
        trial_table = pd.DataFrame(np.zeros(n) + s[g])
        trial_table['x^2'] = trial_table.iloc[:, 0] * trial_table.iloc[:, 0]
        trial_table['continuation'] = a * trial_table['x^2'] + b * trial_table.iloc[:, 0] + c

        if payoff == "c":
            trial_table['exercise'] = s[g] - k
            trial_table['exercise'] = trial_table['exercise'].apply(lambda x: max(x, 0))
        else:
            trial_table['exercise'] = k - s[g]
            trial_table['exercise'] = trial_table['exercise'].apply(lambda x: max(x, 0))

        continuation_list = trial_table['continuation'].tolist()
        exercise_list = trial_table['exercise'].tolist()

        # compare continuation and exercise value
        for w in range(0, n):
            if y_prepare[w] > 0 and continuation_list[w] < exercise_list[w]:
                optional_time_list[w] = optional_time_list[w] - 1

        # update optional execution time
        s.drop(columns=['optional_execution_time'])
        s['optional_execution_time'] = optional_time_list

    # delete usefulness rows
    s_new = s[s['value_at_maturity'] > 0]

    # determine American option price -- output
    optional_time_list_new = s_new['optional_execution_time'].tolist()
    value_total = 0
    total_row_new = s_new.shape[0]

    for q in range(0, total_row_new):
        if payoff == "c":
            optional_step = optional_time_list_new[q]
            value = (s_new.iloc[[q], [optional_step]].values[0][0] - k) * discount_factor ** optional_step
            value_total = value_total + value
        else:
            optional_step = optional_time_list_new[q]
            value = (k - s_new.iloc[[q], [optional_step]].values[0][0]) * discount_factor ** optional_step
            value_total = value_total + value
   
    option_value = value_total / total_row_new

    return option_value, s_new
