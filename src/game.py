import sys
import pygame
from .settings import *
from .utils import load_cover
from .seal import Seal
from .kelp import KelpAnimation, KelpPair
from .button import Button
from .audio import AudioManager, MUSIC_RESTART_EVENT

class Game:
    MENU, READY, PLAYING, GAME_OVER = "menu", "ready", "playing", "game_over"

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flappy Wiu")
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        self.debug = DEBUG

        self.background = load_cover("sprites/bg.jpg", (WIDTH, HEIGHT))
        self.kelp_anim = KelpAnimation()   # requiere display ya creado
        self.seal = Seal()
        self.audio = AudioManager()
        self.audio.play_music()

        self.play_button = Button("JUGAR", (WIDTH // 2, 440), self.font, size=(200, 60))
        self.restart_button = Button("REINICIAR", (WIDTH // 2, 110), self.small_font)

        self.best_score = 0
        self.show_menu()

    # ---------- Estados ----------
    def show_menu(self):
        self.reset()
        self.state = self.MENU
        self.seal.x = self.seal.target_x = WIDTH // 2   # foca centrada en el menú

    def start_game(self):
        self.state = self.READY
        self.seal.target_x = SEAL_X                      # se desliza a su sitio

    def reset(self):
        """Prepara una partida nueva (queda en espera, sin pasar por el menú)."""
        self.state = self.READY
        self.score = 0
        self.kelps = []
        self.spawn_timer = KELP_SPAWN_TIME
        self.game_over_timer = 0.0
        self.seal.reset()

    def game_over(self):
        if self.state == self.GAME_OVER:
            return
        self.state = self.GAME_OVER
        self.game_over_timer = 0.0
        self.best_score = max(self.best_score, self.score)
        self.audio.play_collision()

    def can_restart(self):
        return self.state == self.GAME_OVER and self.game_over_timer >= RESTART_LOCK

    def flap(self):
        self.seal.flap()
        self.audio.play_jump()

    # ---------- Eventos ----------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                elif event.key == pygame.K_F1:
                    self.debug = not self.debug
                elif event.key == pygame.K_m:
                    self.audio.toggle_mute()
                elif event.key == pygame.K_SPACE:
                    self.on_input()
                elif event.key == pygame.K_RETURN and self.state == self.MENU:
                    self.start_game()
                elif event.key in (pygame.K_RETURN, pygame.K_r) and self.can_restart():
                    self.reset()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == self.MENU:
                    if self.play_button.is_clicked(event):
                        self.start_game()
                elif self.state == self.GAME_OVER:
                    if self.restart_button.is_clicked(event) and self.can_restart():
                        self.reset()
                else:
                    self.on_input()

            elif event.type == MUSIC_RESTART_EVENT:
                self.audio.restart_music()

    def on_input(self):
        """Salto / inicio de partida. En menú y Game Over no hace nada."""
        if self.state == self.READY:
            self.state = self.PLAYING
            self.flap()
        elif self.state == self.PLAYING:
            self.flap()

    # ---------- Lógica ----------
    def update(self, dt):
        if self.state in (self.MENU, self.READY):
            self.seal.update(dt, apply_physics=False)
            return
        if self.state == self.GAME_OVER:
            self.game_over_timer += dt
            self.restart_button.enabled = self.can_restart()
            return

        self.kelp_anim.update(dt)
        self.seal.update(dt)
        self.spawn_kelps(dt)

        for kelp in self.kelps:
            kelp.update(dt)
            if not kelp.passed and kelp.x + kelp.width < self.seal.rect.left:
                kelp.passed = True
                self.score += 1
            if kelp.collides_with(self.seal.hitbox):
                self.game_over()

        self.kelps = [k for k in self.kelps if not k.is_offscreen()]

        if self.seal.hitbox.top < 0 or self.seal.hitbox.bottom > HEIGHT:
            self.game_over()

    def spawn_kelps(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer >= KELP_SPAWN_TIME:
            self.spawn_timer = 0
            self.kelps.append(KelpPair(WIDTH + 20, self.kelp_anim))

    # ---------- Dibujo ----------
    def draw_text(self, text, font, y):
        surf = font.render(text, True, (255, 255, 255))
        shadow = font.render(text, True, (0, 0, 0))
        rect = surf.get_rect(center=(WIDTH // 2, y))
        self.screen.blit(shadow, rect.move(2, 2))
        self.screen.blit(surf, rect)

    def draw_menu(self):
        self.draw_text("Flappy Wiu", self.title_font, 140)
        self.draw_text(f"Récord: {self.best_score}", self.small_font, 200)
        self.play_button.draw(self.screen)
        self.draw_text("ENTER para jugar", self.small_font, 500)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        for kelp in self.kelps:
            kelp.draw(self.screen)
        self.seal.draw(self.screen)

        if self.debug:
            for kelp in self.kelps:
                kelp.draw_debug(self.screen)
            self.seal.draw_debug(self.screen)
            self.draw_text("DEBUG (F1)", self.small_font, HEIGHT - 15)

        if self.state == self.MENU:
            self.draw_menu()
        else:
            self.draw_text(str(self.score), self.font, 40)
            if self.state == self.READY:
                self.draw_text("Click o ESPACIO para empezar", self.small_font, HEIGHT - 50)
            elif self.state == self.GAME_OVER:
                self.draw_text("Game Over", self.font, HEIGHT // 2 - 20)
                self.draw_text(f"Récord: {self.best_score}", self.small_font, HEIGHT // 2 + 20)
                self.draw_text("ENTER o botón de arriba", self.small_font, HEIGHT // 2 + 48)
                self.restart_button.draw(self.screen)

        pygame.display.flip()

    # ---------- Bucle principal ----------
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()
