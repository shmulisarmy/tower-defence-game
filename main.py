
from dataclasses import dataclass, field
import time
from typing import Iterable
from button import Button
import pygame
from types import SimpleNamespace

from setting import *
from colors import *
from board import *
from balloon_class import Balloon
pygame.init()


ballons = [Balloon(6, i%3) for i in range(20)]

game = SimpleNamespace(lives = 150, buttons = [
    Button(300-50, 20, lambda: ballons.extend([Balloon(6, 0), Balloon(6, 1), Balloon(6, 2)]), (0, 0, 255), (0, 0, 0), width=100, height=30, radius=10, padding=5, text="next wave"),
    Button(450-50, 20, lambda: print('clicked'), (0, 0, 255), (0, 0, 0), width=100, height=30, radius=10, padding=5, text="pause"),
    Button(600-50, 20, lambda: print('clicked'), (0, 0, 255), (0, 0, 0), width=100, height=30, radius=10, padding=5, text="resume"),
], balloons_killed = 0)







def draw_path():
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] != 0:
                left_corner = (col * CUBE_SIZE, row * CUBE_SIZE)
                pygame.draw.rect(screen, (0, 0, 0), (left_corner[0], left_corner[1], CUBE_SIZE, CUBE_SIZE))











def get_alive_ballons() -> Iterable['Balloon']:
    return (ballon for ballon in ballons if ballon.is_alive())

    # def get_covered_squares(self) -> Iterable[tuple[int, int]]:
    #     for neighbor in get_neighbors(self.row, self.col):
    #         yield neighbor





@dataclass
class Tower:
    x: int
    y: int
    core_size: int = CUBE_SIZE // 3
    attack_radius: int = CUBE_SIZE
    color: tuple[int, int, int, int] = (0, 0, 255)
    covered_squares: list[tuple[int, int]] = field(default_factory=list)


    def __post_init__(self):
        self.covered_squares = self.get_covered_squares()


    def draw(self):
        #first draw the attack range
        s = pygame.Surface((self.attack_radius*2, self.attack_radius*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (192, 192, 192, 100), (self.attack_radius, self.attack_radius), self.attack_radius)
        screen.blit(s, (self.x - self.attack_radius, self.y - self.attack_radius))
        #then draw the tower
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.core_size)


    def get_covered_squares(self) -> list[tuple[int, int]]:
        # starts from the middle
        left = (self.x - self.attack_radius)/CUBE_SIZE
        right = (self.x + self.attack_radius)/CUBE_SIZE
        top = (self.y - self.attack_radius)/CUBE_SIZE
        bottom = (self.y + self.attack_radius)/CUBE_SIZE
        
        covered_squares = [ (row, col) for row in range(int(top), int(bottom)+1) for col in range(int(left), int(right)+1) if in_bounds(row, col) ]
        
        return sorted(covered_squares, key=lambda square: board[square[0]][square[1]], reverse=True)
    def attack_farthest_balloon(self):
        for square in self.covered_squares:
            for balloon in get_alive_ballons():
                balloon: Balloon
                if balloon.row == square[0] and balloon.col == square[1]:
                    return balloon.get_attacked()
        return None


towers = [Tower(180, 250), Tower(400, 400), Tower(240, 400)]

def draw():
    # screen.fill((255, 255, 255))
    grass_image = pygame.image.load('grass.png')
    for row in range(MATRIX_SIZE):
        for col in range(MATRIX_SIZE):
            if board[row][col] == 0:
                screen.blit(grass_image, (col*CUBE_SIZE, row*CUBE_SIZE))


    for button in game.buttons:
        button.draw()
    

    draw_path()
    for tower in towers:
        tower: Tower
        tower.draw()
    for balloon in get_alive_ballons():
        balloon.draw()

    font = pygame.font.Font(None, 36)
    lives_text = font.render(f'Lives: {game.lives}', True, (0, 0, 0))
    screen.blit(lives_text, (10, 10))
    heart = pygame.image.load('heart.png')
    heart = pygame.transform.scale(heart, (36, 36))
    screen.blit(heart, (150, 10))
    

    font = pygame.font.Font(None, 36)
    balloons_killed_text = font.render(f'Balloon killed: {game.balloons_killed}', True, (0, 0, 0))
    screen.blit(balloons_killed_text, (10, 50))
    
    

    pygame.display.update()



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for tower in towers:
        tower: Tower
        tower.attack_farthest_balloon()

    for balloon in get_alive_ballons():
        time.sleep(0.01)
        balloon.move()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in game.buttons:
                button: Button
                if button.is_clicked(event.pos):
                    button.onclick()



    draw()


pygame.quit()
