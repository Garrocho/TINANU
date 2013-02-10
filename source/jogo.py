# -*- coding: utf-8 -*-

import pygame
import random
from math import ceil
from pygame.locals import *


class Background:
    """
    Esta classe representa o ator "Fundo" do jogo.
    """
    image = None
    
    def __init__( self ):
        image = pygame.image.load( './imagens/tile.jpg' )
        self.isize  = image.get_size()
        self.pos    = [ 0, -1 * self.isize[ 1 ] ]
        screen      = pygame.display.get_surface()
        screen_size = screen.get_size()

        largura = ( ceil( float( screen_size[ 0 ] ) / self.isize[ 0 ] ) + 1 ) * self.isize[ 0 ]
        altura  = ( ceil( float( screen_size[ 1 ] ) / self.isize[ 1 ] ) + 1 ) * self.isize[ 1 ]

        back = pygame.Surface( ( largura, altura ) )
        
        for i in range( ( back.get_size()[ 0 ] / self.isize[ 0 ] ) ):
            for j in range( ( back.get_size()[ 1 ] / self.isize[ 1 ] ) ):
                back.blit( image, ( i * self.isize[ 0 ], j * self.isize[ 1 ] ) )

        self.image = back
    # __init__()

    def update( self, dt ):
        self.pos[ 1 ] += 1
        if ( self.pos[ 1 ] > 0 ):
            self.pos[ 1 ] -= self.isize[ 1 ]
    # update()

    def draw( self, screen ):
        screen.blit( self.image, self.pos )
    # draw()
# Background


class GameObject( pygame.sprite.Sprite ):
    """
    Esta é a classe básica de todos os objetos do jogo.
    """

    def __init__( self, end_image, posicao, velocidade=None ):
        pygame.sprite.Sprite.__init__( self )
        self.image = pygame.image.load( end_image )

        self.rect  = self.image.get_rect()
        screen     = pygame.display.get_surface()
        self.area  = screen.get_rect()
        
        self.set_posicao( posicao )
        self.set_velocidade( velocidade or ( 0, 2 ) )
    # __init__()

    def update( self, dt ):
        velocidade_mov = ( self.velocidade[ 0 ] * dt / 16, self.velocidade[ 1 ] * dt / 16 )
        self.rect  = self.rect.move( velocidade_mov )
        if self.rect.left > self.area.right or self.rect.top > self.area.bottom or self.rect.right < 0:
            self.kill()
        if self.rect.bottom < -40:
            self.kill()
    # update()

    def get_velocidade( self ):
        return self.velocidade
    # get_velocidade()

    def set_velocidade( self, velocidade ):
        self.velocidade = velocidade
    # set_velocidade()

    def get_posicao( self ):
        return ( self.rect.center[ 0 ], self.rect.bottom )
    # get_posicao()

    def set_posicao( self, posicao ):
        self.rect.center = ( posicao[ 0 ], posicao[ 1 ] )
    # set_posicao()

    def get_size( self ):
        return self.image.get_size()
    # get_size()
# GameObject


class Nave( GameObject ):

    vidas = None

    def __init__( self, posicao, vidas=0, velocidade=[ 0, 0 ], end_imagem=None ):
        self.acceleration = [ 3, 3 ]
        GameObject.__init__( self, end_imagem, posicao, velocidade )
        self.set_vidas( vidas )
    # __init__()

    def get_vidas( self ):
        return self.vidas
    # get_vidas()

    def set_vidas( self, vidas ):
        self.vidas = vidas
    # set_vidas()
# Nave


class Inimigo( Nave ):
    def __init__( self, posicao, vidas=0, velocidade=None, end_imagem='./imagens/inimigo.png' ):
        Nave.__init__( self, posicao, vidas, velocidade, end_imagem )
    # __init__()
# Inimigo



if __name__ == '__main__':
    game = Game()
    game.loop()
