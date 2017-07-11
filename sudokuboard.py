import copy


class SudokuBoard:
    def __init__(self, given):
        self.givenValues = given
        self.playerValues = copy.deepcopy(self.givenValues)

    def reset(self):
        self.playerValues = copy.deepcopy(self.givenValues)

    def print(self, playervalues=None):
        if playervalues is None:
            playervalues = self.playerValues

        W = '\033[0m'  # white (normal)
        R = '\033[31m'  # red
        G = '\033[32m'  # green
        O = '\033[33m'  # orange
        B = '\033[34m'  # blue
        P = '\033[35m'  # purple

        print("┌───┬───┬───" + B + "╥" + W + "───┬───┬───" + B + "╥" + W + "───┬───┬───┐")

        for i in range(0, 9):
            print('│', end='')
            for j in range(0, 9):
                value = ' '
                if self.givenValues[i][j] != 0:
                    value = G + str(self.givenValues[i][j]) + W
                elif playervalues[i][j] != 0:
                    value = R + str(playervalues[i][j]) + W

                terminator = B + '║' + W if (j + 1) % 3 == 0 and j < 8 and j != 0 else '│'
                print(' ' + value + ' ' + terminator, end='' if j < 8 else '\n')
            if i < 8:
                if i != 0 and (i + 1) % 3 == 0:
                    print(B + "╞═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╡" + W)
                else:
                    print("├───┼───┼───" + B + "╫" + W + "───┼───┼───" + B + "╫" + W + "───┼───┼───┤")
        print("└───┴───┴───" + B + "╨" + W + "───┴───┴───" + B + "╨" + W + "───┴───┴───┘")