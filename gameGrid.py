import numpy as np
from gameCell import Cell


class Grid:
    def __init__(self, cols, rows, cell_size):
        self.cols = cols
        self.rows = rows
        self.cell_size = cell_size
        self.view_x = 0
        self.view_y = 0
        self.full_grid = np.array([[Cell(x, y, cell_size) for y in range(rows)] for x in range(cols)])
        self.update_visible_grid()

    def draw(self, win):
        for col in range(self.cols):
            for row in range(self.rows):
                self.grid[col][row].draw(win)

    def update(self):
        new_full_grid = np.array([[Cell(x, y, self.cell_size) for y in range(self.full_grid.shape[1])] for x in
                                  range(self.full_grid.shape[0])])
        for col in range(self.full_grid.shape[0]):
            for row in range(self.full_grid.shape[1]):
                num_neighbors = self.count_neighbors(col, row)
                if self.full_grid[col][row].alive:
                    new_full_grid[col][row].alive = num_neighbors == 2 or num_neighbors == 3
                else:
                    new_full_grid[col][row].alive = num_neighbors == 3
        self.full_grid = new_full_grid
        self.update_visible_grid()

    def count_neighbors(self, col, row):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0):
                    neighbor_col = (col + i) % self.full_grid.shape[0]
                    neighbor_row = (row + j) % self.full_grid.shape[1]
                    count += self.full_grid[neighbor_col][neighbor_row].alive
        return count

    def handle_click(self, pos):
        x, y = pos
        col = x // self.cell_size
        row = y // self.cell_size
        if 0 <= col < self.cols and 0 <= row < self.rows:
            full_col = col + self.view_x
            full_row = row + self.view_y
            if 0 <= full_col < self.full_grid.shape[0] and 0 <= full_row < self.full_grid.shape[1]:
                self.full_grid[full_col][full_row].toggle()
                self.update_visible_grid()

    def resize(self, new_cols, new_rows, new_cell_size):
        old_full_grid = self.full_grid.copy()
        new_full_cols = max(self.full_grid.shape[0], new_cols)
        new_full_rows = max(self.full_grid.shape[1], new_rows)
        self.cell_size = new_cell_size

        self.full_grid = np.array(
            [[Cell(x, y, new_cell_size) for y in range(new_full_rows)] for x in range(new_full_cols)])
        for col in range(old_full_grid.shape[0]):
            for row in range(old_full_grid.shape[1]):
                self.full_grid[col][row].alive = old_full_grid[col][row].alive

        self.cols = new_cols
        self.rows = new_rows
        self.update_visible_grid()

    def update_visible_grid(self):
        self.grid = np.array(
            [[self.full_grid[x + self.view_x][y + self.view_y] for y in range(self.rows)] for x in range(self.cols)])

    def set_viewport(self, view_x, view_y):
        self.view_x = view_x
        self.view_y = view_y
        self.update_visible_grid()
