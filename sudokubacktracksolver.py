import time


class SudokuBackTrackSolver:
    cumulativetime = 0
    start = time.time()

    def find_cell_to_fill(self, solution, i=0, j=0):
        for x in range(i, 9):
            for y in range(j, 9):
                if solution[x][y] == 0:
                    self.cumulativetime += (time.time() - self.start)
                    return x, y

        for x in range(9):
            for y in range(9):
                if solution[x][y] == 0:
                    return x, y
        self.cumulativetime += (time.time() - self.start)
        return -1, -1

    def solve_sudoku(self, grid, i=0, j=0):
        i, j = self.find_cell_to_fill(grid, i, j)
        if i == -1:
            return True
        topleft_x, topleft_y = 3 * int(i / 3), 3 * int(j / 3)

        invalid_box = [grid[topleft_x][topleft_y], grid[topleft_x][topleft_y + 1], grid[topleft_x][topleft_y + 2],
                       grid[topleft_x + 1][topleft_y], grid[topleft_x + 1][topleft_y + 1],
                       grid[topleft_x + 1][topleft_y + 2],
                       grid[topleft_x + 2][topleft_y], grid[topleft_x + 2][topleft_y + 1],
                       grid[topleft_x + 2][topleft_y + 2]]

        valid_values = set(range(1, 10)) - set(
            grid[i] + [grid[0][j], grid[1][j], grid[2][j], grid[3][j], grid[4][j], grid[5][j], grid[6][j], grid[7][j],
                       grid[8][j]] + invalid_box)
        for guess in valid_values:
            grid[i][j] = guess
            if self.solve_sudoku(grid, i, j):
                return True
            grid[i][j] = 0
        return False