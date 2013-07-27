# -*- coding: utf-8 -*-
# @author: Charles Tim Batista Garrocho
# @contact: ccharles.garrocho@gmail.com
# @copyright: (C) 2013 - 2013 Python Software Open Source

"""
Este é o módulo responsável definir as configurações do menu inicial do jogo.
"""

import pygame, sys
from pygame.locals import *
import motor
import media


def novoJogo(screen):
    game = motor.Game(screen)
    game.loop()


class Menu(object):    

    def __init__(self, screen):
        media.executar_musica("menu.ogg", 0.75)
        self.screen = screen
        self.menu = NFMenu(["Novo Jogo", lambda: novoJogo(screen)], ["Sair", sys.exit])
        self.clock = pygame.time.Clock()
        events = pygame.event.get()
        self.menu.update(events)
        self.menu.draw(self.screen)
        self.bg = media.carrega_imagem_menu('menu_background.png')
        self.fonteGrande = pygame.font.Font(media.carrega_fonte("321impact.ttf"), 72)
        self.loop()

    def loop(self):
        while True:
            self.clock.tick(40)
            events = pygame.event.get()
            self.menu.update(events)
            self.screen.blit(self.bg, (0, 0))
            ren = self.fonteGrande.render("Tiro nas Nuvens", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 180))
            self.menu.draw(self.screen)
            pygame.display.flip()


class NFMenu:

    def __init__(self, *vetor_funcoes_menu):

        self.vetor_funcoes_menu = vetor_funcoes_menu
        self.tiro = media.obter_som('item-menu.ogg')
        self.hcolor = (255, 0, 0)
        self.fonte = pygame.font.Font(None, 32)
        self.posicao_atual = 0
        self.width = 1
        self.color = [0, 0, 0]
        self.hcolor = [255, 0, 0]
        self.height = len(self.vetor_funcoes_menu)*self.fonte.get_height()
        for funcao in self.vetor_funcoes_menu:
            texto = funcao[0]
            ren = self.fonte.render(texto, 1, (0, 0, 0))
            if ren.get_width() > self.width:
                self.width = ren.get_width()
        self.x = 300-(self.width/2)
        self.y = 400-(self.height/2)

    def draw(self, surface):
        i=0
        for funcao in self.vetor_funcoes_menu:
            if i==self.posicao_atual:
                clr = self.hcolor
            else:
                clr = self.color
            texto = funcao[0]
            ren = self.fonte.render(texto, 1, clr)
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            surface.blit(ren, ((self.x+self.width/2) - ren.get_width()/2, self.y + i*(self.fonte.get_height()+4)))
            i+=1
            
    def update(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    self.posicao_atual += 1
                    self.tiro.play()
                if e.key == pygame.K_UP:
                    self.posicao_atual -= 1
                    self.tiro.play()
                if e.key == pygame.K_RETURN:
                    self.vetor_funcoes_menu[self.posicao_atual][1]()
                if e.type == QUIT:
                    sys.exit()
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    sys.exit()
        if self.posicao_atual > len(self.vetor_funcoes_menu)-1:
            self.posicao_atual = 0
        if self.posicao_atual < 0:
            self.posicao_atual = len(self.vetor_funcoes_menu)-1