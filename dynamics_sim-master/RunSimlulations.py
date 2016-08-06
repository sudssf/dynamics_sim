from wrapper import GameDynamicsWrapper, VariedGame

from dynamics.wright_fisher import WrightFisher
from dynamics.replicator import Replicator
from dynamics.moran import Moran

from games.coordination import Coordination
from games.hawk_dove import HawkDove
from games.cts_disc import CtsDisc

import unittest

state = [(0, 0, 0, 0, 0, 0, 0, 0, 100, 0)]

class TestCase(unittest.TestCase):
    def setUp(self):
        import logging
        logging.basicConfig(filename='debug.log', level=logging.DEBUG)

    def test_single_simulation(self):
        s = GameDynamicsWrapper(Coordination, Moran)
        s.simulate(num_gens=100, graph=dict(area=True), graph_payoffs=True)

    def test_single_population(self):
        s = GameDynamicsWrapper(HawkDove, WrightFisher, dynamics_kwargs=dict(selection_strength=0.15))
        #s.simulate(num_gens=2000, graph=dict(area=True))

    def test_many_simulation(self):  # Determines which equilibria result based upon several simulations, text output
        s = GameDynamicsWrapper(CtsDisc, WrightFisher)
        #print(s.simulate_many(num_iterations=100, num_gens=100, graph=False, class_end=True))#dict(area=True, shading='redBlue')))
if __name__ == '__main__':
    unittest.main()

if False:
    def calculate_stationary(self):
        s = GameDynamicsWrapper(Coordination, Moran)
        s.stationaryDistribution()

    def test_vary_one(self):  # Simulates while changing a single variable over time
        s = VariedGame(HawkDove, WrightFisher, dynamics_kwargs=dict(uniDist=True))
        s.vary_param('lCost', (5, 0, 5), num_gens=500, num_iterations=5, graph=dict(area=True))

    def test_vary_one2(self):  # Simulates while changing a single variable over time
        s = VariedGame(HawkDove, WrightFisher, dynamics_kwargs=dict(uniDist=True))
        s.vary_param('high_sender_proportion', (1, 15, 37), num_gens=160, num_iterations=500, graph=dict(area=True, normalize=9, lineArray=[(.36, .36, 0, 1)]))

    def test_wireFrame(self):  # 3d graph of equilibrium found when varying two variables
        s = VariedGame(HawkDoveBourgeois, WrightFisher)
        s.vary_2params('v', (0, 5, 1), 'c', (1, 5, 1), num_iterations=1, num_gens=200)

    def test_contour_graph(self):  # 2d contour color plot
        s = VariedGame(HawkDoveBourgeois, WrightFisher)
        s.vary_2params('v', (0, 50, 1), 'c', (0, 100, 1), num_iterations=1, num_gens=500, burn=499, graph=dict(type='contour', lineArray=[(0, 50, 0, 50)]))
