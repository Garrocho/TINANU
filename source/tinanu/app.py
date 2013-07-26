# -*- coding: utf-8 -*-
# @author: Charles Tim Batista Garrocho
# @contact: ccharles.garrocho@gmail.com
# @copyright: (C) 2013 - 2013 Python Software Open Source

"""
Este é o módulo responsável definir as configurações e iniciar o jogo.
"""


import menu
import pygame


if __name__ == '__main__':
    pygame.init()
    pygame.mouse.set_visible(0)
    pygame.display.set_caption("Tiro nas Nuvens")
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    menu.Menu(screen)