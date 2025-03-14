import unittest
import pygame
from tetris import Tetrimino, check_collision, rotate_shape, clear_lines, grid, GRID_WIDTH  # Adjust import

class TestTetris(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.tetrimino = Tetrimino()

    def test_tetrimino_initialization(self):
        self.assertIn(self.tetrimino.shape, [
            [[1, 1, 1, 1]],  # I shape
            [[1, 1], [1, 1]],  # O shape
            [[0, 1, 0], [1, 1, 1]],  # T shape
            [[1, 1, 0], [0, 1, 1]],  # S shape
            [[0, 1, 1], [1, 1, 0]],  # Z shape
            [[1, 0, 0], [1, 1, 1]],  # L shape
            [[0, 0, 1], [1, 1, 1]]  # J shape
        ])
        self.assertGreaterEqual(self.tetrimino.x, 0)
        self.assertEqual(self.tetrimino.y, 0)

    def test_tetrimino_movement(self):
        original_x = self.tetrimino.x
        self.tetrimino.move(-1, 0)
        self.assertEqual(self.tetrimino.x, original_x - 1)

    def test_rotation(self):
        original_shape = self.tetrimino.shape
        rotated = rotate_shape(original_shape)
        self.assertEqual(len(rotated), len(original_shape[0]))

    def test_collision_detection(self):
        self.assertFalse(check_collision(self.tetrimino.shape, (self.tetrimino.x, self.tetrimino.y)))


if __name__ == "__main__":
    unittest.main()
