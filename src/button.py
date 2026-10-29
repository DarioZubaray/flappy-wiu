import pygame

class Button:
    def __init__(self, text, center, font, size=(170, 48)):
        self.text = text
        self.font = font
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = center
        self.enabled = True

    def is_clicked(self, event):
        return (
            self.enabled
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

    def draw(self, surface):
        hovered = self.enabled and self.rect.collidepoint(pygame.mouse.get_pos())
        if not self.enabled:
            fill, text_color = (70, 70, 80), (150, 150, 160)
        elif hovered:
            fill, text_color = (60, 150, 200), (255, 255, 255)
        else:
            fill, text_color = (30, 110, 160), (255, 255, 255)

        pygame.draw.rect(surface, fill, self.rect, border_radius=10)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=10)
        label = self.font.render(self.text, True, text_color)
        surface.blit(label, label.get_rect(center=self.rect.center))
