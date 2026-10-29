import random
import pygame
from .settings import *
from .utils import load_gif_frames

class KelpAnimation:
    """Recursos compartidos por todos los obstáculos (se crea una sola vez)."""

    def __init__(self):
        sprites, self.durations = load_gif_frames("alga-idle-16x48.gif", scale=PIXEL_SCALE)
        self.width = sprites[0].get_width()

        # Columna de alto completo por frame (punta arriba, tronco repetido)
        self.frames = [self._build_column(s) for s in sprites]
        self.flipped = [pygame.transform.flip(f, False, True) for f in self.frames]

        # Máscaras: solo los píxeles visibles cuentan para colisionar
        self.masks = [pygame.mask.from_surface(f) for f in self.frames]
        self.flipped_masks = [pygame.mask.from_surface(f) for f in self.flipped]

        # Superficies rojas translúcidas para el modo debug
        red, clear = (255, 0, 0, 140), (0, 0, 0, 0)
        self.debug_surfs = [m.to_surface(setcolor=red, unsetcolor=clear) for m in self.masks]
        self.debug_flipped = [m.to_surface(setcolor=red, unsetcolor=clear) for m in self.flipped_masks]

        self.index = 0
        self.timer = 0.0

    @staticmethod
    def _build_column(sprite):
        """Dibuja el sprite arriba y repite su franja inferior hasta cubrir HEIGHT."""
        w, h = sprite.get_size()
        body_h = KELP_BODY_ROWS * PIXEL_SCALE
        body = sprite.subsurface((0, h - body_h, w, body_h))

        column = pygame.Surface((w, HEIGHT), pygame.SRCALPHA)
        column.blit(sprite, (0, 0))
        y = h
        while y < HEIGHT:
            column.blit(body, (0, y))
            y += body_h
        return column

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.durations[self.index]:
            self.timer = 0.0
            self.index = (self.index + 1) % len(self.frames)


class KelpPair:
    def __init__(self, x, animation):
        self.anim = animation
        self.width = animation.width
        self.x = float(x)
        self.gap_y = random.randint(
            KELP_MARGIN + KELP_GAP // 2,
            HEIGHT - KELP_MARGIN - KELP_GAP // 2,
        )
        self.passed = False
        self._update_positions()

    def _update_positions(self):
        self.bottom_pos = (int(self.x), self.gap_y + KELP_GAP // 2)
        self.top_pos = (int(self.x), self.gap_y - KELP_GAP // 2 - HEIGHT)

    def update(self, dt):
        self.x -= KELP_SPEED * dt
        self._update_positions()

    def collides_with(self, rect):
        i = self.anim.index
        seal_mask = pygame.Mask(rect.size, fill=True)
        parts = (
            (self.anim.flipped_masks[i], self.top_pos),
            (self.anim.masks[i], self.bottom_pos),
        )
        for mask, pos in parts:
            offset = (rect.x - pos[0], rect.y - pos[1])
            if mask.overlap(seal_mask, offset):
                return True
        return False

    def is_offscreen(self):
        return self.x + self.width < 0

    def draw(self, surface):
        i = self.anim.index
        surface.blit(self.anim.flipped[i], self.top_pos)
        surface.blit(self.anim.frames[i], self.bottom_pos)

    def draw_debug(self, surface):
        i = self.anim.index
        surface.blit(self.anim.debug_flipped[i], self.top_pos)
        surface.blit(self.anim.debug_surfs[i], self.bottom_pos)
