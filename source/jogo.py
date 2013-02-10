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


class Tiro( GameObject ):
    def __init__( self, posicao, velocidade=None, end_imagem='./imagens/tiro.png', lista=None ):
        GameObject.__init__( self, end_imagem, posicao, velocidade )
        if lista != None:
            self.add( lista )
    # __init__()
# Tiro


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

   def tiro( self, lista_tiros, end_imagem=None ):
        s = list( self.get_velocidade() )
        s[ 1 ] *= 2
        Tiro( self.get_posicao(), s, end_imagem, lista_tiros )
    # tiro()

    def do_hit( self ):
        if self.get_vidas() == 0:
            self.kill()
        else:
            self.set_vidas( self.get_vidas() - 1 )
    # do_hit()

    def do_collision( self ):
        if self.get_vidas() == 0:
            self.kill()
        else:
            self.set_vidas( self.get_vidas() - 1 )
    # do_collision()

    def is_dead( self ):
        return self.get_vidas() == 0
    # is_dead()

    def accel_top( self ):
        velocidade = self.get_velocidade()
        self.set_velocidade( ( velocidade[ 0 ], velocidade[ 1 ] - self.acceleration[ 1 ] ) )
    # accel_top

    def accel_bottom( self ):
        velocidade = self.get_velocidade()
        self.set_velocidade( ( velocidade[ 0 ], velocidade[ 1 ] + self.acceleration[ 1 ] ) )
    # accel_bottom

    def accel_left( self ):        
        velocidade = self.get_velocidade()
        self.set_velocidade( ( velocidade[ 0 ] - self.acceleration[ 0 ], velocidade[ 1 ] ) )
    # accel_left

    def accel_right( self ):
        velocidade = self.get_velocidade()
        self.set_velocidade( ( velocidade[ 0 ] + self.acceleration[ 0 ], velocidade[ 1 ] ) )
    # accel_right
# Nave


class Inimigo( Nave ):
    def __init__( self, posicao, vidas=0, velocidade=None, end_imagem='./imagens/inimigo.png' ):
        Nave.__init__( self, posicao, vidas, velocidade, end_imagem )
    # __init__()
# Inimigo


class Jogador( Nave ):
    """
    A classe Jogador é uma classe derivada da classe GameObject.
    """

    def __init__( self, posicao, vidas=10, end_imagem='./imagens/nave.png' ):
        Nave.__init__( self, posicao, vidas, [ 0, 0 ], end_imagem )
        self.set_XP( 0 )
    # __init__()

    def update( self, dt ):
        velocidade_mov = ( self.velocidade[ 0 ] * dt / 16, self.velocidade[ 1 ] * dt / 16)
        self.rect  = self.rect.move( velocidade_mov )
        
        if ( self.rect.right > self.area.right ):
            self.rect.right = self.area.right
            
        elif ( self.rect.left < 0 ):
            self.rect.left = 0
            
        if ( self.rect.bottom > self.area.bottom ):
            self.rect.bottom = self.area.bottom
            
        elif ( self.rect.top < 0 ):
            self.rect.top = 0
    # update()
    
    def get_posicao( self ):
        return ( self.rect.center[ 0 ], self.rect.top )
    # get_posicao()
    
    def get_XP( self ):
        return self.XP
    # get_XP()

    def set_XP( self, XP ):
        self.XP = XP
    # get_XP()

    def tiro( self, lista_tiros, end_imagem=None ):
        l = 1
        if self.XP > 10: l = 3
        if self.XP > 50: l = 5
        
        posicao     = self.get_posicao()
        velocidades = self.get_velocidade_tiro( l )
        for velocidade in velocidades:
            Tiro( posicao, velocidade, end_imagem, lista_tiros )
    # tiro()

    def get_velocidade_tiro( self, municao ):
        velocidades = []

        if municao <= 0:
            return velocidades
        
        if municao == 1:
            velocidades += [ (  0, -5 ) ]
            
        if municao > 1 and municao <= 3:
            velocidades += [ (  0, -5 ) ]
            velocidades += [ ( -2, -3 ) ]
            velocidades += [ (  2, -3 ) ]
            
        if municao > 3 and municao <= 5:
            velocidades += [ (  0, -5 ) ]
            velocidades += [ ( -2, -3 ) ]
            velocidades += [ (  2, -3 ) ]
            velocidades += [ ( -4, -2 ) ]
            velocidades += [ (  4, -2 ) ]

        return velocidades
    # get_velocidade_tiro()
# Jogador


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
    # init()

    def handle_events( self ):
        """
        Trata o evento e toma a ação necessária.
        """
        player = self.player

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
                    self.interval = 0
                    player.fire( self.list[ "fire" ] )
                elif k == K_UP:
                    player.accel_top()
                elif k == K_DOWN:
                    player.accel_bottom()
                elif k == K_RIGHT:
                    player.accel_right()
                elif k == K_LEFT:
                    player.accel_left()
        
            elif t == KEYUP:
                if   k == K_DOWN:
                    player.accel_top()
                elif k == K_UP:
                    player.accel_bottom()
                elif k == K_LEFT:
                    player.accel_right()
                elif k == K_RIGHT:
                    player.accel_left()
        
            keys = pygame.key.get_pressed()
            if self.interval > 10:
                self.interval = 0
                if keys[ K_RCTRL ] or keys[ K_LCTRL ]:
                    player.fire( self.list[ "fire" ] )        
    # handle_events()

    def atores_update( self, dt ):
        self.background.update( dt )
        for ator in self.lista.values():
            ator.update( dt )
    # atores_update()

    def atores_draw( self ):
        self.background.draw( self.screen )
        for ator in self.lista.values():
            ator.draw( self.screen )
    # atores_draw()

    def ator_check_hit( self, ator, lista, acao ):
        if isinstance( ator, pygame.sprite.RenderPlain ):
            hitted = pygame.sprite.groupcollide( ator, lista, 1, 0 )
            for v in hitted.values():
                for o in v:
                    action( o )
            return hitted

        elif isinstance( ator, pygame.sprite.Sprite ):
            if pygame.sprite.spritecollide( ator, lista, 1 ):
                action()
            return ator.is_dead()
    # ator_check_hit()

    def actors_act( self ):
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
        xp = self.jogaror.get_XP()
        if xp > 10  and self.level == 0:
            self.background = Background( "tile2.png" )
            self.level = 1
            self.jogador.set_vidas( self.jogador.get_vidas() + 3 )
        elif xp > 50  and self.level == 1:
            self.background = Background( "tile3.png" )
            self.level = 2        
            self.jogador.set_vidas( self.jogador.get_vidas() + 6 )
    # modifica_level()

    def manage( self ):
        self.ticks += 1
        # Faz os inimigos atirarem aleatóriamente
        if self.ticks > random.randint( 20, 30 ):
            for enemy in self.lista[ "inimigos" ].sprites():
                if Random.randint( 0, 10 ) > 5:
                    inimigo.tiro( self.lista[ "tiro_inimigo" ], end_imagem="./imagens/tiro_inimigo.png" )
                    self.ticks = 0
        
        # criamos mais inimigos randomicamente para o jogo não ficar chato
        r = random.randint( 0, 100 )
        x = random.randint( 1, self.screen_size[ 0 ] / 20 )
        if ( r > ( 40 * len( self.lista[ "inimigos" ] ) ) ):
            enemy = Inimigo( [ 0, 0 ] )
            size  = inimigo.get_size()
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
        self.background = Background( "tile.png" )

        # Inicializamos o relogio e o dt que vai limitar o valor de
        # frames por segundo do jogo
        clock          = pygame.time.Clock()
        dt             = 16
        self.ticks     = 0
        self.intervalo = 1

        posicao      = [ self.screen_size[ 0 ] / 2, self.screen_size[ 1 ] ]
        self.jogador = Jogador( posicao, vidas=10 )

        self.lista = {
            "jogador"       : pygame.sprite.RenderPlain( self.jogador ),
            "inimigos"      : pygame.sprite.RenderPlain( Inimigo( [ 120, 0 ] ) ),
            "tiro"          : pygame.sprite.RenderPlain(),
            "tiro_inimigo"  : pygame.sprite.RenderPlain()
            }

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