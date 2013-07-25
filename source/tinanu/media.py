# -*- coding: utf-8 -*-
# @author: Charles Tim Batista Garrocho
# @contact: ccharles.garrocho@gmail.com
# @copyright: (C) 2013 - 2013 Python Software Open Source

"""
Este é o módulo responsável por realizar o carregamento dos endereços de fontes, imagens e sons do jogo.
"""


import os
import pygame
from os.path import join as join_path


dados_py  = os.path.abspath(os.path.dirname(__file__))
dados_dir = os.path.normpath(join_path(dados_py, '..', 'media'))


endereco_arquivos = dict(
    fontes  = join_path(dados_dir, 'fontes'),
    imagens = join_path(dados_dir, 'imagens'),
    sons = join_path(dados_dir, 'sons'),
)


def endereco_arquivo(tipo, nome_arquivo):
    return join_path(endereco_arquivos[tipo], nome_arquivo)


def carrega(tipo, nome_arquivo, modo='rb'):
	return open(endereco_arquivo(tipo, nome_arquivo), modo)


def carrega_fonte(nome_arquivo):
    return endereco_arquivo('fontes', nome_arquivo)

def carrega_imagem(nome_arquivo):
	return endereco_arquivo('imagens', nome_arquivo)

def carrega_imagem_menu(nome_arquivo):
	filename = carrega('imagens', nome_arquivo)
	try:
		image = pygame.image.load(filename)
		return image
		image = pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2))
	except pygame.error:
		raise SystemExit, "Unable to load: " + filename
	return image


def carrega_son(nome_arquivo):
    return carrega('sons', nome_arquivo)