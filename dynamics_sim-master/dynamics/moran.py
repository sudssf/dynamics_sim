from dynamics.dynamics import DynamicsSimulator
import numpy as np
from itertools import chain

class Moran(DynamicsSimulator):
    """
    A stochastic dynamics simulator that performs the Moran process on all player types in the population.
    See U{Moran Process<http://en.wikipedia.org/wiki/Moran_process#Selection>}
    """
    def __init__(self, num_iterations_per_time_step=1,*args, **kwargs):
        """
        The constructor for the Moran dynamics process, that the number of births/deaths to process per time step.

        @param num_iterations_per_time_step: the number of iterations of the Moran process we do per time step
        @type num_iterations_per_time_step: int
        """
        super(Moran, self).__init__(*args,stochastic=True,**kwargs)
        assert num_iterations_per_time_step >= 1
        self.num_iterations_per_time_step = num_iterations_per_time_step
        self.mu=0.01

    def next_generation(self, previous_state, group_selection, rate):
        next_state = []

        # Copy to the new state
        for p in previous_state:
            next_state.append(p.copy())    
            
        number_groups=len(previous_state)
        fitness = []
        for i in range(len(previous_state)):
            fitness.append(self.calculate_fitnesses(next_state[i]))
        total_fitness_per_player_type=[[] for i in range(len(previous_state[0]))]
        for i in range(len(previous_state[0])):
            for j in range(len(previous_state)):
                for k in range(len(fitness[j][i])):
                    total_fitness_per_player_type[i].append(fitness[j][i][k]*next_state[j][i][k])
                        
        # Moran at the group level            
        if group_selection and np.random.uniform(0,1)<rate:
            avg_payoffs=[]
            for k in range(number_groups):
                avg_payoffs.append(sum(chain(*fitness[k]))/sum(sum(chain(*fitness[j])) for j in range(number_groups)))
                
            # Pick the group that will reproduce and the one that it replaces
            reproduction = np.random.multinomial(1,avg_payoffs)
            reproduction_index = np.nonzero(reproduction)[0][0]
            replacement_event=np.random.randint(0,number_groups)
            next_state[replacement_event]=next_state[reproduction_index]
        else:
            # Moran at individual level where one individual from all the groups is chosen to reproduce proportional to it's fitness
            group=[]
            strategy=[]
               
            # For each player-type pick one individual from one group to reproduce
            for i in range(len(total_fitness_per_player_type)):
                weighted_total=sum(total_fitness_per_player_type[i])
                dist = np.array([f_i/weighted_total for f_i in total_fitness_per_player_type[i]])
                sample = np.random.multinomial(1,dist)
                reproduce_index=np.nonzero(sample)[0][0]
                player_strat= len(total_fitness_per_player_type[i])/number_groups
                group.append(int(reproduce_index/player_strat))
                strategy.append(int(reproduce_index%player_strat))
                   
            # Pick a random individual to replace from the same group as the reproducing individual
            for player_no, (group_no,strat_no) in enumerate(zip(group,strategy)):
                p = next_state[group_no][player_no]
                   
                # Determine who dies
                total = p.sum()
                dist = [n_i / float(total) for n_i in p]
                   
                # Chance of mutating while reproduction
                if np.random.uniform(0,1)<self.mu:
                    strat_no = np.random.randint(0,len(p))
                p[strat_no] += 1
                p -= np.random.multinomial(1, dist)
            next_state[group_no][player_no]=p  
               
        # TO DO: Variable iterations per time step   
        
        return next_state, fitness
        
            
            
            