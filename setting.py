from board import board
import pygame

CUBE_SIZE = 70
MATRIX_SIZE = len(board)
WINDOW_SIZE = (MATRIX_SIZE * CUBE_SIZE, MATRIX_SIZE * CUBE_SIZE)
screen = pygame.display.set_mode(WINDOW_SIZE)
starting_position = (6, 0)
