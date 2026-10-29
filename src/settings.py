from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"

WIDTH, HEIGHT = 360, 640   # celular en vertical
DEBUG = False              # F1 lo alterna mientras jugás
FPS = 60

PIXEL_SCALE = 4        # factor entero para TODOS los sprites

# Física (píxeles y segundos)
GRAVITY = 1500
FLAP_SPEED = -420
FLAP_ANIM_TIME = 1     # cuánto dura la imagen "mirando" tras un click

# Foca
SEAL_HEIGHT = 50
SEAL_X = 100
# Tolerancia extra sobre la foca visible (en píxeles escalados).
# Más grande = hitbox más chico = juego más permisivo.
SEAL_HITBOX_SHRINK = (3 * PIXEL_SCALE, 2 * PIXEL_SCALE)
SEAL_ANIM_SPEED = 0.2     # segundos entre frame y frame

# Algas
KELP_WIDTH = 70
KELP_GAP = 170
KELP_SPEED = 180
KELP_SPAWN_TIME = 1.8
KELP_MARGIN = 100
KELP_BODY_ROWS = 8     # filas (del sprite original) que se repiten hacia abajo

RESTART_LOCK = 0.6   # segundos que no se puede reiniciar tras perder

# Musica & Audio
JUMP_SOUND = "freesound_community-cartoon-jump-6462.mp3"
MUSIC_FILE = "Seal Arpeggio.mp3"
JUMP_VOLUME = 0.6
MUSIC_VOLUME = 0.4
