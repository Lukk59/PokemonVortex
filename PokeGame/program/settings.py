import pygame  # 1 - Importa a biblioteca Pygame para gráficos, eventos e controle de tela
import threading  # 2 ****** - Importa suporte para múltiplas threads; Import threading for potential future use. point of the game; ***********************
import sys  # 3 - Importa funções do sistema (ex: sys.exit())
from timer import Timer  # 4 - Importa classe Timer personalizada
from os.path import join  # 5 - Importa função para criar caminhos de arquivo seguros
from os import walk  # 6 - Importa função para percorrer diretórios
from PIL import Image  # 7 - Importa suporte para imagens (Pillow)

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720  # 8 - Define a resolução da janela do jogo

class Display():  # 9 - Classe para encapsular a criação da tela do jogo
    def __init__(self):  # 10 - Construtor da tela
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # 11 - Cria a tela com tamanho fixo
        pygame.display.set_caption('Run & Gun')  # 12 - Define o título da janela
        self.running = True  # 13 - Flag que indica se o jogo está em execução

COLORS = {  # 14 - Dicionário de cores nomeadas utilizadas na interface
    'black' : '#000000',  # 15 - Preto
    'red': '#ee1a0f',  # 16 - Vermelho
    'gray': '#808080',  # 17 - Cinza
    'white': '#ffffff',  # 18 - Branco
}

MONSTER_DATA = {  # 19 - Dicionário com dados dos monstros jogáveis
    'Plumette':    {'element': 'plant', 'health': 90},     # 20 - Planta com 90 de vida
    'Ivieron':     {'element': 'plant', 'health': 140},    # 21 - Planta com 140 de vida
    'Pluma':       {'element': 'plant', 'health': 160},    # 22 - Planta com 160 de vida
    'Sparchu':     {'element': 'fire', 'health': 70},      # 23 - Fogo com 70 de vida
    'Cindrill':    {'element': 'fire', 'health': 100},     # 24 - Fogo com 100 de vida
    'Charmadillo': {'element': 'fire', 'health': 120},     # 25 - Fogo com 120 de vida
    'Finsta':      {'element': 'water', 'health': 50},     # 26 - Água com 50 de vida
    'Gulfin':      {'element': 'water', 'health': 80},     # 27 - Água com 80 de vida
    'Finiette':    {'element': 'water', 'health': 100},    # 28 - Água com 100 de vida
    'Atrox':       {'element': 'fire', 'health': 50},      # 29 - Fogo frágil
    'Pouch':       {'element': 'plant', 'health': 80},     # 30 - Planta com 80 de vida
    'Draem':       {'element': 'plant', 'health': 110},    # 31 - Planta com 110 de vida
    'Larvea':      {'element': 'plant', 'health': 40},     # 32 - Planta com 40 de vida
    'Cleaf':       {'element': 'plant', 'health': 90},     # 33 - Planta com 90 de vida
    'Jacana':      {'element': 'fire', 'health': 60},      # 34 - Fogo com 60 de vida
    'Friolera':    {'element': 'water', 'health': 70},     # 35 - Água com 70 de vida
}

ABILITIES_DATA = {  # 36 - Dicionário com dados de habilidades disponíveis
    'scratch' : {'damage': 20, 'element': 'normal', 'animation': 'scratch'},  # 37 - Ataque básico
    'spark' :   {'damage': 35, 'element': 'fire', 'animation': 'fire'},       # 38 - Ataque de fogo
    'nuke' :    {'damage': 50, 'element': 'fire', 'animation': 'explosion'},  # 39 - Ataque forte de fogo
    'splash' :  {'damage': 30, 'element': 'water', 'animation': 'splash'},    # 40 - Ataque de água
    'shards' :  {'damage': 50, 'element': 'water', 'animation': 'ice'},       # 41 - Ataque de gelo/água
    'spiral' :  {'damage': 40, 'element': 'plant', 'animation': 'green'}      # 42 - Ataque de planta
}

ELEMENT_DATA  = {  # 43 - Tabela de multiplicadores de dano com base em elementos
    'fire': {'water': 0.5, 'plant': 2, 'fire': 1, 'normal': 1},  # 44 - Fogo toma menos de água, mais de planta
    'water': {'water': 1, 'plant': 0.5, 'fire': 2, 'normal': 1},  # 45 - Água toma menos de planta, mais de fogo
    'plant': {'water': 2, 'plant': 1, 'fire': 0.5, 'normal': 1},  # 46 - Planta toma menos de fogo, mais de água
    'normal': {'water': 1, 'plant': 1, 'fire': 1, 'normal': 1},  # 47 - Normal não tem vantagem/desvantagem
}