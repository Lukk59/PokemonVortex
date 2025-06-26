from settings import *  # 1 - Importa as configurações globais do jogo (como cores e dimensões)
from support import folder_importer  # 2 - Importa função utilitária para carregar imagens de uma pasta

class UI:  # 3 - Classe responsável pela interface do jogador (menus de ação, troca, cura etc.)
    def __init__(self, monster, player_monsters, simple_surfs, get_input):  # 4 - Inicializa a interface do jogador
        self.display_surface = pygame.display.get_surface()  # 5 - Superfície onde os elementos da UI serão desenhados
        self.font = pygame.font.Font(None, 30)  # 6 - Fonte usada nos textos da UI
        self.left = WINDOW_WIDTH / 2 - 100  # 7 - Posição horizontal da UI
        self.top = WINDOW_HEIGHT / 2 + 50  # 8 - Posição vertical da UI
        self.monster = monster  # 9 - Monstro atual do jogador
        self.simple_surfs = simple_surfs  # 10 - Dicionário de imagens simples dos monstros
        self.get_input = get_input  # 11 - Função callback para processar a ação do jogador

        # control
        self.general_options = ['attack', 'heal', 'switch', 'escape']  # 12 - Opções principais disponíveis
        self.general_index = {'col' : 0, 'row': 0}  # 13 - Índice da seleção no menu principal
        self.attack_index = {'col': 0, 'row': 0}  # 14 - Índice da seleção no menu de ataque
        self.state = 'general'  # 15 - Estado atual da interface
        self.rows, self.cols  = 2,2  # 16 - Número de linhas e colunas dos menus
        self.visible_monsters = 4  # 17 - Quantos monstros aparecem ao mesmo tempo no menu de troca
        self.player_monsters = player_monsters  # 18 - Lista de todos os monstros do jogador
        self.available_monsters = [monster for monster in self.player_monsters if monster != self.monster and monster.health > 0]  # 19 - Filtra os monstros disponíveis para troca
        self.switch_index = 0  # 20 - Índice atual do menu de troca

        # ícones
        self.elementos_icones = folder_importer('images', 'icones')  # 21 - Carrega os ícones dos elementos

    def input(self):  # 22 - Função que processa entradas do jogador
        keys = pygame.key.get_just_pressed()  # 23 - Captura teclas recém pressionadas
        if self.state == 'general':  # 24 - Menu principal
            self.general_index['row'] = (self.general_index['row'] + int(keys[pygame.K_DOWN]) + int(keys[pygame.K_s]) - int(keys[pygame.K_UP]) - int(keys[pygame.K_w])) % self.rows  # 25 - Navega entre as linhas
            self.general_index['col'] = (self.general_index['col'] + int(keys[pygame.K_RIGHT]) + int(keys[pygame.K_d]) - int(keys[pygame.K_LEFT]) - int(keys[pygame.K_a])) % self.cols  # 26 - Navega entre as colunas
            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:  # 27 - Seleciona uma opção se pressionar espaço ou enter;
                self.state = self.general_options[self.general_index['col'] + self.general_index['row'] * 2]  # 28 - Muda o estado da UI conforme a seleção
        
        elif self.state == 'attack':  # 29 - Menu de ataque
            self.attack_index['row'] = (self.attack_index['row'] + int(keys[pygame.K_DOWN]) + int(keys[pygame.K_s]) - int(keys[pygame.K_UP]) - int(keys[pygame.K_w])) % self.rows  # 30 - Move linha
            self.attack_index['col'] = (self.attack_index['col'] + int(keys[pygame.K_RIGHT]) + int(keys[pygame.K_d]) - int(keys[pygame.K_LEFT]) - int(keys[pygame.K_a])) % self.cols  # 31 - Move coluna
            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:  # 32 - Confirma ataque;
                attack = (self.monster.abilities[self.attack_index['col'] + self.attack_index['row'] * 2])  # 33 - Recupera o ataque selecionado
                self.get_input(self.state, attack)  # 34 - Envia o ataque
                self.state = 'general'  # 35 - Volta para o menu principal

        elif self.state == 'switch':  # 36 - Menu de troca
            if self.available_monsters:  # 37 - Se há monstros disponíveis
                self.switch_index = (self.switch_index + int(keys[pygame.K_DOWN] + int(keys[pygame.K_s]) - int(keys[pygame.K_UP] + int(keys[pygame.K_w])))) % len(self.available_monsters)  # 38 - Muda o índice da troca
            
                if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:  # 39 - Seleciona troca;
                    self.get_input(self.state, self.available_monsters[self.switch_index])  # 40 - Envia monstro escolhido
                    self.state = 'general'  # 41 - Volta ao menu principal

        elif self.state == 'heal':  # 42 - Ação de cura
            self.get_input('heal')  # 43 - Envia comando de cura
            self.state = 'general'  # 44 - Volta ao menu principal

        elif self.state == 'escape':  # 45 - Ação de fuga
            self.get_input('escape')  # 46 - Envia comando de fuga

        if keys[pygame.K_BACKSPACE]:  # 47 - Tecla para voltar
            self.state = 'general'  # 48 - Retorna ao menu principal;
            self.general_index = {'col': 0, 'row': 0}  # 49 - Reseta o índice do menu principal;
            self.attack_index = {'col': 0, 'row': 0}  # 50 - Reseta o índice do menu de ataque;
            self.switch_index = 0  # 51 - Reseta o índice do menu de troca;

    def quad_select(self, index, options):  # 52 - Desenha menu 2x2 para ações ou ataques
        rect = pygame.Rect(self.left + 40, self.top + 60, 400, 200)  # 53 - Retângulo do menu
        pygame.draw.rect(self.display_surface, COLORS['white'], rect, 0, 4)  # 54 - Fundo branco
        pygame.draw.rect(self.display_surface, COLORS['gray'], rect, 4, 4)  # 55 - Borda cinza

        for col in range(self.cols):  # 56 - Para cada coluna
            for row in range(self.rows):  # 57 - Para cada linha
                x = rect.left + rect.width / (self.cols * 2) + (rect.width / self.cols) * col  # 58 - Coordenada X do item
                y = rect.top + rect.height / (self.rows * 2) + (rect.height/ self.rows) * row  # 59 - Coordenada Y do item
                i = col + 2 * row  # 60 - Índice linear
                color = COLORS['gray'] if col == index['col'] and row == index['row'] else COLORS['black']  # 61 - Cor do texto (destaque)

                text_surf = self.font.render(options[i], True, color)  # 62 - Renderiza o texto
                text_rect = text_surf.get_rect(center = (x, y))  # 63 - Centraliza o texto

                if self.state == "attack":  # 64 - Se for ataque, desenha ícone;
                    ability_name = options[i]  # 65 - Nome da habilidade;
                    elemento = ABILITIES_DATA[ability_name]['element']  # 66 - Pega o tipo do ataque
                    icon = self.elementos_icones[elemento]  # 67 - Ícone do tipo
                    icon_small = pygame.transform.scale(icon, (23, 23))  # 68 - Redimensiona ícone
                    icon_rect = icon_small.get_rect(midright=(text_rect.left + 110, y - 10))  # 69 - Define posição do ícone
                    self.display_surface.blit(icon_small, icon_rect)  # 70 - Desenha o ícone

                self.display_surface.blit(text_surf, text_rect)  # 71 - Desenha o texto da ação

    def switch(self):  # 72 - Desenha o menu de troca de monstros
        rect = pygame.Rect(self.left + 40, self.top - 140, 400, 400)  # 73 - Retângulo do menu
        pygame.draw.rect(self.display_surface, COLORS['white'], rect, 0, 4)  # 74 - Fundo branco;
        pygame.draw.rect(self.display_surface, COLORS['gray'], rect, 4, 4)  # 75 - Borda cinza;

        v_offset = 0 if self.switch_index < self.visible_monsters else -(self.switch_index - self.visible_monsters + 1) * rect.height / self.visible_monsters  # 76 - Compensa o scroll

        for i in range(len(self.available_monsters)):  # 77 - Itera sobre os monstros disponíveis
            x = rect.centerx  # 78 - Posição X central do retângulo;
            y = rect.top + rect.height / (self.visible_monsters * 2) + rect.height / self.visible_monsters * i + v_offset  # 79 - Calcula a posição Y;
            color = COLORS['gray'] if i == self.switch_index else COLORS['black']  # 80 - Cor de seleção;
            name = self.available_monsters[i].name  # 81 - Nome do monstro;

            simple_surf = self.simple_surfs[name]  # 82 - Imagem do monstro;
            simple_rect = simple_surf.get_frect(center = (x - 100, y))  # 83 - Posição da imagem

            text_surf = self.font.render(name, True, color)  # 84 - Renderiza o texto do nome do monstro;
            text_rect = text_surf.get_frect(midleft = (x,y))  # 85 - Posição do texto;
            if rect.collidepoint(text_rect.center):  # 86 - Só desenha se estiver visível;
                self.display_surface.blit(text_surf, text_rect)  # 87 - Desenha o texto do nome do monstro;
                self.display_surface.blit(simple_surf, simple_rect)  # 88 - Desenha a imagem do monstro;

    def stats(self):  # 89 - Desenha a barra de vida do monstro atual
        rect = pygame.FRect(self.left, self.top, 250, 80)  # 90 - Retângulo onde a barra de vida será desenhada;
        pygame.draw.rect(self.display_surface, COLORS['white'], rect, 0, 4)  # 91 - Fundo branco;
        pygame.draw.rect(self.display_surface, COLORS['gray'], rect, 4, 4)  # 92 - Borda cinza;

        name_surf = self.font.render(self.monster.name, True, COLORS['black'])  # 93 - Renderiza o nome do monstro;
        name_rect = name_surf.get_frect(topleft = rect.topleft + pygame.Vector2(rect.width * 0.05, 12))  # 94 - Posição do nome;
        self.display_surface.blit(name_surf, name_rect)  # 95 - Desenha o nome do monstro;

        health_rect = pygame.FRect(name_rect.left, name_rect.bottom + 10, rect.width * 0.9, 20)  # 96 - Retângulo da barra de vida;
        pygame.draw.rect(self.display_surface, COLORS['gray'], health_rect)  # 97 - Desenha fundo da barra de vida;
        self.draw_bar(health_rect, self.monster.health, self.monster.max_health)  # 98 - Desenha a barra de vida com a função draw_bar;

    def draw_bar(self, rect, value, max_value):  # 99 - Função para desenhar barra de progresso (vida);
        ratio = rect.width / max_value  # 100 - Calcula a proporção do valor máximo;
        progress_rect = pygame.FRect(rect.topleft, (value * ratio, rect.height))  # 101 - Retângulo da barra de progresso;
        pygame.draw.rect(self.display_surface, COLORS['red'], progress_rect)  # 102 - Desenha a barra de progresso com a cor vermelha;

    def update(self):  # 103 - Atualiza a UI;
        self.input()  # 104 - Processa entradas do jogador;
        self.available_monsters = [monster for monster in self.player_monsters if monster != self.monster and monster.health > 0]  # 105 - Atualiza lista de monstros disponíveis para troca;

    def draw(self):  # 106 - Desenha os menus apropriados
        match self.state:  # 107 - Verifica o estado atual da UI;
            case 'general': self.quad_select(self.general_index, self.general_options)  # 108 - Desenha o menu geral;
            case 'attack': self.quad_select(self.attack_index, self.monster.abilities)  # 109 - Desenha o menu de ataques;
            case 'switch': self.switch()  # 110 - Desenha o menu de troca de monstros;

        if self.state != 'switch':  # 111 - Se não estiver no menu de troca, desenha a barra de vida do monstro atual;
            self.stats()  # 112 - Desenha a barra de vida do monstro atual;

# ===========================
# Classe da UI do oponente;
class OpponentUI:  # 113 - Classe da UI do oponente
    def __init__(self, monster):  # 114 - Inicializa a UI do oponente;
        self.display_surface = pygame.display.get_surface()  # 115 - Superfície onde a UI do oponente será desenhada;
        self.monster = monster  # 116 - Monstro do oponente;
        self.font = pygame.font.Font(None, 30)  # 117 - Fonte usada nos textos da UI do oponente;

    def draw(self):  # 118 - Desenha a barra de vida do oponente;
        rect = pygame.FRect((0, 0), (250, 80)).move_to(midleft = (500, self.monster.rect.centery))  # 119 - Retângulo onde a barra de vida do oponente será desenhada;
        pygame.draw.rect(self.display_surface, COLORS['white'], rect, 0, 4)  # 120 - Fundo branco;
        pygame.draw.rect(self.display_surface, COLORS['gray'], rect, 4, 4)  # 121 - Borda cinza;

        name_surf = self.font.render(self.monster.name, True, COLORS['black'])  # 122 - Renderiza o nome do monstro do oponente;
        name_rect = name_surf.get_frect(topleft = rect.topleft + pygame.Vector2(rect.width * 0.05, 12))  # 123 - Posição do nome do monstro;
        self.display_surface.blit(name_surf, name_rect)  # 124 - Desenha o nome do monstro do oponente;

        health_rect = pygame.FRect(name_rect.left, name_rect.bottom + 10, rect.width * 0.9, 20)  # 125 - Retângulo da barra de vida do oponente;
        ratio = health_rect.width / self.monster.max_health  # 126 - Calcula a proporção do valor máximo de vida do oponente;
        progress_rect = pygame.FRect(health_rect.topleft, (self.monster.health * ratio, health_rect.height))  # 127 - Retângulo da barra de progresso da vida do oponente;
        pygame.draw.rect(self.display_surface, COLORS['gray'], health_rect)  # 128 - Desenha fundo da barra de vida do oponente;
        pygame.draw.rect(self.display_surface, COLORS['red'], progress_rect)  # 129 - Desenha a barra de progresso da vida do oponente;

    def update(self):  # 130 - Atualiza a UI do oponente;
        pass  # 131 - Método reservado para atualizações futuras
