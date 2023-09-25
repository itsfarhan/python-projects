import random
import tkinter as tk

class Cell:
    def __init__(self, x1, y1, x2, y2, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win = win

    def draw(self):
        if self._win:
            if self.has_left_wall:
                self._win.draw_line(self._x1, self._y1, self._x1, self._y2)
            if self.has_right_wall:
                self._win.draw_line(self._x2, self._y1, self._x2, self._y2)
            if self.has_top_wall:
                self._win.draw_line(self._x1, self._y1, self._x2, self._y1)
            if self.has_bottom_wall:
                self._win.draw_line(self._x1, self._y2, self._x2, self._y2)

class Window:
    def __init__(self, width, height, num_cols, num_rows):
        self.__root = tk.Tk()
        self.__root.title("Maze Solver")
        
        self.__canvas = tk.Canvas(self.__root, width=width, height=height)
        self.__canvas.pack(fill=tk.BOTH, expand=True)
        
        self.__running = False

        self._width = width
        self._height = height
        self._num_cols = num_cols
        self._num_rows = num_rows
        
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
        
    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
    
    def close(self):
        self.__running = False
    
    def draw_line(self, start_x, start_y, end_x, end_y, fill_color="black", width=2):
        self.__canvas.create_line(start_x, start_y, end_x, end_y, fill=fill_color, width=width)
    
    def draw_cell(self, x1, y1, x2, y2, fill_color="white"):
        return self.__canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color)
    
    def draw_move(self, from_cell, to_cell, undo=False):
        x1 = (from_cell._x1 + from_cell._x2) / 2
        y1 = (from_cell._y1 + from_cell._y2) / 2
        x2 = (to_cell._x1 + to_cell._x2) / 2
        y2 = (to_cell._y1 + to_cell._y2) / 2
        line_color = "red" if undo else "gray"
        self.draw_line(x1, y1, x2, y2, fill_color=line_color, width=2)

class Maze:
    def __init__(self, x1, y1, num_cols, num_rows, cell_size, win=None, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_cols = num_cols
        self._num_rows = num_rows
        self._cell_size = cell_size
        self._win = win
        self._cells = []

        if seed is not None:
            random.seed(seed)

        self._create_cells()

    def _create_cells(self):
        for i in range(self._num_cols):
            col = []
            for j in range(self._num_rows):
                x1 = self._x1 + i * self._cell_size
                y1 = self._y1 + j * self._cell_size
                x2 = x1 + self._cell_size
                y2 = y1 + self._cell_size
                cell = Cell(x1, y1, x2, y2, self._win)
                col.append(cell)
                cell.draw()
                cell.visited = False
            self._cells.append(col)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        
        while True:
            possible_directions = []
            for dx, dy in directions:
                ni, nj = i + dx, j + dy
                if (
                    0 <= ni < self._num_cols
                    and 0 <= nj < self._num_rows
                    and not self._cells[ni][nj].visited
                ):
                    possible_directions.append((ni, nj))
            
            if not possible_directions:
                return
            
            ni, nj = random.choice(possible_directions)
            
            if ni > i:
                self._cells[i][j].has_right_wall = False
                self._cells[ni][nj].has_left_wall = False
            elif ni < i:
                self._cells[i][j].has_left_wall = False
                self._cells[ni][nj].has_right_wall = False
            elif nj > j:
                self._cells[i][j].has_bottom_wall = False
                self._cells[ni][nj].has_top_wall = False
            elif nj < j:
                self._cells[i][j].has_top_wall = False
                self._cells[ni][nj].has_bottom_wall = False

            self._break_walls_r(ni, nj)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_left_wall = False
        self._cells[0][0].has_top_wall = False
        self._cells[-1][-1].has_right_wall = False
        self._cells[-1][-1].has_bottom_wall = False

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def _solve_r(self, i, j):
        
        self._cells[i][j].visited = True
        
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for dx, dy in directions:
            ni, nj = i + dx, j + dy
            if (
                0 <= ni < self._num_cols
                and 0 <= nj < self._num_rows
                and not self._cells[ni][nj].visited
                and (
                    (dx, dy) == (0, -1) and not self._cells[i][j].has_top_wall
                    or (dx, dy) == (0, 1) and not self._cells[i][j].has_bottom_wall
                    or (dx, dy) == (-1, 0) and not self._cells[i][j].has_left_wall
                    or (dx, dy) == (1, 0) and not self._cells[i][j].has_right_wall
                )
            ):
                self._win.draw_move(self._cells[i][j], self._cells[ni][nj])
                if self._solve_r(ni, nj):
                    return True
                self._win.draw_move(self._cells[ni][nj], self._cells[i][j], undo=True)

        return False

    def solve(self):
        self._reset_cells_visited()
        return self._solve_r(0, 0)

def main():
    num_cols = 10
    num_rows = 10
    cell_size = 40
    width = num_cols * cell_size
    height = num_rows * cell_size
    win = Window(width, height, num_cols, num_rows)
    maze = Maze(0, 0, num_cols, num_rows, cell_size, win, seed=42)
    maze._break_walls_r(0, 0)
    maze._break_entrance_and_exit()
    # No need to start animation, we'll just generate and solve the maze

    if maze.solve():
        print("Maze solved!")
    else:
        print("Maze cannot be solved!")

    win.wait_for_close()

if __name__ == "__main__":
    main()
