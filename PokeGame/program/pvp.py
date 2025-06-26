from settings import *  # 1 - Importa configurações globais do jogo, como dimensões da janela e cores
from pvpc import *  # 2 - Importa classe PokeSelect usada para seleção de monstros

class PokePvP():  # 3 - Classe responsável por gerenciar a seleção de monstros no modo PvP
    def __init__(self, simples_surfs):  # 4 - Inicializa a seleção para dois jogadores
        pygame.init()  # 5 - Inicia o Pygame
        self.display = Display()  # 6 - Inicializa o objeto de display (janela)
        self.display_surface = self.display.display_surface  # 7 - Superfície onde tudo será desenhado
        self.clock = pygame.time.Clock()  # 8 - Controlador de FPS
        self.running = True  # 9 - Flag principal de execução do loop

        self.p1 = PokeSelect(simples_surfs)  # 10 - Seleção de monstros para o jogador 1
        self.p2 = PokeSelect(simples_surfs)  # 11 - Seleção de monstros para o jogador 2
        self.p1.left = WINDOW_WIDTH / 2 - 550  # 12 - Posição da interface do jogador 1
        self.p2.left = (WINDOW_WIDTH * 3) // 4 - 200  # 13 - Posição da interface do jogador 2

        self.p1.selected = []  # 14 - Lista de monstros escolhidos pelo jogador 1
        self.p2.selected = []  # 15 - Lista de monstros escolhidos pelo jogador 2
        self.p1.index = 0  # 16 - Índice atual da lista para navegação do jogador 1
        self.p2.index  = 0  # 17 - Índice atual da lista para navegação do jogador 2

        self.all_monsters = list(self.p1.simple_surfs.keys())  # 18 - Lista de todos os monstros disponíveis
        self.visible_monsters = 5  # 19 - Quantos monstros são visíveis na tela ao mesmo tempo
        self.max_select = 3  # 20 - Número máximo de monstros que cada jogador pode escolher

    def draw_panel(self, surface, index, center, label, selected):  # 21 - Desenha um painel de seleção de monstros
        font = self.p1.font  # 22 - Usa a mesma fonte do seletor p1
        
        rect = pygame.Rect(center[0] - 210, center[1] - 200, 420, 400)  # 23 - Retângulo do painel
        pygame.draw.rect(surface, COLORS['white'], rect, 0, 4)  # 24 - Preenche o painel com branco
        pygame.draw.rect(surface, COLORS['gray'], rect, 4, 4)  # 25 - Desenha a borda cinza

        label_surf = font.render(label, True, (255, 255, 255))  # 26 - Renderiza o título do painel (Player 1 ou 2)
        surface.blit(label_surf, (rect.centerx - label_surf.get_width() // 2, rect.top - 40))  # 27 - Centraliza o texto

        monster_names = list(self.p1.simple_surfs.keys())  # 28 - Lista de nomes de monstros disponíveis

        v_offset = 0 if index < self.visible_monsters else -(index - self.visible_monsters + 1) * rect.height / self.visible_monsters  # 29 - Corrige o scroll vertical
        for i in range(len(monster_names)):  # 30 - Itera sobre todos os monstros
            x = rect.centerx  # 31 - Posição horizontal central
            y = rect.top + rect.height / (self.visible_monsters * 2) + rect.height / self.visible_monsters * i + v_offset  # 32 - Posição vertical ajustada
            name = self.all_monsters[i]  # 33 - Nome do monstro
            color = COLORS['red'] if name in selected else (COLORS['gray'] if i == index else COLORS['black'])  # 34 - Cor do nome (vermelho se selecionado, cinza se destacado)

            monster_img = self.p1.simple_surfs[name]  # 35 - Imagem do monstro
            img_rect = monster_img.get_frect(center=(x - 100, y))  # 36 - Posição da imagem à esquerda do nome

            name_surf = font.render(name, True, color)  # 37 - Renderiza o nome do monstro
            name_rect = name_surf.get_frect(midleft=(x, y))  # 38 - Posiciona o texto ao lado da imagem

            if rect.collidepoint(name_rect.center):  # 39 - Verifica se o monstro está visível no painel
                surface.blit(name_surf, name_rect)  # 40 - Desenha o nome
                surface.blit(monster_img, img_rect)  # 41 - Desenha a imagem

        selected_text = "Selected: " + ", ".join(selected)  # 42 - Texto com os monstros selecionados
        selected_surf = font.render(selected_text, True, (200, 200, 200))  # 43 - Renderiza o texto
        surface.blit(selected_surf, (rect.centerx - selected_surf.get_width() // 2, rect.bottom + 10))  # 44 - Desenha abaixo do painel

    def run(self):  # 45 - Loop principal da seleção PvP
        selecting_p1 = True  # 46 - Começa com o jogador 1 selecionando
        while self.running:  # 47 - Loop até ambos selecionarem
            self.display_surface.fill((30, 30, 30))  # 48 - Fundo escuro

            rect_width, rect_height = 420, 400  # 49 - Dimensões dos painéis
            rect_y = (WINDOW_HEIGHT - rect_height) // 2  # 50 - Posição vertical dos painéis

            rect1 = pygame.Rect(WINDOW_WIDTH // 5 - rect_width // 2, rect_y, rect_width, rect_height)  # 51 - Painel do jogador 1
            rect2 = pygame.Rect(WINDOW_WIDTH * 7 // 8.8 - rect_width // 2, rect_y, rect_width, rect_height)  # 52 - Painel do jogador 2
            center_y = rect_y + rect_height // 2  # 53 - Centro vertical dos painéis

            self.draw_panel(self.display_surface, self.p1.index, (rect1.centerx, center_y),  # 54 - Desenha painel do jogador 1
                            'Player 1' + (" (Your turn!)" if selecting_p1 else ""), self.p1.selected)
            self.draw_panel(self.display_surface, self.p2.index, (rect2.centerx, center_y),  # 55 - Desenha painel do jogador 2
                            'Player 2' + ("" if selecting_p1 else " (Your turn!)"), self.p2.selected)
            pygame.display.update()  # 56 - Atualiza a tela

            key = pygame.key.get_pressed()  # 57 - Lê as teclas pressionadas
            for event in pygame.event.get():  # 58 - Processa eventos do Pygame
                if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:  # 59 - Sai do jogo
                    self.running = False    # 60 - Encerra o loop principal;
                elif event.type == pygame.KEYDOWN:  # 60 - Se alguma tecla foi pressionada
                    if selecting_p1:  # 61 - Controles do jogador 1
                        if event.key == pygame.K_w:  # 62 - Move para cima
                            self.p1.index = (self.p1.index - 1) % len(self.all_monsters) # 63 - Garante que o índice não saia do intervalo;
                        elif event.key == pygame.K_s:  # 63 - Move para baixo
                            self.p1.index = (self.p1.index + 1) % len(self.all_monsters) # 64 - Garante que o índice não saia do intervalo;
                        elif event.key == pygame.K_d:  # 64 - Seleciona ou remove
                            monster = self.all_monsters[self.p1.index]  # 65 - Obtém o monstro atual;
                            if monster in self.p1.selected: # 66 - Se já estiver selecionado, remove;
                                self.p1.selected.remove(monster)    # 67 - Remove o monstro da seleção do jogador 1;
                            elif len(self.p1.selected) < self.max_select:   # 68 - Se ainda não atingiu o máximo de seleção;
                                self.p1.selected.append(monster)    # 69 - Adiciona o monstro à seleção do jogador 1;
                        if len(self.p1.selected) == self.max_select:  # 65 - Passa a vez ao jogador 2
                            selecting_p1 = False    # 66 - Muda para o jogador 2;
                    else:  # 66 - Controles do jogador 2
                        if event.key == pygame.K_UP:  # 67 - Move para cima
                            self.p2.index = (self.p2.index - 1) % len(self.all_monsters)    # 68 - Garante que o índice não saia do intervalo;
                        elif event.key == pygame.K_DOWN:  # 68 - Move para baixo
                            self.p2.index = (self.p2.index + 1) % len(self.all_monsters)    # 69 - Garante que o índice não saia do intervalo;
                        elif event.key == pygame.K_RIGHT:  # 69 - Seleciona ou remove
                            monster = self.all_monsters[self.p2.index]  # 70 - Obtém o monstro atual;
                            if monster in self.p2.selected:   # 70 - Se já estiver selecionado, remove;
                                self.p2.selected.remove(monster)    # 71 - Remove o monstro da seleção do jogador 2;
                            elif len(self.p2.selected) < self.max_select:   # 71 - Se ainda não atingiu o máximo de seleção;
                                self.p2.selected.append(monster)    # 72 - Adiciona o monstro à seleção do jogador 2;
                        if len(self.p2.selected) == self.max_select:  # 70 - Finaliza seleção
                            self.running = False    # 71 - Encerra o loop principal quando ambos os jogadores selecionarem seus monstros;

            self.clock.tick(15)  # 71 - Limita o FPS da tela de seleção;
        return self.p1.selected, self.p2.selected  # 72 - Retorna os monstros selecionados por ambos os jogadores;