from settings import *  # 1 - Importa configurações globais do jogo, como dimensões, MONSTER_DATA, etc.
from random import sample  # 2 - Importa a função sample para selecionar habilidades aleatórias

# Importa os dados de monstros e habilidades;
class Creature:  # 3 - Classe base para representar uma criatura (usada tanto por monstros quanto oponentes)
    def get_data(self, name):  # 4 - Carrega os dados do monstro a partir de seu nome
        self.element = MONSTER_DATA[name]['element']  # 5 - Define o elemento do monstro (ex: água, fogo)
        self._health = self.max_health = MONSTER_DATA[name]['health']  # 6 - Define vida atual e máxima
        self.abilities = sample(list(ABILITIES_DATA.keys()), 4)  # 7 - Seleciona 4 habilidades aleatórias do dicionário
        self.name = name  # 8 - Armazena o nome do monstro

    # Getter e Setter para a propriedade health, que controla a vida do monstro;
    @property # 9 - Define uma propriedade para acessar a vida do monstro;
    def health(self):  # 9 - Getter da propriedade health
        return self._health  # 10 - Retorna a vida atual privada;

    # Setter para a propriedade health, que garante que a vida não ultrapasse os limites;
    @health.setter
    def health(self, value):  # 11 - Setter da propriedade health
        self._health = min(self.max_health, max(0, value))  # 12 - Garante que a vida fique entre 0 e a vida máxima

# Importa o Pygame e as configurações do jogo;
class Monster(pygame.sprite.Sprite, Creature):  # 13 - Classe que representa o monstro do jogador, herda Sprite e Creature
    def __init__(self, name, surf):  # 14 - Construtor que recebe o nome do monstro e sua imagem
        super().__init__()  # 15 - Inicializa a Sprite
        self.image = surf  # 16 - Define a imagem do monstro
        self.rect = self.image.get_rect(bottomleft = (100, WINDOW_HEIGHT))  # 17 - Posiciona o monstro no canto inferior esquerdo da tela
        self.name = name  # 18 - Salva o nome do monstro
        self.get_data(name)  # 19 - Chama o método para carregar habilidades, elemento e vida

    # Método para atacar outro monstro, reduzindo sua vida;
    def __repr__(self):  # 20 - Representação textual do objeto, útil para debug
        return f'{self.name}: {self.health}/{self.max_health}'  # 21 - Retorna string com nome e vida do monstro

# Importa o Pygame e as configurações do jogo;
class Opponent(pygame.sprite.Sprite, Creature):  # 22 - Classe que representa o oponente controlado pela IA
    def __init__(self, name, surf, groups):  # 23 - Construtor que recebe nome, imagem e grupos de sprites
        super().__init__(groups)  # 24 - Inicializa a Sprite e adiciona aos grupos
        self.image = surf  # 25 - Define a imagem do oponente
        self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH - 350, 300))  # 26 - Posiciona oponente na lateral direita da tela
        self.get_data(name)  # 27 - Carrega habilidades, vida e elemento do oponente
