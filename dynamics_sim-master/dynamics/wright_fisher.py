__author__ = 'eblubin@mit.edu'
import numpy as np
from dynamics.dynamics import DynamicsSimulator
from itertools import chain


class WrightFisher(DynamicsSimulator):
    def __init__(self, mu=0.05, *args, **kwargs):
        # TODO don't allow pop_size of 0, wright fisher only works with finite pop size
        super(WrightFisher, self).__init__(*args,stochastic=True,**kwargs)
        self.mu = mu

    def next_generation(self, previous_state, group_selection, rate):
        next_state = []
        number_groups=len(previous_state)
        fitness = []
        for i in range(len(previous_state)):
            fitness.append(self.calculate_fitnesses(previous_state[i]))
            
        # Wright-Fisher between groups           
        if group_selection and np.random.uniform(0,1)<rate:
            avg_payoffs=[]
            for k in range(number_groups):
                avg_payoffs.append(sum(chain(*fitness[k]))/sum(sum(chain(*fitness[j])) for j in range(number_groups)))
                
            # Groups reproduce proportional to their fitness
            new_group_distribution = np.random.multinomial(number_groups,avg_payoffs)
                
            # Update the new distribution of groups
            for idx, group_freq in enumerate(new_group_distribution):
                for i in range(group_freq):
                    next_state.append(previous_state[idx])
                        
        # Wright-Fisher inside groups
        else:
            for i in range(number_groups):
                new_group_state =[]
                for player_idx, (strategy_distribution, fitnesses, num_players) in enumerate(zip(previous_state[i], fitness[i], self.num_players)):
                    num_strats = len(strategy_distribution)
                    total_mutations = 0
                    new_player_state = np.zeros(num_strats)

                    for strategy_idx, n in enumerate(strategy_distribution):
                        f = fitnesses[strategy_idx]

                        # sample from binomial distribution to get number of mutations for strategy
                        if n == 0:
                            mutations = 0
                        else:
                            mutations = np.random.binomial(n, self.mu)
                        n -= mutations
                        total_mutations += mutations
                        new_player_state[strategy_idx] = n * f
                            
                        # distribute player strategies proportional n * f
                        # don't use multinomial, because that adds randomness we don't want yet
                    new_player_state *= float(num_players - total_mutations) / new_player_state.sum()
                    new_player_state = np.array(self.round_individuals(new_player_state))

                    new_player_state += np.random.multinomial(total_mutations, [1. / num_strats] * num_strats)
                    new_group_state.append(new_player_state)
                next_state.append(new_group_state)

        return next_state, fitness

