"""Ponto de entrada do jogo Space Invaders."""

import os

import pygame

from src.game import SpaceInvaders


def main():
    """Inicializa o Pygame e inicia o jogo."""
    os.environ.setdefault("SDL_VIDEO_CENTERED", "1")

    pygame.mixer.pre_init(22050, -16, 2, 1024)
    pygame.init()
    pygame.mixer.init(22050, -16, 2, 1024)

    try:
        game = SpaceInvaders()
        game.main()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
