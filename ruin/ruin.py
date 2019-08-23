"""
A simple simulation of risk-taking in a domain where risk premiums come with a
proportional chance of ruin. Based on the real world challenge of trading firms choosing
cryptocurrency exchanges to trade on.

We have a set of traders, T, and a set of exchanges E. Traders are given N 'bets' to
represent trading capital, and allocate these between between exchanges. Traders may
allocate multiple (or all) bets on a single exchange. Exchanges give returns at each
step of the simulation, and each exchange has unique return characteristics determined
by a single parameter 'z'. At a low z, exchanges give high returns, but there is also a
high chance that they will "explode" with a complete loss of funds to their traders. As
z increases, both ruin risk and the excess returns decrease exponentially.
"""

from collections import defaultdict

from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import colormaps


NEGATIVE_INFINITY = -10000

NUM_STEPS = 2600
NUM_EXCHANGES = 8
BETS_PER_TRADER = 2
BET_SIZE = 1.0 / BETS_PER_TRADER
NUM_TRADERS = NUM_EXCHANGES * BETS_PER_TRADER

MAX_RISK = 30  # The riskiest exchange has a 1 in (MAX_RISK ^ RUIN_DECAY) ruin risk.
RUIN_DECAY = 2  # Exponent by which ruin risk decreases as z increases.
PREMIUM_DECAY = 2.6  # Exponent by which the risk premium decreases as z increases.
MAX_PREMIUM = 0.0009  # Maximum risk premium.

# Default return characteristics for each tick.
RETURN_MEAN = 0
RETURN_STD = 0.007


class Exchange(object):
    def __init__(self, z):
        self.z = z
        self.traders = []  # Trader to notify of a new payoff.
        self.is_dead = False
        rank = (float(self.z) - MAX_RISK) / (NUM_EXCHANGES - 1)
        scale = (1 - rank) ** PREMIUM_DECAY
        self.premium = scale * MAX_PREMIUM

    def register_trader(self, t):
        self.traders.append(t)

    def tick(self, tick_num):
        if self.is_dead:
            payoff = 0.0
        elif np.random.randint(0, self.z ** RUIN_DECAY) == 0:
            payoff = NEGATIVE_INFINITY
            self.is_dead = True
        else:
            payoff = np.random.normal(
                RETURN_MEAN + self.premium,
                RETURN_STD,
            )

        for t in self.traders:
            t.receive_payoff(self.z, payoff, tick_num)
    

class Trader(object):
    def __init__(self, trader_id, exchanges):
        self.trader_id = trader_id
        self.exchanges = exchanges
        self.account_balance = defaultdict(lambda: 0.0)
        self.account_series = defaultdict(lambda: np.array([]))
        self.tick = 0

        for e in self.exchanges:
            self.account_balance[e.z] += BET_SIZE

        for z, initial_balance in self.account_balance.items():
            self.account_series[z] = np.array(initial_balance)

        for e in self.exchanges:
            e.register_trader(self)

    def receive_payoff(self, z, payoff, tick):
        if tick > self.tick:
            self.record_balances(self.tick)
            self.tick = tick

        self.account_balance[z] += payoff

    def record_balances(self, tick):
        for z in set([e.z for e in self.exchanges]):
            if self.account_balance[z] < 0:
                self.account_balance[z] = 0.0

            self.account_series[z] = np.append(
                self.account_series[z],
                [self.account_balance[z]],
            )

    @property
    def returns(self):
        return sum([v for k,v in self.account_series.items()])

 
def contiguous_sublists_size_n(l, n):
    return [l[i: i + n] for i in range(0, len(l) - (n - 1))]


def add_colorbar(colormap):
    sm = plt.cm.ScalarMappable(cmap=colormap, norm=plt.Normalize(vmin=0, vmax=1))
    sm._A = []
    cb = plt.colorbar(sm)
    #cb.ax.set_yticks([0, 0.5, 1])
    #cb.ax.set_yticklabels(['-1', '0', '1'])
    cb.set_ticks([0, 1])
    cb.set_ticklabels(['High', 'Low'])
    cb.set_label('Risk', rotation=0)


def plot_all_returns(traders):
    pd.options.display.mpl_style = 'default'
    df = pd.DataFrame([t.returns for t in traders]).transpose()
    df.plot(linewidth=5, colormap=colormaps.plasma, figsize=(12, 6))
    plt.legend().remove()
    add_colorbar(colormaps.plasma)


def pretty_plot():
    plt.xlabel('Time', fontsize=20, labelpad=10, position=(0.5,0.5))
    plt.ylabel('Returns', position=(1,1), rotation=0, fontsize=20, labelpad=-5)

def generate_exchanges():
    return [Exchange(z + MAX_RISK) for z in range(0, NUM_EXCHANGES)]


def generate_traders(exchanges):
    exchanges_perm = []
    for e in exchanges:
        for i in range(BETS_PER_TRADER):
            exchanges_perm.append(e)

    exchange_sets = contiguous_sublists_size_n(exchanges_perm, BETS_PER_TRADER)

    traders = [Trader(i, exchange_sets[i]) for i in range(len(exchange_sets))]

    return traders


def run_simulation(exchanges, steps):
    for i in range(0, steps):
        for exchange in exchanges:
            exchange.tick(i)

    return exchanges


def main():
    exchanges = generate_exchanges()
    traders = generate_traders(exchanges)

    run_simulation(exchanges, NUM_STEPS)

    plot_all_returns(traders)

    return traders, exchanges


if __name__ == '__main__':
    main()
