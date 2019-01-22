from dynamics.dynamics import DynamicsSimulator
import numpy as np

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

    def next_generation(self, previous_state, group_selection):
        next_state = []

        # copy to the new state
        for p in previous_state:
            next_state.append(p.copy())    
        # For group selection one individual from all the groups is chosen to reproduce proportional to it's fitness
        if group_selection:
            number_groups=len(previous_state)
            fitness = []
            for i in range(len(previous_state)):
                fitness.append(self.calculate_fitnesses(next_state[i]))
            total_fitness_per_player_type=[[] for i in range(len(previous_state[0]))]
            for i in range(len(previous_state[0])):
                for j in range(len(previous_state)):
                    for k in range(len(fitness[j][i])):
                        total_fitness_per_player_type[i].append(fitness[j][i][k]*next_state[j][i][k])
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
        # TO DO: Variable iterations per time step and consolidate both group and individual selection?    
        # In the absence of group selection
        else:
            
           fitness = self.calculate_fitnesses(next_state)

           minimum_total = min(p.sum() for p in next_state)
           # make sure there are enough individuals of each type to take away 2 * num_iterations_per_time_step
           num_iterations = int(min(self.num_iterations_per_time_step * 2, minimum_total) / 2)
        
           for idx, (p, f) in enumerate(zip(next_state, fitness)):
                reproduce = np.zeros(len(p))
                for i in range(num_iterations):
                    # sample from distribution to determine winner and loser (he who reproduces, he who dies)
                    weighted_total = sum(n_i * f_i for n_i, f_i in zip(p, f))
                    dist = np.array([n_i * f_i / weighted_total for n_i, f_i in zip(p, f)])
                    sample = np.random.multinomial(1, dist)
                    p -= sample
                    reproduce += sample
                
                    # Can add mutations during reproduction. Add it at the level of DynamicsSimulator?
                    reproduce=self.mutate(reproduce,self.mu)

                for i in range(num_iterations):
                    # now determine who dies from what's left
                    total = p.sum()
                    dist = [n_i / float(total) for n_i in p]
                    p -= np.random.multinomial(1, dist)
                next_state[idx] = p + reproduce * 2
        
        return next_state, fitness
   # I don't think a separate function is needed? 
    def mutate(self,reproduce,mu):
        
        if np.random.uniform(0,1)<mu:
            reproduce=np.zeros(len(reproduce))
            mutationIndex=np.random.randint(0,len(reproduce))
            reproduce[mutationIndex]+=1
        
        return reproduce
            
            
            