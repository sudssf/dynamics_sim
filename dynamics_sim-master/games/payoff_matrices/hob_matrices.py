def payoffs(p1, p2, p3, p4, a, b, c, d):
    payoffs = [[0 for x in range(8)] for x in range(4)]
    
    for index1, strat1 in enumerate(payoffs):
        for index2, payoff in enumerate(strat1):
            p1move12 = 1 if index1 > 1 else 0#If the state is 1 or 2, player 1 will play B
            p1move34 = index1 % 2
            
            p2move1 = 1 if index2 > 3 else 0
            p2move23 = 1 if (index2 % 4) > 1 else 0
            p2move4 = index2 % 2
            
            if p1move12 == 0:#States 1 and 2
                #State 1
                if p2move1 == 0:
                    payoffs[index1][index2] += a*p1
                else:
                    payoffs[index1][index2] += c*p1
                #State 2
                if p2move23 == 0:
                    payoffs[index1][index2] += a*p2
                else:
                    payoffs[index1][index2] += c*p2                        
            else:
                #State 1
                if p2move1 == 0:
                    payoffs[index1][index2] += b*p1
                else:
                    payoffs[index1][index2] += d*p1
                #State 2
                if p2move23 == 0:
                    payoffs[index1][index2] += b*p2
                else:
                    payoffs[index1][index2] += d*p2
                    
            if p1move34 == 0:#States 3 and 4
                #State 3
                if p2move23 == 0:
                    payoffs[index1][index2] += a*p3
                else:
                    payoffs[index1][index2] += c*p3
                #State 4
                if p2move4 == 0:
                    payoffs[index1][index2] += a*p4
                else:
                    payoffs[index1][index2] += c*p4              
            else:
                #State 3
                if p2move23 == 0:
                    payoffs[index1][index2] += b*p3
                else:
                    payoffs[index1][index2] += d*p3
                #State 2
                if p2move4 == 0:
                    payoffs[index1][index2] += b*p4
                else:
                    payoffs[index1][index2] += d*p4
                    
    return payoffs
            
            
