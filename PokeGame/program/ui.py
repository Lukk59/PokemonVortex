from settings import *  # 1 - Importa configurações globais do jogo (como cores, dimensões, etc.)
from support import folder_importer  # 2 - Importa função utilitária para carregar pastas de imagens

class UI:  # 3 - Define a classe responsável pela interface do jogador
    def __init__(self, monster, player_monsters, simple_surfs, get_input):  # 4 - Inicializa a interface gráfica
        self.display_surface = pygame.display.get_surface()  # 5 - Superfície principal onde tudo será desenhado
        self.font = pygame.font.Font(None, 30)  # 6 - Define a fonte usada na interface
        self.left = WINDOW_WIDTH / 2 - 100  # 7 - Define a posição horizontal da UI
        self.top = WINDOW_HEIGHT / 2 + 50  # 8 - Define a posição vertical da UI
        self.monster = monster  # 9 - Monstro atual do jogador
        self.simple_surfs = simple_surfs  # 10 - Dicionário com sprites simples dos monstros
        self.get_input = get_input  # 11 - Função callback para registrar escolhas do jogador

        self.general_options = ['attack', 'heal', 'switch', 'escape']  # 12 - Ações principais disponíveis
        self.general_index = {'col' : 0, 'row': 0}  # 13 - Índice do menu geral (posição na grade)
        self.attack_index = {'col': 0, 'row': 0}  # 14 - Índice do menu de ataques
        self.state = 'general'  # 15 - Estado atual da UI (tipo de menu ativo)
        self.rows, self.cols  = 2,2  # 16 - Define a grade de opções (2x2)
        self.visible_monsters = 4  # 17 - Quantos monstros aparecem no menu de troca
        self.player_monsters = player_monsters  # 18 - Lista de monstros do jogador
        self.available_monsters = [monster for monster in self.player_monsters if monster != self.monster and monster.health > 0]  # 19 - Filtra apenas os monstros disponíveis para troca
        self.switch_index = 0  # 20 - Índice do monstro selecionado para troca

        self.elementos_icones = folder_importer('images', 'icones')  # 21 - Carrega ícones dos elementos das habilidades

    # Abaixo estão os métodos que tratam a entrada do jogador, desenham os menus e atualizam a interface;
    def input(self):  # 22 - Trata a entrada de teclado do jogador
        keys = pygame.key.get_just_pressed()  # 23 - Captura teclas recém pressionadas

        # Verifica se o jogador está no menu geral ou em outro estado
        # Se estiver no menu geral, permite navegação entre opções
        # Se estiver no menu de ataques, permite selecionar habilidades
        if self.state == 'general':  # 24 - Se estiver no menu geral
            self.general_index['row'] = (self.general_index['row'] + int(keys[pygame.K_DOWN]) + int(keys[pygame.K_s]) - int(keys[pygame.K_UP]) - int(keys[pygame.K_w])) % self.rows  # 25 - Atualiza linha com base nas teclas
            self.general_index['col'] = (self.general_index['col'] + int(keys[pygame.K_RIGHT]) + int(keys[pygame.K_d]) - int(keys[pygame.K_LEFT]) - int(keys[pygame.K_a])) % self.cols  # 26 - Atualiza coluna com base nas teclas
            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:  # 27 - Confirma opção
                self.state = self.general_options[self.general_index['col'] + self.general_index['row'] * 2]  # 28 - Atualiza estado da UI com base na opção escolhida

        # Se estiver no menu de ataques, permite selecionar habilidades;
        elif self.state == 'attack':  # 29 - Se estiver no menu de ataques
            self.attack_index['row'] = (self.attack_index['row'] + int(keys[pygame.K_DOWN]) + int(keys[pygame.K_s]) - int(keys[pygame.K_UP]) - int(keys[pygame.K_w])) % self.rows  # 30 - Atualiza linha
            self.attack_index['col'] = (self.attack_index['col'] + int(keys[pygame.K_RIGHT]) + int(keys[pygame.K_d]) - int(keys[pygame.K_LEFT]) - int(keys[pygame.K_a])) % self.cols  # 31 - Atualiza coluna
            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:  # 32 - Se confirmar com espaço ou enter;
                attack = (self.monster.abilities[self.attack_index['col'] + self.attack_index['row'] * 2])  # 33 - Seleciona habilidade
                self.get_input(self.state, attack)  # 34 - Envia ação para o jogo
                self.state = 'general'  # 35 - Retorna ao menu principal

        # Se estiver no menu de troca, permite selecionar outro monstro;
        elif self.state == 'switch':  # 36 - Se estiver no menu de troca
            if self.available_monsters:  # 37 - Verifica se há monstros disponíveis
                self.switch_index = (self.switch_index + int(keys[pygame.K_DOWN] + int(keys[pygame.K_s]) - int(keys[pygame.K_UP] + int(keys[pygame.K_w])))) % len(self.available_monsters)  # 38 - Atualiza seleção com base nas teclas

                # Se pressionar espaço ou enter, confirma a troca;
                # Envia a escolha do monstro para o jogo e volta ao menu principal;
                if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:  # 39 - Confirma troca
                    self.get_input(self.state, self.available_monsters[self.switch_index])  # 40 - Envia escolha
                    self.state = 'general'  # 41 - Retorna ao menu principal

        # Se estiver no menu de cura ou fuga, executa a ação correspondente;
        elif self.state == 'heal':  # 42 - Se escolheu curar
            self.get_input('heal')  # 43 - Envia comando de cura
            self.state = 'general'  # 44 - Volta ao menu principal

        #  Se escolheu fugir, executa a ação de fuga;
        elif self.state == 'escape':  # 45 - Se escolheu fugir
            self.get_input('escape')  # 46 - Envia comando de fuga

        # Se pressionar a tecla de voltar, retorna ao menu geral; Tem isso?
        # Isso permite ao jogador sair de menus secundários e voltar ao menu principal.
        if keys[pygame.K_BACKSPACE]:  # 47 - Tecla para voltar ao menu geral
            self.state = 'general'  # 48 - Reseta o estado
            self.general_index = {'col': 0, 'row': 0}  # 49 - Reseta índice do menu geral
            self.attack_index = {'col': 0, 'row': 0}  # 50 - Reseta índice do menu de ataque
            self.switch_index = 0  # 51 - Reseta índice do menu de troca

    def quad_select(self, index, options):  # 52 - Desenha um menu em formato de grade (2x2)
        rect = pygame.Rect(self.left + 40, self.top + 60, 400, 200)  # 53 - Define a área do menu
        pygame.draw.rect(self.display_surface, COLORS['white'], rect, 0, 4)  # 54 - Preenche fundo
        pygame.draw.rect(self.display_surface, COLORS['gray'], rect, 4, 4)  # 55 - Borda do menu

        for col in range(self.cols):  # 56 - Loop pelas colunas
            for row in range(self.rows):  # 57 - Loop pelas linhas
                x = rect.left + rect.width / (self.cols * 2) + (rect.width / self.cols) * col  # 58 - Calcula posição X do item
                y = rect.top + rect.height / (self.rows * 2) + (rect.height/ self.rows) * row  # 59 - Calcula posição Y do item
                i = col + 2 * row  # 60 - Calcula índice linear
                color = COLORS['gray'] if col == index['col'] and row == index['row'] else COLORS['black']  # 61 - Destaca opção selecionada

                text_surf = self.font.render(options[i], True, color)  # 62 - Renderiza texto da opção
                text_rect = text_surf.get_rect(center = (x, y))  # 63 - Centraliza texto

                if self.state == "attack":  # 64 - Se estiver mostrando habilidades
                    ability_name = options[i]  # 65 - Nome da habilidade
                    elemento = ABILITIES_DATA[ability_name]['element']  # 66 - Tipo elemental
                    icon = self.elementos_icones[elemento]  # 67 - Ícone correspondente
                    icon_rect = icon.get_rect(midright=(text_rect.left + 110, y - 35))  # 68 - Posição do ícone
                    self.display_surface.blit(icon, icon_rect)  # 69 - Desenha ícone

                self.display_surface.blit(text_surf, text_rect)  # 70 - Desenha texto

    def switch(self):  # 71 - Desenha o menu de troca de monstros
        rect = pygame.Rect(self.left + 40, self.top - 140, 400, 400)  # 72 - Área do menu
        pygame.draw.rect(self.display_surface, COLORS['white'], rect, 0, 4)  # 73 - Fundo branco
        pygame.draw.rect(self.display_surface, COLORS['gray'], rect, 4, 4)  # 74 - Borda cinza

        v_offset = 0 if self.switch_index < self.visible_monsters else -(self.switch_index - self.visible_monsters + 1) * rect.height / self.visible_monsters  # 75 - Deslocamento vertical para rolagem

        for i in range(len(self.available_monsters)):  # 76 - Itera sobre os monstros disponíveis
            x = rect.centerx  # 77 - Centro horizontal
            y = rect.top + rect.height / (self.visible_monsters * 2) + rect.height / self.visible_monsters * i + v_offset  # 78 - Posição vertical
            color = COLORS['gray'] if i == self.switch_index else COLORS['black']  # 79 - Cor do nome

            name = self.available_monsters[i].name  # 80 - Nome do monstro
            simple_surf = self.simple_surfs[name]  # 81 - Sprite do monstro
            simple_rect = simple_surf.get_frect(center = (x - 100, y))  # 82 - Posição do sprite

            text_surf = self.font.render(name, True, color)  # 83 - Renderiza texto
            text_rect = text_surf.get_frect(midleft = (x,y))  # 84 - Posiciona texto

            if rect.collidepoint(text_rect.center):  # 85 - Verifica se está visível
                self.display_surface.blit(text_surf, text_rect)  # 86 - Desenha texto
                self.display_surface.blit(simple_surf, simple_rect)  # 87 - Desenha sprite

    def stats(self):  # 88 - Exibe estatísticas do monstro (nome e vida)
        rect = pygame.FRect(self.left, self.top, 250, 80)  # 89 - Área da barra de status
        pygame.draw.rect(self.display_surface, COLORS['white'], rect, 0, 4)  # 90 - Fundo branco
        pygame.draw.rect(self.display_surface, COLORS['gray'], rect, 4, 4)  # 91 - Borda cinza

        name_surf = self.font.render(self.monster.name, True, COLORS['black'])  # 92 - Nome do monstro
        name_rect = name_surf.get_frect(topleft = rect.topleft + pygame.Vector2(rect.width * 0.05, 12))  # 93 - Posição do nome
        self.display_surface.blit(name_surf, name_rect)  # 94 - Exibe nome

        health_rect = pygame.FRect(name_rect.left, name_rect.bottom + 10, rect.width * 0.9, 20)  # 95 - Área da barra de vida
        pygame.draw.rect(self.display_surface, COLORS['gray'], health_rect)  # 96 - Fundo da barra de vida
        self.draw_bar(health_rect, self.monster.health, self.monster.max_health)  # 97 - Desenha barra com valor atual

    def draw_bar(self, rect, value, max_value):  # 98 - Desenha uma barra proporcional (vida)
        ratio = rect.width / max_value  # 99 - Proporção atual
        progress_rect = pygame.FRect(rect.topleft, (value * ratio, rect.height))  # 100 - Retângulo proporcional
        pygame.draw.rect(self.display_surface, COLORS['red'], progress_rect)  # 101 - Cor vermelha da barra

    def update(self):  # 102 - Atualiza interface
        self.input()  # 103 - Lê entrada do jogador
        self.available_monsters = [monster for monster in self.player_monsters if monster != self.monster and monster.health > 0]  # 104 - Atualiza lista de monstros vivos

    def draw(self):  # 105 - Desenha elementos da interface
        match self.state:  # 106 - Escolhe interface com base no estado
            case 'general': self.quad_select(self.general_index, self.general_options)  # 107 - Menu principal
            case 'attack': self.quad_select(self.attack_index, self.monster.abilities)  # 108 - Menu de ataques
            case 'switch': self.switch()  # 109 - Menu de troca

        if self.state != 'switch':  # 110 - Se não estiver no menu de troca
            self.stats()  # 111 - Mostra status do monstro

class OpponentUI:  # 112 - Interface gráfica do oponente
    def __init__(self, monster):  # 113 - Inicializa interface com o monstro adversário
        self.display_surface = pygame.display.get_surface()  # 114 - Superfície principal
        self.monster = monster  # 115 - Monstro adversário
        self.font = pygame.font.Font(None, 30)  # 116 - Fonte do texto

    def draw(self):  # 117 - Desenha UI do oponente
        rect = pygame.FRect((0, 0), (250, 80)).move_to(midleft = (500, self.monster.rect.centery))  # 118 - Área de status
        pygame.draw.rect(self.display_surface, COLORS['white'], rect, 0, 4)  # 119 - Fundo branco
        pygame.draw.rect(self.display_surface, COLORS['gray'], rect, 4, 4)  # 120 - Borda cinza

        name_surf = self.font.render(self.monster.name, True, COLORS['black'])  # 121 - Nome do oponente
        name_rect = name_surf.get_frect(topleft = rect.topleft + pygame.Vector2(rect.width * 0.05, 12))  # 122 - Posição do nome
        self.display_surface.blit(name_surf, name_rect)  # 123 - Exibe nome

        health_rect = pygame.FRect(name_rect.left, name_rect.bottom + 10, rect.width * 0.9, 20)  # 124 - Área da barra de vida
        ratio = health_rect.width / self.monster.max_health  # 125 - Proporção da vida
        progress_rect = pygame.FRect(health_rect.topleft, (self.monster.health * ratio, health_rect.height))  # 126 - Barra proporcional
        pygame.draw.rect(self.display_surface, COLORS['gray'], health_rect)  # 127 - Fundo da barra
        pygame.draw.rect(self.display_surface, COLORS['red'], progress_rect)  # 128 - Vida em vermelho
        
    def update(self):  # 129 - Placeholder para atualizações futuras
        pass  # 130 - Nada implementado ainda
