from wrapper import GameDynamicsWrapper, VariedGame

from dynamics.wright_fisher import WrightFisher
from dynamics.replicator import Replicator

from games.hdb import HawkDoveBourgeois
from games.cwol import CWOL

import unittest


class TestCase(unittest.TestCase):
    def setUp(self):
        import logging
        logging.basicConfig(filename='debug.log', level=logging.DEBUG) 

    # def calculate_stationary(self):
    #     s = GameDynamicsWrapper(Coordination, Moran)
    #     s.stationaryDistribution()
    #
    def test_single_simulation(self):
        s = GameDynamicsWrapper(CWOL, WrightFisher)
        s.simulate(num_gens=10000, graph=dict(area=True))

    def test_vary_one(self):  #Simulates while changing a single variable over time
        s = VariedGame(CWOL, WrightFisher, dynamics_kwargs=dict(uniDist=True))
        #s.vary_param('b', (0, 2, 10), num_gens=5000, num_iterations=20, graph=dict(area=True))

    # def test_vary_one2(self):#  Simulates while changing a single variable over time
    #     s = VariedGame(HumblySignaling, WrightFisher, dynamics_kwargs=dict(uniDist=True))
    #     s.vary_param('high_sender_proportion', (1, 15, 37), num_gens=160, num_iterations=500, graph=dict(area=True, normalize=9, lineArray=[(.36, .36, 0, 1)]))

    # def test_wireframe(self):# 3d graph of equilibrium found when varying two variables
    #     s = VariedGame(HawkDoveBourgeois, WrightFisher)
    #     s.vary_2params('v', (0, 5, 1), 'c', (1, 5, 1), num_iterations=1, num_gens=200)
    #
    # def test_contour_graph(self):#2d contour color plot
    #     s = VariedGame(HawkDoveBourgeois, WrightFisher)
    #     s.vary_2params('v', (0, 50, 1), 'c', (0, 100, 1), num_iterations=1, num_gens=500, burn=499, graph=dict(type='contour', lineArray=[(0, 50, 0, 50)]))
    #
    # def test_many_simulation(self):# Determines which equilibria result based upon several simulations, text output
    #     s = GameDynamicsWrapper(HawkDoveBourgeois, WrightFisher)
    #     print(s.simulate_many(num_iterations=2, num_gens=500))

if __name__ == '__main__':
    unittest.main()
