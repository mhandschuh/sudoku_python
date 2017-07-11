import time

from sudokubacktracksolver import SudokuBackTrackSolver
from sudokuboard import SudokuBoard
import ctypes


def millis():
    "return a timestamp in milliseconds (ms)"
    tics = ctypes.c_int64()
    freq = ctypes.c_int64()

    # get ticks on the internal ~2MHz QPC clock
    ctypes.windll.Kernel32.QueryPerformanceCounter(ctypes.byref(tics))
    # get the actual freq. of the internal ~2MHz QPC clock
    ctypes.windll.Kernel32.QueryPerformanceFrequency(ctypes.byref(freq))

    t_ms = tics.value * 1e3 / freq.value
    return t_ms

givenValues = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

sudokuBoard = SudokuBoard(givenValues)

print("Input ----------------")
sudokuBoard.print()
print()
solver = SudokuBackTrackSolver()

start = millis()
solver.solve_sudoku(sudokuBoard.playerValues)
duration = millis() - start
print(duration)

print("Solution -------------")
sudokuBoard.print()
