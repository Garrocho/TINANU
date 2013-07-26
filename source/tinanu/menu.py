#! /usr/bin/env python

import pygame, sys
from pygame.locals import *

from ezmenu import *
import media
import os


def NovoJogo(screen):
    pass
    #media.executar_musica("musica.ogg", 0.75)
    #Game(screen)
    #play_music("title.ogg", 0.75)


def Continuar(screen):
    pass
    #Game(screen, True)
    #play_music("title.ogg", 0.75)


class Menu(object):    

    def __init__(self, screen):
        media.executar_musica("menu.ogg", 0.75)
        self.screen = screen
        self.menu = EzMenu(["Novo Jogo", lambda: NovoJogo(screen)], ["Continuar", lambda: Continuar(screen)], ["Sair", sys.exit])
        self.menu.set_highlight_color((255, 0, 0))
        self.menu.set_normal_color((255, 255, 255))
        self.menu.center_at(300, 400)
        self.clock = pygame.time.Clock()
        events = pygame.event.get()
        self.menu.update(events)
        self.menu.draw(self.screen)
        self.bg = media.carrega_imagem_menu('menu_background.png')
        self.fonteGrande = pygame.font.Font(media.carrega_fonte("321impact.ttf"), 72)
        self.main_loop()

    def main_loop(self):
        while 1:
            self.clock.tick(40)
            events = pygame.event.get()
            self.menu.update(events)
            for e in events:
                if e.type == QUIT:
                    pygame.quit()
                    pass
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    pygame.quit()
                    pass
            
            self.screen.blit(self.bg, (0, 0))

            ren = self.fonteGrande.render("Tiro nas Nuvens", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 180))

            self.menu.draw(self.screen)
            pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    pygame.mouse.set_visible(0)
    pygame.display.set_caption("Tiro nas Nuvens")
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    Menu(screen)