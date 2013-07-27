#! /usr/bin/env python
import pygame
import media

class EzMenu:

    def __init__(self, *vetor_funcoes_menu):

        self.vetor_funcoes_menu = vetor_funcoes_menu
        self.tiro = media.obter_som('item-menu.ogg')
        self.x = 0
        self.y = 0
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
        if self.posicao_atual > len(self.vetor_funcoes_menu)-1:
            self.posicao_atual = 0
        if self.posicao_atual < 0:
            self.posicao_atual = len(self.vetor_funcoes_menu)-1

    def set_pos(self, x, y):     
        self.x = x
        self.y = y
        
    def set_font(self, font):
        self.fonte = font
        
    def set_highlight_color(self, color):
        self.hcolor = color
        
    def set_normal_color(self, color):
        self.color = color
        
    def center_at(self, x, y):
        self.x = x-(self.width/2)
        self.y = y-(self.height/2)
