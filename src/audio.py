import pygame
from .settings import *

class AudioManager:
    def __init__(self):
        self.enabled = True
        self.muted = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.jump_sound = pygame.mixer.Sound(str(ASSETS_DIR / JUMP_SOUND))
            self.jump_sound.set_volume(JUMP_VOLUME)
            pygame.mixer.music.load(str(ASSETS_DIR / MUSIC_FILE))
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
        except (pygame.error, FileNotFoundError) as error:
            print(f"Audio desactivado: {error}")
            self.enabled = False

    def play_music(self):
        if self.enabled:
            pygame.mixer.music.play(loops=-1)   # -1 = bucle infinito

    def play_jump(self):
        if self.enabled and not self.muted:
            self.jump_sound.stop()   # si suena todavía, reinicia (salto más "crujiente")
            self.jump_sound.play()

    def toggle_mute(self):
        if not self.enabled:
            return
        self.muted = not self.muted
        pygame.mixer.music.set_volume(0 if self.muted else MUSIC_VOLUME)
