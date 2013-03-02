# -*- coding: utf-8 -*-
"""
Este é o módulo responsável por toda interação dos atores no jogo.
"""

import copy
import pygame
import random
from pygame.locals import *
from atores import *


class JogadorXPStatus:
    """
    Esta classe representa a experiência do usuário
    """
    fonte   = None
    last_xp = -1
    fgcolor = None
    bgcolor = None
    imagem  = None
    
    def __init__( self, jogador, posicao=None, fonte=None, ptsize=30, fgcolor="0xffff00", bgcolor=None ):
        self.jogador = jogador
        self.fgcolor = pygame.color.Color( fgcolor )
        if bgcolor:
            self.bgcolor = pygame.color.Color( bgcolor )
        self.posicao = posicao or [ 0, 0 ]
        self.fonte   = pygame.font.Font( fonte, ptsize )
    # __init__()

    def update( self, dt ):
        pass
    # update()

    def draw( self, screen ):
        xp = self.jogador.get_XP()
        if self.last_xp != xp:
            self.last_xp = xp
            texto = "XP: % 4d" % xp
            if self.bgcolor:
                self.imagem = self.fonte.render( texto, True, self.fgcolor, self.bgcolor )
            else:                
                self.imagem = self.fonte.render( texto, True, self.fgcolor )
                
        screen.blit( self.imagem, self.posicao )   
    # draw()
# JogadorXPStatus


class JogadorVidaStatus:
    """
    Esta classe representa o contador de vidas do jogador
    """
    jogador    = None
    posicao    = None
    imagem     = None
    size_image = None
    spacing    = 5

    def __init__( self, jogador, posicao=None, end_imagem="./imagens/nave_status.png" ):
        self.imagem     = pygame.image.load( end_imagem )
        self.jogador    = jogador
        self.posicao    = posicao or [ 5, 5 ]
        self.size_image = self.imagem.get_size()
    # __init__()

    def update( self, dt ):
        pass
    # update()

    def draw( self, screen ):
        posicao = copy.copy( self.posicao )
        for i in range( self.jogador.get_vidas() ):
            posicao[ 0 ] += self.size_image[ 0 ] + self.spacing
            screen.blit( self.imagem, posicao )
    # draw()
# JogadorVidaStatus


class Game:
    screen      = None
    screen_size = None
    run         = True
    intervalo   = 0
    level       = 0
    lista       = None
    jogador     = None
    background  = None  
    
    def __init__( self ):
        """
        Esta é a função que inicializa o pygame, define a resolução da tela,
        caption, e disabilitamos o mouse dentro desta.
        """
        atores = {}
        pygame.init()
        self.screen      = pygame.display.set_mode( (850, 700) )
        self.screen_size = self.screen.get_size()

        pygame.mouse.set_visible( 0 )
        pygame.display.set_caption( 'TINANU - Tiro nas Nuvens' )
        self.carrega_imagens()
    # init()

    def carrega_imagens( self ):
        """
        Lê as imagens necessarias pelo jogo.
        """
        self.imagem_jogador      = pygame.image.load( "./imagens/nave.png" )
        self.imagem_inimigo      = pygame.image.load( "./imagens/inimigo.png" )
        self.imagem_tiro         = pygame.image.load( "./imagens/tiro.png" )
        self.imagem_tiro_inimigo = pygame.image.load( "./imagens/tiro_inimigo.png" )
    # carrega_imagens()

    def handle_events( self ):
        """
        Trata o evento e toma a ação necessária.
        """
        jogador = self.jogador

        for event in pygame.event.get():
            t = event.type
            if t in ( KEYDOWN, KEYUP ):
                k = event.key
        
            if t == QUIT:
                self.run = False

            elif t == KEYDOWN:
                if   k == K_ESCAPE:
                    self.run = False
                elif k == K_LCTRL or k == K_RCTRL:
                    self.intervalo = 0
                    jogador.tiro( lista_tiros = self.lista[ "tiros" ], imagem = self.imagem_tiro )
                elif k == K_UP:
                    jogador.accel_top()
                elif k == K_DOWN:
                    jogador.accel_bottom()
                elif k == K_RIGHT:
                    jogador.accel_right()
                elif k == K_LEFT:
                    jogador.accel_left()
        
            elif t == KEYUP:
                if   k == K_DOWN:
                    jogador.accel_top()
                elif k == K_UP:
                    jogador.accel_bottom()
                elif k == K_LEFT:
                    jogador.accel_right()
                elif k == K_RIGHT:
                    jogador.accel_left()
        
            keys = pygame.key.get_pressed()
            if self.intervalo > 10:
                self.intervalo = 0
                if keys[ K_RCTRL ] or keys[ K_LCTRL ]:
                    jogador.tiro( self.lista[ "tiros" ], self.imagem_tiro )        
    # handle_events()

    def atores_update( self, dt ):
        self.background.update( dt )
        for ator in self.lista.values():
            ator.update( dt )
        self.jogador_vida.update( dt )
        self.jogador_xp.update( dt )
    # atores_update()

    def atores_draw( self ):
        self.background.draw( self.screen )
        for ator in self.lista.values():
            ator.draw( self.screen )
        self.jogador_vida.draw( self.screen )
        self.jogador_xp.draw( self.screen )
    # atores_draw()

    def ator_check_hit( self, ator, lista, acao ):
        if isinstance( ator, pygame.sprite.RenderPlain ):
            hitted = pygame.sprite.groupcollide( ator, lista, 1, 0 )
            for v in hitted.values():
                for o in v:
                    acao( o )
            return hitted

        elif isinstance( ator, pygame.sprite.Sprite ):
            if pygame.sprite.spritecollide( ator, lista, 1 ):
                acao()
            return ator.is_dead()
    # ator_check_hit()

    def atores_act( self ):
        # Verifica se personagem foi atingido por um tiro
        self.ator_check_hit( self.jogador, self.lista[ "tiro_inimigo" ], self.jogador.do_hit )
        if self.jogador.is_dead():
            self.run = False
            return

        # Verifica se o personagem trombou em algum inimigo
        self.ator_check_hit( self.jogador, self.lista[ "inimigos" ], self.jogador.do_collision )
        if self.jogador.is_dead():
            self.run = False
            return

        # Verifica se o personagem atingiu algum alvo.
        hitted = self.ator_check_hit( self.lista[ "tiros" ], self.lista[ "inimigos" ], Inimigo.do_hit )
        
        # Aumenta a eXPeriência baseado no número de acertos:
        self.jogador.set_XP( self.jogador.get_XP() + len( hitted ) )
    # atores_check_hit()

    def modifica_level( self ):
        xp = self.jogador.get_XP()
        if xp > 2  and self.level == 0:
            self.background = Background( "./imagens/tile2.jpg" )
            self.level = 1
            self.jogador.set_vidas( self.jogador.get_vidas() + 3 )
        elif xp > 5  and self.level == 1:
            self.background = Background( "./imagens/tile3.jpg" )
            self.level = 2        
            self.jogador.set_vidas( self.jogador.get_vidas() + 6 )
        elif xp > 10  and self.level == 2:
            self.background = Background( "./imagens/tile4.jpg" )
            self.level = 3      
            self.jogador.set_vidas( self.jogador.get_vidas() + 9 )
    # modifica_level()

    def manage( self ):
        self.ticks += 1
        # Faz os inimigos atirarem aleatóriamente
        if self.ticks > random.randint( 20, 30 ):
            for inimigo in self.lista[ "inimigos" ].sprites():
                if random.randint( 0, 10 ) > 5:
                    inimigo.tiro( self.lista[ "tiro_inimigo" ], imagem = self.imagem_tiro_inimigo )
                    self.ticks = 0
        
        # criamos mais inimigos randomicamente para o jogo não ficar chato
        r = random.randint( 0, 100 )
        x = random.randint( 1, self.screen_size[ 0 ] / 20 )
        if ( r > ( 40 * len( self.lista[ "inimigos" ] ) ) ):
            inimigo = Inimigo( posicao = [ 0, 0 ], imagem = self.imagem_inimigo )
            size    = inimigo.get_size()
            inimigo.set_posicao( [ x * size[ 0 ], - size[ 1 ] ] )
            self.lista[ "inimigos" ].add( inimigo )

        # Verifica se ascendeu de nível
        self.modifica_level()
    # manage()

    def loop( self ):
        """
        Laço principal
        """
        # Criamos o fundo
        self.background = Background( "./imagens/tile.jpg" )

        # Inicializamos o relogio e o dt que vai limitar o valor de
        # frames por segundo do jogo
        clock          = pygame.time.Clock()
        dt             = 16
        self.ticks     = 0
        self.intervalo = 1

        posicao      = [ self.screen_size[ 0 ] / 2, self.screen_size[ 1 ] ]
        self.jogador = Jogador( posicao, vidas=10, imagem = self.imagem_jogador )

        self.lista = {
            "jogador"       : pygame.sprite.RenderPlain( self.jogador ),
            "inimigos"      : pygame.sprite.RenderPlain( Inimigo( posicao = [ 120, 0 ], imagem = self.imagem_inimigo ) ),
            "tiros"         : pygame.sprite.RenderPlain(),
            "tiro_inimigo"  : pygame.sprite.RenderPlain()
            }

        self.jogador_vida = JogadorVidaStatus( self.jogador, [ 5, 5 ] )
        self.jogador_xp   = JogadorXPStatus( self.jogador, [ self.screen_size[ 0 ] - 100, 5 ], fgcolor="0xff0000" )

        # assim iniciamos o loop principal do programa
        while self.run:
            clock.tick( 1000 / dt )
            self.intervalo += 1

            # Handle Input Events
            self.handle_events()

            # Atualiza Elementos
            self.atores_update( dt )

            # Faça os atores atuarem
            self.atores_act()

            # Faça a manutenção do jogo, como criar inimigos, etc.
            self.manage()
            
            # Desenhe para o back buffer
            self.atores_draw()
            
            # ao fim do desenho temos que trocar o front buffer e o back buffer
            pygame.display.flip()
        # while self.run
    # loop()
# Game


if __name__ == '__main__':
    game = Game()
    game.loop()