import copy
import alphaBetaPruning
from os import system
import random

VICTORY = 10 ** 20  # The value of a winning board (for max)
LOSS = -VICTORY  # The value of a losing board (for max)
TIE = 0  # The value of a tie
SIZE = 4  # the length of winning seq.
COMPUTER = SIZE + 1  # Marks the computer's cells on the board
HUMAN = 1  # Marks the human's cells on the board

turn = {HUMAN: COMPUTER, COMPUTER: HUMAN}

rows = 6
columns = 7


class game:
    board = []
    size = rows * columns
    playTurn = HUMAN
    # Used by alpha-beta pruning to allow pruning

    '''
    The state of the game is represented by a list of 4 items:
        0. The game board - a matrix (list of lists) of ints. Empty cells = 0,
        the comp's cells = COMPUTER and the human's = HUMAN
        1. The heuristic value of the state.
        2. Whose turn is it: HUMAN or COMPUTER
        3. Number of empty cells
    '''


def create(s):
    # Returns an empty board. The human plays first.
    # create the board
    s.board = []
    for i in range(rows):
        s.board = s.board + [columns * [0]]

    s.playTurn = HUMAN
    s.size = rows * columns
    s.val = 0.00001

    # return [board, 0.00001, playTurn, r*c]     # 0 is TIE


def cpy(s1):
    # construct a parent DataFrame instance
    s2 = game()
    s2.playTurn = s1.playTurn
    s2.size = s1.size
    s2.board = copy.deepcopy(s1.board)
    # print("board ", s2.board)
    return s2

# Yishai Lutvak 304909864
# Notice that I left the depth of tree 2,
# and yet the heuristics make the computer play really well

# Returns the heuristic value of s
# The totalEvaluate function will have documentation that explains the heuristics
def value(s):
    # Checks whether there is a win or a loss
    if find_horizontal(s) or find_vertical(s) or find_hypotenuse1(s) or find_hypotenuse2(s):
        return VICTORY if s.playTurn == HUMAN else LOSS

    # Checks whether the result is a draw - if the board is full
    if s.size == 0:
        return TIE

    # print(s.board)
    # print(f"HUMAN value: {totalEvaluate(s,HUMAN)}")
    # print(f"COMPUTER value: {totalEvaluate(s,COMPUTER)}")
    # print (f"COMPUTER LESS HUMAN value: {0.00001 + totalEvaluate(s,COMPUTER) - totalEvaluate(s,HUMAN)}")

    # Returns the board value result to the player less the board value to the other player
    return 0.00001 + totalEvaluate(s, COMPUTER) - totalEvaluate(s, HUMAN)

# Checks if there is a sequence of four in any row
def find_horizontal(s):
    return any(map(lambda i: max_len(s.board[i], turn[s.playTurn]) >= 4, range(rows)))

# Builds a list of the columns when each column is a list
def vertical_func(s):
    verticals = []
    for i in range(columns):
        verti = []
        for item in s.board:
            verti += [item[i]]
        verticals += [verti]
    # print(verticals)
    return verticals

# Checks if there is a sequence of four in any column
def find_vertical(s):
    # vertical_func = lambda i: map(lambda x: x[i], s.board)
    listVerticals = vertical_func(s)
    return any(map(lambda i: max_len(listVerticals[i], turn[s.playTurn]) >= 4, range(columns)))

# Builds a list of the diagonals from top and left to bottom and right
def hypotenuse1_func(s):
    column = 0
    row = rows - 4
    hypotenuses1 = []
    for i in range(rows + columns - 2 * 3 - 1):
        hypo = []
        step = 0
        while row + step < rows and column + step < columns:
            hypo = hypo + [s.board[row + step][column + step]]
            step += 1
        hypotenuses1 += [hypo]
        if row != 0:
            row -= 1
        else:
            column += 1
    # print(hypotenuses1)
    return hypotenuses1

# Checks if there is a sequence of four in any diagonal from top and left to bottom and right
def find_hypotenuse1(s):
    listHypotenuse1 = hypotenuse1_func(s)
    return any(map(lambda i: max_len(listHypotenuse1[i], turn[s.playTurn]) >= 4, range(rows + columns - 2 * 3 - 1)))

# Builds a list of the diagonals from top and right to bottom and left
def hypotenuse2_func(s):
    column = 3
    row = 0
    hypotenuses2 = []
    for i in range(rows + columns - 2 * 3 - 1):
        hypo = []
        step = 0
        while row + step < rows and column - step >= 0:
            hypo = hypo + [s.board[row + step][column - step]]
            step += 1
        hypotenuses2 += [hypo]
        if column != columns - 1:
            column += 1
        else:
            row += 1
    # print(hypotenuses2)
    return hypotenuses2

# Checks if there is a sequence of four in any diagonal from top and right to bottom and left
def find_hypotenuse2(s):
    listHypotenuse2 = hypotenuse2_func(s)
    return any(map(lambda i: max_len(listHypotenuse2[i], turn[s.playTurn]) >= 4, range(rows + columns - 2 * 3 - 1)))

# Auxiliary function for calculating maximum sequence in a list
def max_len(_list, num):
    count = 0
    max_count = 0
    for item in _list:
        if item != num:
            count = 0
        else:
            count += 1
        max_count = max(count, max_count)
    return max_count

# Heuristics combine two different heuristics
# 1. Calculation of how many possibilities remain on the board for player to create sequence four
# As the game begins, there are 69 options to create a four sequence for each player
# 2. Giving value by sequences of three,
# whether there is a three or continuous or non-continuous sequence (one free space)
# in a way that adding one full position will be beatable.
# In addition, priority is given to creating a consecutive sequence of three
# so that victory can be achieved on both sides of the sequence.
def totalEvaluate(s, actor):

    # Internal function for single line evaluation
    def evaluate(_list, actor):

        # Parameters for potential
        counter = 0

        # Parameters for a sequence of three
        valueOfSequenceThree = 16
        sequenceThree = 0
        continuousSequence = 0
        sequence = 0

        # Temporary parameters
        flagOneJamp = 0
        flagLast0AfterSequence = 0

        for item in _list:
            # Case 1 - The other player's place
            if item != 0 and item != actor:
                flagLast0AfterSequence == 0
                if counter < 4:
                    counter = 0
                    sequence = 0
                    continuousSequence = 0
                # No more chances for four places
                else:
                    break

            # Case 2 - The player's place
            elif item == actor:
                flagLast0AfterSequence == 0
                counter += 1
                sequence += 1
                continuousSequence += 1

            # Case 3 - Empty place
            else:
                counter += 1
                # Two empty spaces interrupt a sequence|X| | |X|
                if flagLast0AfterSequence == 1:
                    sequence = 0
                    flagLast0AfterSequence = 0
                    flagOneJamp = 0
                # The sequence is continuous
                elif continuousSequence == 3:
                    sequenceThree = 2 if counter > 4 else 1  # |X|X|X| | = 1, | |X|X|X| | = 2
                    sequence = 0
                    flagOneJamp = 0
                # The sequence of three is not continuous |X| |X|X|
                elif sequence >= 3:
                    sequenceThree = 1
                    sequence = 0
                    flagOneJamp = 0
                # The sequence is less than three
                elif sequence > 0:
                    flagLast0AfterSequence = 1
                    if flagOneJamp == 0:  # for example | |X|X| |
                        flagOneJamp = 1
                    # The sequence is not continuous |X| |X| |
                    else:
                        sequence = continuousSequence
                continuousSequence = 0

        # The number of options to create a sequence is as many as the optional less than three.
        # For example: |X|X|X|X| | | | or | |X|X|X|X| | | or | | |X|X|X|X| | or | | | |X|X|X|X| = 7 - 3 = 4
        if counter > 3:
            potential = counter - 3
            if sequence > 3:
                sequenceThree = 1
        else:
            potential = 0
        return potential + sequenceThree * valueOfSequenceThree

    # Create 4 lists of all options to create sequences and then scan them by the internal function
    totalEval = 0
    listVerticals = vertical_func(s)
    listHypotenuse1 = hypotenuse1_func(s)
    listHypotenuse2 = hypotenuse2_func(s)
    lists = [s.board, listVerticals, listHypotenuse1, listHypotenuse2]
    for list in lists:
        for item in list:
            totalEval += evaluate(item, actor)
    return totalEval


def printState(s):
    system("cls")
    # Prints the board. The empty cells are printed as numbers = the cells name(for input)
    # If the game ended prints who won.
    for r in range(rows):
        print("\n|", end="")
        # print("\n",len(s[0][0])*" --","\n|",sep="", end="")
        for c in range(columns):
            if s.board[r][c] == COMPUTER:
                print("X|", end="")
            elif s.board[r][c] == HUMAN:
                print("O|", end="")
            else:
                print(" |", end="")

    print()

    for i in range(columns):
        print(" ", i, sep="", end="")

    print()

    val = value(s)

    if val == VICTORY:
        print("I won!")
    elif val == LOSS:
        print("You beat me!")
    elif val == TIE:
        print("It's a TIE")


def isFinished(s):
    # Seturns True iff the game ended
    return value(s) in [LOSS, VICTORY, TIE] or s.size == 0


def isHumTurn(s):
    # Returns True iff it is the human's turn to play
    return s.playTurn == HUMAN


def decideWhoIsFirst(s):
    # The user decides who plays first
    if int(input("Who plays first? 1-me / anything else-you : ")) == 1:
        s.playTurn = COMPUTER
    else:
        s.playTurn = HUMAN

    return s.playTurn


def makeMove(s, c):
    # Puts mark (for huma. or comp.) in col. c
    # and switches turns.
    # Assumes the move is legal.
    r = 0
    while r < rows and s.board[r][c] == 0:
        r += 1

    s.board[r - 1][c] = s.playTurn  # marks the board
    s.size -= 1  # one less empty cell
    if (s.playTurn == COMPUTER):
        s.playTurn = HUMAN
    else:
        s.playTurn = COMPUTER


def inputMove(s):
    # Reads, enforces legality and executes the user's move.

    # self.printState()
    flag = True
    while flag:
        c = int(input("Enter your next move: "))
        if c < 0 or c >= columns or s.board[0][c] != 0:
            print("Illegal move.")

        else:
            flag = False
            makeMove(s, c)


def getNext(s):
    # returns a list of the next states of s
    ns = []
    for c in list(range(columns)):
        # print("c=", c)
        if s.board[0][c] == 0:
            # print("possible move ", c)
            tmp = cpy(s)
            makeMove(tmp, c)
            # print("tmp board=", tmp.board)
            ns += [tmp]
            # print("ns=", ns)
    # print("returns ns ", ns)
    return ns


def inputComputer(s):
    return alphaBetaPruning.go(s)
