from wrapper import GameDynamicsWrapper, VariedGame

from dynamics.wright_fisher import WrightFisher

from games.humbly_signaling import HumblySignaling
from games.hawk_dove import HawkDove
from games.costly_signaling import CostlySignaling

import unittest


class TestCase(unittest.TestCase):
    def setUp(self):
        import logging
        logging.basicConfig(filename='debug.log', level=logging.DEBUG) 

    # def calculate_stationary(self):
    #     s = GameDynamicsWrapper(Coordination, Moran)
    #     s.stationary_distribution()
    #
    # def test_single_simulation(self):# Runs simulation outputs time plot
    #     s = GameDynamicsWrapper(HumblySignaling, WrightFisher)
    #     s.simulate(num_gens=200, graph=dict(area=True, lineArray=[(5, 100, 0, 1), (100, 200, 1, .5)]))
    #
    # def test_vary_one(self):#Simulates while changing a single variable over time
    #     s = VariedGame(HumblySignaling, WrightFisher, dynamics_kwargs=dict(uniDist=True))
    #     s.vary_param('lReveal', (40, 100, 10), num_gens=100, num_iterations=2, graph=dict(area=True))
    #
    # def test_3d_graph(self):# 3d graph of equilibrium found when varying two variables, does not have hori or vert lines
    #     s = VariedGame(CostlySignaling, WrightFisher)
    #     s.vary_2params('lCost', (0, 5, 10), 'lProp', (1, 5, 10), num_iterations=15, num_gens=100)
    #
    def test_contour_graph(self):#2d contour color plot
        s = VariedGame(HumblySignaling, WrightFisher)
        s.vary_2params('lhSender', (1, 7, 5), 'lhReceiver', (-8, 0, 5), num_iterations=5, num_gens=2, graph=dict(type='contour', lineArray=[(-5, -2, 2, 4)]))
    #
    # def test_many_simulation(self):# Determines which equilibria result based upon several simulations, text output
    #     s = GameDynamicsWrapper(HawkDoveBourgeois, WrightFisher)
    #     print(s.simulate_many(num_iterations=10000, num_gens=1000))

if __name__ == '__main__':
    unittest.main()
    

        
