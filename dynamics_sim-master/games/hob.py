from games.game import Game
from games.payoff_matrices.hob_matrices import payoffs

class HoB(Game):
    DEFAULT_PARAMS = dict(p1=1, p2=1, p3=1, p4=1, a=1, b=0, c=0, d=1, player1_prop=0.5)
    PLAYER_LABELS = ('Player 1', 'Player 2')
    STRATEGY_LABELS = (('AA', 'AB', 'BA', 'BB'),
                       ('AAA', 'AAB', 'ABA', 'ABB', 'BAA', 'BAB', 'BBA', 'BBB'))
    EQUILIBRIA_LABELS = ('All A', 'All B')

    def __init__(self, p1, p2, p3, p4, a, b, c, d, player1_prop, equilibrium_tolerance=0.1):
        P1 = p1 / (p1+p2+p3+p4)
        P2 = p2 / (p1+p2+p3+p4)
        P3 = p3 / (p1+p2+p3+p4)
        P4 = p4 / (p1+p2+p3+p4)
        
        '''
        payoff matrix = (( (a,a), (c,c) ),
                         ( (b,b), (d,d) ))
        '''
        
        payoff_matrix_p1 = payoffs(P1, P2, P3, P4, a, b, c, d)
        payoff_matrix_p2 = payoff_matrix_p1

        payoff_matrix = [payoff_matrix_p1, payoff_matrix_p2]
        player_dist = (player1_prop, 1 - player1_prop)
        super(HoB, self).__init__(payoff_matrices=payoff_matrix, player_frequencies=player_dist, equilibrium_tolerance=equilibrium_tolerance)

    @classmethod
    def classify(cls, params, state, tolerance):
        threshold = 1 - tolerance

        if state[0][0] > threshold and state[1][0] > threshold:
            return 0#All A
        elif state[0][3] > threshold and state[1][7] > threshold:
            return 1#All B
        else:
            return super(HoB, cls).classify(params, state, tolerance)
