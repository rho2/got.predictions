#!/usr/bin/python

import sys
sys.path.append(r"C:\cygwin64\bin")

from matplotlib import pyplot as plt
import numpy as np
import pymc3 as pm
from pymc3.distributions.timeseries import GaussianRandomWalk
import seaborn as sns
import pandas as pd
from theano import tensor as T
import theano
theano.config.cxx = ""
theano.config.cxx


df = pd.read_csv(pm.get_data('mastectomy.csv'))
df.event = df.event.astype(np.int64)
df.metastized = (df.metastized == 'yes').astype(np.int64)
n_patients = df.shape[0]
patients = np.arange(n_patients)

fig, ax = plt.subplots(figsize=(8, 6))

blue, _, red = sns.color_palette()[:3]

ax.hlines(patients[df.event.values == 0], 0, df[df.event.values == 0].time,
          color=blue, label='Censored')

ax.hlines(patients[df.event.values == 1], 0, df[df.event.values == 1].time,
          color=red, label='Uncensored')

ax.scatter(df[df.metastized.values == 1].time, patients[df.metastized.values == 1],
           color='k', zorder=10, label='Metastized')

ax.set_xlim(left=0)
ax.set_xlabel('Months since mastectomy')

ax.set_ylim(-0.25, n_patients + 0.25)

ax.legend(loc='center right')

interval_length = 3
interval_bounds = np.arange(
    0, df.time.max() + interval_length + 1, interval_length)
n_intervals = interval_bounds.size - 1
intervals = np.arange(n_intervals)

fig, ax = plt.subplots(figsize=(8, 6))

ax.hist(df[df.event == 1].time.values, bins=interval_bounds,
        color=red, alpha=0.5, lw=0,
        label='Uncensored')
ax.hist(df[df.event == 0].time.values, bins=interval_bounds,
        color=blue, alpha=0.5, lw=0,
        label='Censored')

ax.set_xlim(0, interval_bounds[-1])
ax.set_xlabel('Months since mastectomy')

ax.set_yticks([0, 1, 2, 3])
ax.set_ylabel('Number of observations')

ax.legend()

last_period = np.floor(((100 * df.time) - 1) / interval_length / 100)
# needed because np.floor creates float64
last_period = last_period.astype(int)
death = np.zeros((n_patients, n_intervals))
death[patients, last_period] = df.event

exposure = np.greater_equal.outer(
    df.time, interval_bounds[:-1]) * interval_length
exposure[patients, last_period] = df.time - interval_bounds[last_period]

SEED = 5078864  # from random.org

with pm.Model() as model:
    lambda0 = pm.Gamma('lambda0', 0.01, 0.01, shape=n_intervals)

    sigma = pm.Uniform('sigma', 0., 10.)
    tau = pm.Deterministic('tau', sigma**-2)
    mu_beta = pm.Normal('mu_beta', 0., 10**-2)
    beta = pm.Normal('beta', mu_beta, tau)

    lambda_ = pm.Deterministic('lambda_', T.outer(
        T.exp(beta * df.metastized), lambda0))
    mu = pm.Deterministic('mu', exposure * lambda_)

    obs = pm.Poisson('obs', mu, observed=death)

n_samples = 400
burn = 2000
thin = 20

with model:
    step = pm.Metropolis()
    trace_ = pm.sample(n_samples, step, random_seed=SEED)


np.exp(trace_['beta'].mean())

pm.plot_posterior(trace_, varnames=['beta'], color='#87ceeb')

pm.autocorrplot(trace_, varnames=['beta'])

base_hazard = trace_['lambda0']
met_hazard = trace_['lambda0'] * np.exp(np.atleast_2d(trace_['beta']).T)


def cum_hazard(hazard):
    return (interval_length * hazard).cumsum(axis=-1)


def survival(hazard):
    return np.exp(-cum_hazard(hazard))


def plot_with_hpd(x, hazard, f, ax, color=None, label=None, alpha=0.05):
    mean = f(hazard.mean(axis=0))

    percentiles = 100 * np.array([alpha / 2., 1. - alpha / 2.])
    hpd = np.percentile(f(hazard), percentiles, axis=0)

    ax.fill_between(x, hpd[0], hpd[1], color=color, alpha=0.25)
    ax.step(x, mean, color=color, label=label)


# In[27]:


fig, (hazard_ax, surv_ax) = plt.subplots(
    ncols=2, sharex=True, sharey=False, figsize=(16, 6))

plot_with_hpd(interval_bounds[:-1], base_hazard, cum_hazard,
              hazard_ax, color=blue, label='Had not metastized')
plot_with_hpd(interval_bounds[:-1], met_hazard, cum_hazard,
              hazard_ax, color=red, label='Metastized')

hazard_ax.set_xlim(0, df.time.max())
hazard_ax.set_xlabel('Months since mastectomy')

hazard_ax.set_ylabel(r'Cumulative hazard $\Lambda(t)$')

hazard_ax.legend(loc=2)

plot_with_hpd(interval_bounds[:-1], base_hazard, survival,
              surv_ax, color=blue)
plot_with_hpd(interval_bounds[:-1], met_hazard, survival,
              surv_ax, color=red)

surv_ax.set_xlim(0, df.time.max())
surv_ax.set_xlabel('Months since mastectomy')

surv_ax.set_ylabel('Survival function $S(t)$')

fig.suptitle('Bayesian survival model')
