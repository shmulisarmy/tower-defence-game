import pygame
from setting import screen
from dataclasses import dataclass

@dataclass
class Button:
    x: int
    y: int
    onclick: callable
    color: tuple[int, int, int]
    background: tuple[int, int, int]
    width: int
    height: int
    radius: int
    padding: int
    text: str = 'click me'

    def draw(self):
        # Draw the button shadow (optional, but adds depth)
        shadow_offset = 5  # This will give the shadow a little offset
        shadow_color = (0, 0, 0)  # Shadow color (black)
        pygame.draw.rect(screen, shadow_color, 
                         (self.x + shadow_offset, self.y + shadow_offset, self.width, self.height), 
                         border_radius=self.radius)
        
        # Draw the background of the button
        pygame.draw.rect(screen, self.background, 
                         (self.x, self.y, self.width, self.height), 
                         border_radius=self.radius)
        
        # Draw the button itself (smaller rectangle for padding effect)
        pygame.draw.rect(screen, self.color, 
                         (self.x + self.padding, self.y + self.padding, 
                          self.width - self.padding * 2, self.height - self.padding * 2), 
                         border_radius=self.radius)

        # Draw the text on the button
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)
                         

    def is_clicked(self, mouse_pos):
        # Check if mouse click is inside the button (click detection)
        return (self.x <= mouse_pos[0] <= self.x + self.width and
                self.y <= mouse_pos[1] <= self.y + self.height)

    def is_hovered(self, mouse_pos):
        # Check if the mouse is hovering over the button
        return (self.x <= mouse_pos[0] <= self.x + self.width and
                self.y <= mouse_pos[1] <= self.y + self.height)

    def handle_hover_effect(self, mouse_pos):
        # This method could be used to handle hover effects (like changing color)
        if self.is_hovered(mouse_pos):
            hover_color = tuple(min(c + 30, 255) for c in self.color)  # Lighten the button when hovered
            pygame.draw.rect(screen, hover_color, 
                             (self.x + self.padding, self.y + self.padding, 
                              self.width - self.padding * 2, self.height - self.padding * 2), 
                             border_radius=self.radius)
