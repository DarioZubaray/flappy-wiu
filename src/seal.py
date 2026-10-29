import math
import pygame
from .settings import *
from .utils import load_image

class Seal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.idle_frames = [
            load_image("sprites/foca-perfil-1.png", scale=PIXEL_SCALE),
            load_image("sprites/foca-perfil-2.png", scale=PIXEL_SCALE),
        ]
        self.look_frames = [
            load_image("sprites/foca-perfil-mirando-1.png", scale=PIXEL_SCALE),
            load_image("sprites/foca-perfil-mirando-2.png", scale=PIXEL_SCALE),
        ]
        self.reset()

    def reset(self):
        self.frame_index = 0
        self.anim_timer = 0
        self.flap_timer = 0
        self.vel_y = 0
        self.bob_time = 0
        self.base_y = HEIGHT / 2
        self.pos_y = self.base_y
        self.x = self.target_x = SEAL_X
        self.image = self.idle_frames[0]
        self._update_rects()

    def _update_rects(self):
        self.rect = self.image.get_rect(center=(round(self.x), round(self.pos_y)))
        visible = self.image.get_bounding_rect(min_alpha=50)
        self.hitbox = visible.move(self.rect.topleft).inflate(
            -SEAL_HITBOX_SHRINK[0], -SEAL_HITBOX_SHRINK[1]
        )

    def flap(self):
        self.vel_y = FLAP_SPEED
        self.flap_timer = FLAP_ANIM_TIME
        self.frame_index = 0      # la animación "mirando" arranca siempre desde el inicio
        self.anim_timer = 0

    def update(self, dt, apply_physics=True):
        # Deslizamiento suave hacia target_x (menú -> posición de juego)
        self.x += (self.target_x - self.x) * min(1, 6 * dt)

        if apply_physics:
            self.vel_y += GRAVITY * dt
            self.pos_y += self.vel_y * dt
        else:
            # Flotación en menú y espera
            self.bob_time += dt
            self.pos_y = self.base_y + math.sin(self.bob_time * 3) * 8

        if self.flap_timer > 0:
            self.flap_timer -= dt
            frames = self.look_frames
        else:
            frames = self.idle_frames

        self.anim_timer += dt
        if self.anim_timer >= SEAL_ANIM_SPEED:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % len(frames)

        self.image = frames[self.frame_index % len(frames)]
        self._update_rects()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def draw_debug(self, surface):
        pygame.draw.rect(surface, (80, 160, 255), self.rect, 1)
        pygame.draw.rect(surface, (0, 255, 0), self.hitbox, 2)
