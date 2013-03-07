# -*- coding: utf-8 -*-
# @author: Charles Tim Batista Garrocho
# @contact: ccharles.garrocho@gmail.com
# @copyright: (C) 2013 - 2013 Python Software Open Source

"""
Este é o módulo responsável por realizar o carregamento dos endereços de fontes, imagens e sons do jogo.
"""


import os
from os.path import join as join_path


dados_py  = os.path.abspath(os.path.dirname(__file__))
dados_dir = os.path.normpath(join_path(data_py, '..', 'media'))


endereco_arquivos = dict(
    fontes  = join_path(data_dir, 'fontes'),
    imagens = join_path(data_dir, 'imagens'),
    sons = join_path(data_dir, 'sons'),
)


def endereco_arquivo(tipo, nome_arquivo):
    return join_path(endereco_arquivos[tipo], nome_arquivo)


def carrega(tipo, nome_arquivo, modo='rb'):
    return open(endereco_arquivo(tipo, filename), modo)


def carrega_fonte(nome_arquivo):
    return carrega('fontes', nome_arquivo)


def carrega_imagem(nome_arquivo):
    return carrega('imagens', nome_arquivo)


def carrega_son(nome_arquivo):
    return carrega('sons', nome_arquivo)