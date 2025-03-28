from random import randrange
import pygame
from dataclasses import dataclass, field
from setting import CUBE_SIZE, starting_position, screen
from main import game
from board import get_next_position
from setting import *

@dataclass
class Balloon:
    row: int
    col: int
    color: tuple[int, int, int] = (0, 0, 255)
    health: int = 100
    attack_radius: int = CUBE_SIZE
    grid_offset: tuple[int, int] = field(default_factory=lambda: (randrange(0, CUBE_SIZE), randrange(0, CUBE_SIZE)))


    def get_color(self):
        # based off health
        return (100 - self.health/2, self.health*2, self.health*2)


    def is_alive(self) -> bool:
        return self.health > 0


    def get_attacked(self):
        self.health -= 20
        if self.health <= 0:
            game.lives -= 1


    def draw(self):
        print("drawing balloon")
        left_corner = (self.col * CUBE_SIZE + self.grid_offset[0], self.row * CUBE_SIZE + self.grid_offset[1])
        pygame.draw.rect(screen, self.get_color(), (left_corner[0], left_corner[1], CUBE_SIZE, CUBE_SIZE))


    def move(self):
        print(f'{self.row = }')
        print(f'{self.col = }')
        next_position = get_next_position(self.row, self.col)
        print(f'{next_position = }')
        if next_position is not None:
            self.row, self.col = next_position
        else:
            self.row, self.col = starting_position
