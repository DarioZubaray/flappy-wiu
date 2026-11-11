# Flappy Wiu

"Flappy Wiu" es un clon del popular juego [Flappy Bird](https://es.wikipedia.org/wiki/Flappy_Bird) pero en este caso protagonizado por una foca, hecho con **pygame-ce**, en pixel art y con ventana vertical de 360x640 (proporcional a un celular). 

Es una app de escritorio, pero todo está pensado para que funcione con un solo gesto (click o tap). 

El requisito de diseño de partida fue **programación orientada a objetos**: `main.py` solo arranca, y cada responsabilidad vive en su propia clase.

**Pasos para la creación**

Crear un nuevo ambiente(opcional), instalando pygame-ce:
```
# 1. Crear el ambiente virtual (llamado .venv)
python -m venv .venv

# 2. Activar el ambiente
# En Windows (Command Prompt):
.venv\Scripts\activate.ps1

# 3. Instalar las librerias dentro del ambiente
pip install pygame-ce pillow
```

**Pasos para colaboración**
Luego de descargado el código, descargar las dependencias:
```
pip install -r requirements.txt
```

**Ejecutar (dentro del ambiente)**

```
(.venv) python main.py
```

**Controles**

| Acción | Teclado | Mouse / tap |
| --- | --- | --- |
| Empezar desde el menú | ENTER | botón JUGAR |
| Saltar / empezar a jugar | ESPACIO | click |
| Reiniciar tras perder | ENTER o R | botón REINICIAR (arriba) |
| Silenciar todo | M | — |
| Modo debug (hitboxes) | F1 | — |
| Salir | ESC | cerrar ventana |

**Mejoras posibles**

- Guardar el puntaje final luego del cierre de la app.
- Botón de volver al menú desde Game Over.
- Scroll horizontal del fondo (parallax).

**Estructura del proyecto**

```
proyecto/
├── main.py            # punto de entrada: crea Game y llama run()
├── assets/            # bg.jpg, foca-*.png, kelp.gif, 2 MP3 + sonido de colisión
└── src/
    ├── settings.py    # TODAS las constantes (física, tamaños, audio)
    ├── utils.py       # carga y escalado de imágenes / GIF
    ├── seal.py        # clase Seal  (jugador)
    ├── kelp.py        # clases KelpAnimation y KelpPair (obstáculos)
    ├── button.py      # clase Button (UI)
    ├── audio.py       # clase AudioManager (música y efectos)
    └── game.py        # clase Game  (orquestador y bucle principal)
```

`main.py` es deliberadamente mínimo:

```python
from src.game import Game

if __name__ == '__main__':
    Game().run()
```

**Arquitectura**

`Game` es el único que conoce a todos; el resto de las clases no se conocen entre sí. Las dependencias van en una sola dirección.

**El bucle principal**

Dentro de `game.py`, es la función que se llama desde `main.py`

```python
def run(self):
    while True:
        dt = self.clock.tick(FPS) / 1000   # segundos desde el frame anterior
        self.handle_events()
        self.update(dt)
        self.draw()
```