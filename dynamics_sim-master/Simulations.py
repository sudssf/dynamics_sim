from wrapper import GameDynamicsWrapper, VariedGame
from dynamics.wright_fisher import WrightFisher
from dynamics.replicator import Replicator
from games.hdb import HawkDoveBourgeois


shdb=VariedGame(HawkDoveBourgeois,Replicator)
shdb.vary_param('bias_strength',(-100,200,50),num_gens=100,num_iterations=50,parallelize=True,graph=dict(area=True,options=['smallfont']))