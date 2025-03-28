from board import board
import pygame

CUBE_SIZE = 70
MATRIX_SIZE = len(board)
# WINDOW_WIDTH = MATRIX_SIZE * CUBE_SIZE
# WINDOW_HEIGHT = MATRIX_SIZE * CUBE_SIZE
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(WINDOW_SIZE)
starting_position = (6, 0)
