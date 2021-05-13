# ---------------------------------------------------------------
# Monopoly Probability Distribution | Eshan Uniyal
# March 2018, Python 3
# Based on Problem 84 of Project Euler
# ---------------------------------------------------------------

import timer
from random import randint

rolls = 10 ** 4 # total number of rolls/turns

def roll():
    """function to generate roll of dice"""
    moves, condition = [], True
        # moves is a list to store the moves
        # condition stores whether there's a need to roll again
    while condition == True and len(moves) != 3:
        d1, d2 = randint(1, 6), randint(1, 6)
        moves.append(d1 + d2)
        if d1 != d2:
            condition = False # terminates rolling of dice
        if len(moves) == 3 and d1 == d2:
            moves[2] = "G2J" # changes third move to "Go to Jail" if three doubles are rolled
    return(moves)

def cChest(cChestCards):
    # function that computes output of community chest
    odds = randint(1, 16)
    if odds <= 2: # if number from random generator is 1 or 2; effectively simulates chance
        # community chest having a move card 2/16
        to_return = cChestCards[0] # selects card at the top of the pile
        cChestCards.remove(to_return) # to shift to_return from the top of the pile to the bottom of the pile
        cChestCards.append(to_return)
        return(to_return)
    else:
        return(None)

def chance(chanceCards):
    # function that computes output of community chest
    odds = randint(1, 16)
    if odds <= 10: # if number from random generator is between 1 and 10; effectively simulates chance
        # chance having a move card has probability 10/16
        to_return = chanceCards[0] # selects card at the top of the pile
        chanceCards.remove(to_return) # to shift to_return from the top of the pile to the bottom of the pile
        chanceCards.append(to_return)
        return(to_return)
    else:
        return(None)


def main(nRolls):
    positions = {0: "GO", 1: "A1", 2: "CC1", 3: "A2", 4: "T1", 5: "R1", 6: "B1", 7: "CH1", 8: "B2", 9: "B3", 10: "JAIL",
                 11: "C1", 12: "U1", 13: "C2", 14: "C3", 15: "R2", 16: "D1", 17: "CC2", 18: "D2", 19: "D3", 20: "FP",
                 21: "E1", 22: "CH2", 23: "E2", 24: "E3", 25: "R3", 26: "F1", 27: "F2", 28: "U2", 29: "F3", 30: "G2J",
                 31: "G1", 32: "G2", 33: "CC3", 34: "G3", 35: "R4", 36: "CH3", 37: "H1", 38: "T2", 39: "H2"}

    landCount = {x : 0 for x in range(0, 40)}

    cChestCards = ['GO', 'JAIL'] # two out of sixteen cards
    chanceCards = ['GO', 'JAIL', 'C1', 'E3', 'H2', 'R1', 'R', 'R', 'U', -3] # ten out of sixteen cards
        # R = next railway station
        # U = next utility
        # -3 = go back three spaces

    currentPos = 0

    for turn in range(0, nRolls):
        moves = roll() # stores the moves the player has to make

        for move in moves:
            if move == "G2J":  # when three doubles are rolled
                currentPos = 10
                landCount[10] += 1
            else:

                currentPos += move # move forward "move" spaces
                currentPos = currentPos % 40 # necessary condition, else currentPos exceeds 39
                landCount[currentPos] += 1 # add one to landCount

                if positions[currentPos] == "G2J":  # if landed on "Go to Jail"
                    currentPos = 10
                    landCount[10] += 1

                elif "CC" in positions[currentPos]: # if first two letters of currentPos key are CC, then land on community chest
                    next = cChest(cChestCards)
                    if next != None:
                        if next == "GO":
                            currentPos = 0
                            landCount[0] += 1
                        elif next == "JAIL":
                            currentPos = 10
                            landCount[10] += 1

                elif "CH" in positions[currentPos]:
                    next = chance(chanceCards)
                    if next != None:
                        if next == -3: # if chance function returns - 3, go back three spaces
                            currentPos -= 3
                            landCount[currentPos] += 1
                        elif next == "R": # if chance function returns 'R', go to next railway station
                            for i in range(currentPos, 40):
                                if i == 6 or i == 16 or i == 26 or i == 36: # condition for i = index of next railway station
                                    currentPos = i
                                    landCount[currentPos] += 1
                                    break
                        elif next == "U":  # if chance function returns 'U', go to next utility
                            for i in range(currentPos, 40): # condition for i = index of next utility
                                if i == 12 or i == 28:
                                    currentPos = i
                                    landCount[currentPos] += 1
                                    break
                        else: # condition for possibilities 'GO', 'JAIL', 'C1', 'E3', 'H2', 'R1'
                            for position, value in positions.items():
                                if value == next: # if value in given dictionary corresponding a
                                        # certain key equals next, then said key is the position when moved
                                    currentPos = position
                                    landCount[currentPos] += 1

    landPercentages = {}
    for position, count in landCount.items():
        landPercentages[position] = count * 100 / nRolls

    for key, value in landPercentages.items():
        print(key, positions[key], value)

timer.start()
main(rolls)
timer.end()