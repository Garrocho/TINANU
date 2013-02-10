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



if __name__ == '__main__':
    game = Game()
    game.loop()
