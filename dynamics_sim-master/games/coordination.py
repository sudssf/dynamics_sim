from games.game import Game

class Coordination(Game):
    DEFAULT_PARAMS = dict(a=1, b=5)
    PLAYER_LABELS = ('Player 1', 'Player 2')
    STRATEGY_LABELS = (('A1', 'B1'),
                       ('A2', 'B2'))
    EQUILIBRIA_LABELS = ('A', 'B')

    def __init__(self, a, b, equilibrium_tolerance=0.2):
        payoff_matrix_1 = ((a, 0),
                           (0, b))
                                
        payoff_matrix_2 = ((a, 0),
                           (0, b))

        payoff_matrix = [payoff_matrix_1, payoff_matrix_2]
        player_dist = (1/2, 1/2)
        super(Coordination, self).__init__(payoff_matrices=payoff_matrix, player_frequencies=player_dist, equilibrium_tolerance=equilibrium_tolerance)

    @classmethod
    def classify(cls, params, state, tolerance):
        # for convenience, we will guarantee that the state is normalized already to proportions, not absolute number of player
        p = params
        threshold = 1 - tolerance

        if state[0][0] > threshold and state[1][0] > threshold:
            # A
            return 0
        elif state[0][1] > threshold and state[1][1] > threshold:
            # B
            return 1
        else:
            return super(Coordination, cls).classify(params, state, tolerance)
