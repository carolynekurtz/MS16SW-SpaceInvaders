"""Configurações compartilhadas do Space Invaders."""

from pathlib import Path


# Diretórios do projeto. Os caminhos não dependem da pasta em que o jogo é iniciado.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"
FONTS_DIR = ASSETS_DIR / "fonts"

# Compatibilidade simples para os módulos que montam caminhos de recursos.
DIRECTORY = str(PROJECT_ROOT)
FONT = str(FONTS_DIR / "oxanium-semibold.ttf")

# Dimensões da janela.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Paleta clássica do jogo e cores da interface.
WHITE = (245, 246, 255)
RED = (255, 74, 112)
BLACK = (5, 7, 24)
GREEN = (68, 232, 255)
GOLD = (255, 100, 220)
SPRINGREEN = (80, 239, 255)
