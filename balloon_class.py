from random import randrange
import pygame
from dataclasses import dataclass, field
from setting import CUBE_SIZE, starting_position, screen
from setting import *
from board import *


balloon_size = CUBE_SIZE - CUBE_SIZE//4

@dataclass
class Balloon:
    row: int
    col: int
    color: tuple[int, int, int] = (0, 0, 255)
    health: int = 100
    attack_radius: int = CUBE_SIZE
    grid_offset: tuple[int, int] = field(default_factory=lambda: (randrange(0, CUBE_SIZE//4), randrange(0, CUBE_SIZE//4)))
    speed: int = field(default_factory=lambda: randrange(1, 2+1))


    def get_color(self):
        # based off health
        return (100 - self.health/2, self.health*2, self.health*2)


    def is_alive(self) -> bool:
        return self.health > 0


    def get_attacked(self):
        from main import game
        self.health -= 20
        if self.health <= 0:
            game.balloons_killed += 1


    def draw(self):
        left_corner = (self.col * CUBE_SIZE + self.grid_offset[0], self.row * CUBE_SIZE + self.grid_offset[1])
        pygame.draw.rect(screen, self.get_color(), (left_corner[0], left_corner[1], balloon_size, balloon_size))


    def move(self):
        from main import game
        for _ in range(self.speed):
            next_position = get_next_position(self.row, self.col)
            if next_position:
                self.row, self.col = next_position
            else:
                game.lives -= 1
                self.row, self.col = starting_position
