import unittest
from maze import Maze, Window

class Tests(unittest.TestCase):
    
    def test_reset_cells_visited(self):
        num_cols = 10
        num_rows = 10
        win = Window(800, 600)
        maze = Maze(0, 0, num_rows, num_cols, 40, 40, win, seed=42)
        
        # Set the visited status of some cells to True (for testing)
        maze._cells[2][3].visited = True
        maze._cells[5][7].visited = True
        
        # Reset the visited status of all cells
        maze._reset_cells_visited()
        
        for i in range(num_cols):
            for j in range(num_rows):
                self.assertFalse(maze._cells[i][j].visited)  # Ensure all visited properties are False
                
                
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
        
    def test_break_entrance_and_exit(self):
        num_cols = 10
        num_rows = 10
        maze = Maze(0, 0, num_rows, num_cols, 40, 40)
        maze._break_entrance_and_exit()

        # Check that the entrance walls are broken
        top_left_cell = maze._cells[0][0]
        self.assertFalse(top_left_cell.has_left_wall)
        self.assertFalse(top_left_cell.has_top_wall)
        self.assertTrue(top_left_cell.has_right_wall)
        self.assertTrue(top_left_cell.has_bottom_wall)

        # Check that the exit walls are broken (bottom-right cell)
        bottom_right_cell = maze._cells[-1][-1]
        self.assertTrue(bottom_right_cell.has_left_wall)
        self.assertTrue(bottom_right_cell.has_top_wall)
        self.assertFalse(bottom_right_cell.has_right_wall)
        self.assertFalse(bottom_right_cell.has_bottom_wall)

    def test_maze_create_cells_different_dimensions(self):
        num_cols = 8
        num_rows = 6
        m2 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m2._cells),
            num_cols,
        )
        self.assertEqual(
            len(m2._cells[0]),
            num_rows,
        )

    def test_reset_cells_visited_after_break_walls(self):
        num_cols = 10
        num_rows = 10
        maze = Maze(0, 0, num_rows, num_cols, 40, 40)  # Create a maze
        maze._break_walls_r(0, 0)  # Perform some actions to set visited=True
        maze._reset_cells_visited()  # Reset visited property

        # Now, check that all cells in the maze have visited=False
        for i in range(num_cols):
            for j in range(num_rows):
                self.assertFalse(maze._cells[i][j].visited)

    def test_maze_create_cells_with_window(self):
        num_cols = 5
        num_rows = 4
        win = None  # You can pass a Window object here if needed
        m3 = Maze(0, 0, num_rows, num_cols, 10, 10, win)
        self.assertEqual(
            len(m3._cells),
            num_cols,
        )
        self.assertEqual(
            len(m3._cells[0]),
            num_rows,
        )

if __name__ == "__main__":
    unittest.main()
