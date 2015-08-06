__author__ = 'elubin'

from games.game import Game


class HawkDove(Game):
    """
    A class used to to represent the 2 player hawk-dove game. See U{http://www.life.umd.edu/classroom/zool360/L18-ESS/ess.html}
    """
    DEFAULT_PARAMS = dict(v=30, c=60, player1_prop=0.5)
    STRATEGY_LABELS = ('Hawk', 'Dove')
    PLAYER_LABELS = ('Player 1', 'Player 2')
    EQUILIBRIA_LABELS = ('All_Hawk', 'All_Dove', 'Hawk_Dove', 'Dove_Hawk')

    def __init__(self, v, c, player1_prop, equilibrium_tolerance=0.1):
        payoff_matrix = (( (v - c) / 2.0, v),
                         (0, v / 2.0))

        player_dist = (player1_prop, 1 - player1_prop)
        super(HawkDove, self).__init__(payoff_matrices=payoff_matrix, player_frequencies=player_dist, equilibrium_tolerance=equilibrium_tolerance)

    @classmethod
    def classify(cls, params, state, tolerance):
        p = params
        threshold = 1-tolerance
        
        if state[0][0] >= threshold:
            return 0
        elif state[1][1] >= threshold:
            return 1
        elif state[1][0] >= threshold:
            return 2
        elif state[0][1] >= threshold:
            return 3
        else:
            return super(HawkDove, cls).classify(params, state, tolerance)
