
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


balloons = [Balloon(6, i%3) for i in range(20)]


def get_balloon_mean():
    alive_ballons = list(get_alive_ballons())
    if alive_ballons:
        balloon_pos_y_mean = sum(balloon.row * CUBE_SIZE + balloon.grid_offset[1] for balloon in alive_ballons) / len(alive_ballons)
        balloon_pos_x_mean = sum(balloon.col * CUBE_SIZE + balloon.grid_offset[0] for balloon in alive_ballons) / len(alive_ballons)
    else:
        balloon_pos_y_mean = 0
        balloon_pos_x_mean = 0
    print(f'{balloon_pos_y_mean = }, {balloon_pos_x_mean = }')
    
    return balloon_pos_y_mean, balloon_pos_x_mean

game = SimpleNamespace(lives = 150, buttons = [
    Button(300-50, 20, lambda: balloons.extend([Balloon(6, 0), Balloon(6, 1), Balloon(6, 2)]), (0, 0, 255), (0, 0, 0), width=100, height=30, radius=10, padding=5, text="next wave"),
    Button(450-50, 20, lambda: print('clicked'), (0, 0, 255), (0, 0, 0), width=100, height=30, radius=10, padding=5, text="pause"),
    Button(600-50, 20, lambda: print('clicked'), (0, 0, 255), (0, 0, 0), width=100, height=30, radius=10, padding=5, text="resume"),
], balloons_killed = 0)


camera_man = SimpleNamespace(x=0, y=0, )


def camera_man_follow(pos_x: int, pos_y: int):
    travel_x = camera_man.x - pos_x
    if travel_x > 5:
        travel_x = 5
    elif travel_x < -5:
        travel_x = -5
    travel_y = camera_man.y - pos_y
    if travel_y > 5:
        travel_y = 5
    elif travel_y < -5:
        travel_y = -5
    camera_man.x += travel_x
    camera_man.y += travel_y
    

def pos_to_camera_pos(pos: tuple[int, int]) -> tuple[int, int]:
    rv = (pos[0] - (camera_man.x + WINDOW_WIDTH//2), pos[1] - (camera_man.y + WINDOW_HEIGHT//2))
    print(f'{pos = }, {rv = }')
    return rv




def draw_path():
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] != 0:
                left_corner = pos_to_camera_pos((col * CUBE_SIZE, row * CUBE_SIZE))
                pygame.draw.rect(screen, (0, 0, 0), (left_corner[0], left_corner[1], CUBE_SIZE, CUBE_SIZE))









def get_alive_ballons() -> Iterable['Balloon']:
    return (ballon for ballon in balloons if ballon.is_alive())

    # def get_covered_squares(self) -> Iterable[tuple[int, int]]:
    #     for neighbor in get_neighbors(self.row, self.col):
    #         yield neighbor



monkey_image = pygame.image.load('Monkey.png')


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

        scaled_monkey_image = pygame.transform.scale(monkey_image, (self.core_size*3, self.core_size*3))

        #first draw the attack range
        s = pygame.Surface((self.attack_radius*2, self.attack_radius*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (192, 192, 192, 100), (self.attack_radius, self.attack_radius), self.attack_radius)
        screen.blit(s, pos_to_camera_pos((self.x - self.attack_radius, self.y - self.attack_radius)))
        #then draw the tower
        screen.blit(scaled_monkey_image, pos_to_camera_pos((self.x - self.core_size*1.5, self.y - self.core_size*1.5)))


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
    screen.fill((255, 255, 255))
    grass_image = pygame.image.load('grass.png')
    for row in range(MATRIX_SIZE):
        for col in range(MATRIX_SIZE):
            if board[row][col] == 0:
                screen.blit(grass_image, pos_to_camera_pos((col*CUBE_SIZE, row*CUBE_SIZE)))


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


clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in game.buttons:
                button: Button
                if button.is_clicked(event.pos):
                    button.onclick()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                camera_man.x -= 30
            elif event.key == pygame.K_RIGHT:
                camera_man.x += 30
            elif event.key == pygame.K_UP:
                camera_man.y -= 30
            elif event.key == pygame.K_DOWN:
                camera_man.y += 30


    print(f"camera_man.x: {camera_man.x}, camera_man.y: {camera_man.y}")

    balloon_pos_y_mean, balloon_pos_x_mean = get_balloon_mean()

    camera_man_follow(balloon_pos_x_mean, balloon_pos_y_mean)

    for tower in towers:
        tower: Tower
        tower.attack_farthest_balloon()

    for balloon in get_alive_ballons():
        balloon.move()


    draw()


pygame.quit()
