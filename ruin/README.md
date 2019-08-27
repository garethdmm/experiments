Ruin Simulation
---------------

Companion code to the blogpost: ["How we survived 5 years in the most dangerous market in the world"](https://medium.com/@garethmacleod/how-we-survived-5-years-in-the-most-dangerous-market-in-the-world-c1404e0ab5b9)

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

An example with the default settings. 8 exchanges, 2 bets per trader.

![alttext](img/8-2.png)

If we increase the number of exchanges and traders, and increase the premium decay.

![alttext](img/20-3-high-premium-decay.png)

You can experiment yourself to see who wins by tweaking the parameters. Aside from the number of exchanges and bets-per-trader, the most important are `RUIN_DECAY` and `PREMIUM_DECAY`, which determine how quickly the exchanges get safer, and how quickly their hazard premium decreases from the most risky to least risky. You can also tweak the `MAX_PREMIUM`, `MAX_RISK`, and `NUM_STEPS` for interesting results.

There are a few improvements I'd like to make:
* The parameters so far have been chosen fairly arbitrarily. It would be great to do work to set them according to some historical data, such as the number of crypto exchanges that really were created 2012-2019, the number of them that blew up, and reasonable guesses for return characteristics in each tick.
* We should try letting Traders pick their bets randomly, this would show less correlation between their returns. Although arguably, traders returns *are* correlated.
