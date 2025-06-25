import pygame   # Import pygame for game development;
import threading   # Import threading for potential future use. point of the game; ***************************************************
import time        # Import time for potential future use;
import sys       # Import sys for system-specific parameters and functions;
from os.path import join  # Import join to construct file paths;
from os import walk # Import walk to traverse directories;
from PIL import Image   # Import Image from PIL for image processing;

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720 # Define the dimensions of the game window;

class Display():
    def __init__(self):
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Run & Gun')
        self.running = True

COLORS = {
    'black' : '#000000',
    'red': '#ee1a0f',
    'gray': '#808080',
    'white': '#ffffff',
}

MONSTER_DATA = {
    'Plumette':    {'element': 'plant', 'health': 90},
    'Ivieron':     {'element': 'plant', 'health': 140},
    'Pluma':       {'element': 'plant', 'health': 160},
    'Sparchu':     {'element': 'fire', 'health': 70},
    'Cindrill':    {'element': 'fire', 'health': 100},
    'Charmadillo': {'element': 'fire', 'health': 120},
    'Finsta':      {'element': 'water', 'health': 50},
    'Gulfin':      {'element': 'water', 'health': 80},
    'Finiette':    {'element': 'water', 'health': 100},
    'Atrox':       {'element': 'fire', 'health': 50},
    'Pouch':       {'element': 'plant', 'health': 80},
    'Draem':       {'element': 'plant', 'health': 110},
    'Larvea':      {'element': 'plant', 'health': 40},
    'Cleaf':       {'element': 'plant', 'health': 90},
    'Jacana':      {'element': 'fire', 'health': 60},
    'Friolera':    {'element': 'water', 'health': 70},
}

ABILITIES_DATA = {
    'scratch' : {'damage': 20, 'element': 'normal', 'animation': 'scratch'},
    'spark' :   {'damage': 35, 'element': 'fire', 'animation': 'fire'},
    'nuke' :    {'damage': 50, 'element': 'fire', 'animation': 'explosion'},
    'splash' :  {'damage': 30, 'element': 'water', 'animation': 'splash'},
    'shards' :  {'damage': 50, 'element': 'water', 'animation': 'ice'},
    'spiral' :  {'damage': 40, 'element': 'plant', 'animation': 'green'}
}

ELEMENT_DATA  = {
    'fire': {'water': 0.5, 'plant': 2, 'fire': 1, 'normal': 1},
    'water': {'water': 1, 'plant': 0.5, 'fire': 2, 'normal': 1},
    'plant': {'water': 2, 'plant': 1, 'fire': 0.5, 'normal': 1},
    'normal': {'water': 1, 'plant': 1, 'fire': 1, 'normal': 1},
}
