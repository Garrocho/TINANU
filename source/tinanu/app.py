# -*- coding: utf-8 -*-
# @author: Charles Tim Batista Garrocho
# @contact: ccharles.garrocho@gmail.com
# @copyright: (C) 2013 - 2013 Python Software Open Source

"""
Este é o módulo responsável definir as configurações e iniciar o jogo.
"""


import motor


if __name__ == '__main__':
    game = motor.Game()
    game.loop()