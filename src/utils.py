import pygame
from PIL import Image, ImageSequence
import math  
from .settings import ASSETS_DIR

def scale_pixel_art(image, factor):
    """Escala por un factor entero, sin interpolar (bordes nítidos)."""
    w, h = image.get_size()
    return pygame.transform.scale(image, (w * factor, h * factor))

def load_image(name, scale=1, alpha=True):
    image = pygame.image.load(ASSETS_DIR / name)
    image = image.convert_alpha() if alpha else image.convert()
    return scale_pixel_art(image, scale) if scale != 1 else image

def load_cover(name, size, smooth=True, focus_x=0.5, focus_y=0.5):
    """Escala manteniendo la proporción hasta cubrir `size` y recorta lo que sobra.
    focus_x / focus_y: 0 = pegado a izquierda/arriba, 1 = derecha/abajo."""
    image = pygame.image.load(ASSETS_DIR / name).convert()
    iw, ih = image.get_size()
    ratio = max(size[0] / iw, size[1] / ih)
    new_size = (math.ceil(iw * ratio), math.ceil(ih * ratio))

    scaler = pygame.transform.smoothscale if smooth else pygame.transform.scale
    image = scaler(image, new_size)

    x = int((new_size[0] - size[0]) * focus_x)
    y = int((new_size[1] - size[1]) * focus_y)
    return image.subsurface((x, y, size[0], size[1])).copy()

def load_gif_frames(name, scale=1):
    """Devuelve (lista de Surfaces, lista de duraciones en segundos)."""
    gif = Image.open(ASSETS_DIR / name)
    frames, durations = [], []
    for frame in ImageSequence.Iterator(gif):
        durations.append(max(frame.info.get("duration", 100), 20) / 1000)
        rgba = frame.convert("RGBA")
        surface = pygame.image.frombytes(rgba.tobytes(), rgba.size, "RGBA").convert_alpha()
        frames.append(scale_pixel_art(surface, scale) if scale != 1 else surface)
    return frames, durations
