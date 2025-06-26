from settings import *  # 1 - Importa configurações globais, como dimensões da janela, cores e dados dos monstros

class PokeSelect:  # 2 - Classe que permite ao jogador selecionar monstros para jogar
    def __init__(self, simple_surfs):  # 3 - Construtor da classe recebe os sprites simples dos monstros
        pygame.init()  # 4 - Inicializa o Pygame
        
        self.display = Display()  # 5 - Cria a janela principal
        self.display_surface = self.display.display_surface  # 6 - Superfície onde os elementos serão desenhados
        pygame.display.set_caption('PokeGame')  # 7 - Define o título da janela
        self.running = self.display.running  # 8 - Controla o loop de execução do menu
        
        self.left = WINDOW_WIDTH / 2 - 250  # 9 - Posição X inicial do painel
        self.top = WINDOW_HEIGHT / 2 - 70  # 10 - Posição Y inicial do painel
        self.simple_surfs = simple_surfs  # 11 - Armazena os sprites dos monstros
        
        self.clock = pygame.time.Clock()  # 12 - Controlador de FPS
        self.font = pygame.font.Font(join('data', 'Oxanium-Bold.ttf'), 36)  # 13 - Fonte usada no menu
        
        self.all_monsters = list(MONSTER_DATA.keys())  # 14 - Lista com todos os nomes de monstros disponíveis
        self.visible_monsters = 5  # 15 - Quantos monstros aparecem simultaneamente na lista
        self.selected = []  # 16 - Lista de monstros selecionados
        self.index = 0  # 17 - Índice atual da seleção
        self.max_select = 4  # 18 - Número máximo de monstros que podem ser escolhidos

    def draw_panel(self, surface, index, center, label, selected):  # 19 - Desenha o painel de seleção (não utilizado no `run`)
        font = self.font  # 20 - Fonte usada para renderizar textos

        label_surf = font.render(label, True, (255, 255, 255))  # 21 - Renderiza o título (label)
        surface.blit(label_surf, (center[0] - label_surf.get_width() // 2, center[1] - 120))  # 22 - Centraliza o título

        monster_names = list(self.simple_surfs.keys())  # 23 - Lista os nomes dos monstros
        for i, monster_name in enumerate(monster_names):  # 24 - Itera sobre todos os monstros
            y_offset = (i - index) * 60  # 25 - Calcula o deslocamento vertical relativo ao monstro destacado
            x, y = center[0], center[1] + y_offset  # 26 - Define as coordenadas do item

            color = COLORS['red'] if monster_name in selected else (COLORS['gray'] if i == index else COLORS['black'])  # 27 - Define cor do texto

            monster_img = self.simple_surfs[monster_name]  # 28 - Imagem do monstro
            img_rect = monster_img.get_rect(center=(x - 100, y))  # 29 - Posição da imagem
            name_surf = font.render(monster_name, True, color)  # 30 - Renderiza o nome do monstro
            name_rect = name_surf.get_rect(midleft=(x, y))  # 31 - Posição do nome ao lado da imagem
            
            if abs(i - index) <= 2:  # 32 - Só desenha se estiver dentro do número visível
                surface.blit(name_surf, name_rect)  # 33 - Desenha nome
                surface.blit(monster_img, img_rect)  # 34 - Desenha sprite

            surface.blit(name_surf, name_rect)  # 35 - Desenha nome novamente (duplicado desnecessariamente)
            surface.blit(monster_img, img_rect)  # 36 - Desenha sprite novamente (duplicado)

        selected_text = "Selected: " + ", ".join(selected)  # 37 - Texto com os nomes dos selecionados
        selected_surf = font.render(selected_text, True, (200, 200, 200))  # 38 - Renderiza o texto
        surface.blit(selected_surf, (center[0] - selected_surf.get_width() // 2, center[1] + 120))  # 39 - Desenha abaixo da lista

    def menu(self):  # 40 - Função que desenha o menu de seleção principal
        rect = pygame.Rect(self.left + 40, self.top - 140, 420, 400)  # 41 - Cria o retângulo do painel
        pygame.draw.rect(self.display_surface, COLORS['white'], rect, 0, 4)  # 42 - Desenha fundo branco
        pygame.draw.rect(self.display_surface, COLORS['gray'], rect, 4, 4)  # 43 - Desenha borda cinza
        
        v_offset = 0 if self.index < self.visible_monsters else -(self.index - self.visible_monsters + 1) * rect.height / self.visible_monsters  # 44 - Corrige a rolagem vertical
        for i in range(len(self.all_monsters)):  # 45 - Itera sobre todos os monstros
            x = rect.centerx  # 46 - Centro horizontal do painel
            y = rect.top + rect.height / (self.visible_monsters * 2) + rect.height / self.visible_monsters * i + v_offset  # 47 - Posição vertical de cada monstro
            name = self.all_monsters[i]  # 48 - Nome do monstro
            color = COLORS['red'] if name in self.selected else (COLORS['gray'] if i == self.index else COLORS['black'])  # 49 - Cor do texto
            
            simple_surf = self.simple_surfs[name]  # 50 - Sprite do monstro
            simple_rect = simple_surf.get_frect(center = (x - 100, y))  # 51 - Posição do sprite
            
            text_surf = self.font.render(name, True, color)  # 52 - Renderiza nome do monstro
            text_rect = text_surf.get_frect(midleft = (x, y))  # 53 - Define posição do nome
            if rect.collidepoint(text_rect.center):  # 54 - Se estiver dentro da área visível
                self.display_surface.blit(text_surf, text_rect)  # 55 - Desenha o nome
                self.display_surface.blit(simple_surf, simple_rect)  # 56 - Desenha o sprite

    def draw(self):  # 57 - Método auxiliar para desenhar o menu
        self.menu()  # 58 - Chama o menu

    def run(self):  # 59 - Loop principal de execução do menu de seleção
        while self.running:  # 60 - Enquanto estiver rodando
            self.display_surface.fill((30, 30, 30))  # 61 - Fundo cinza escuro
            self.menu()  # 62 - Desenha o menu
            pygame.display.update()  # 63 - Atualiza a tela
            key = pygame.key.get_pressed()  # 64 - Verifica teclas pressionadas
            for event in pygame.event.get():  # 65 - Processa os eventos da fila
                if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:  # 66 - Sai do jogo ao fechar ou apertar ESC
                        self.running = False    # 66 - Encerra o loop principal;
                elif event.type == pygame.KEYDOWN:  # 67 - Evento de tecla pressionada
                    if event.key == pygame.K_UP:  # 68 - Navega para cima na lista
                        self.index = (self.index - 1) % len(self.all_monsters)  # 68 - Garante que o índice não saia do intervalo;
                    elif event.key == pygame.K_DOWN:  # 69 - Navega para baixo na lista;
                        self.index = (self.index + 1) % len(self.all_monsters)  # 69 - Garante que o índice não saia do intervalo;
                    elif event.key == pygame.K_SPACE:  # 70 - Seleciona ou desseleciona um monstro;
                        monster = self.all_monsters[self.index] # 70 - Obtém o monstro atual;
                        if monster in self.selected:    # 70 - Se já estiver selecionado, remove;
                            self.selected.remove(monster)   # 70 - Remove o monstro da lista de selecionados;
                        elif len(self.selected) < self.max_select:  # 71 - Se ainda não atingiu o máximo de seleção;
                            self.selected.append(monster)   # 71 - Adiciona o monstro à lista de selecionados;
                    elif event.key == pygame.K_RETURN and len(self.selected) == self.max_select:  # 71 - Finaliza a seleção
                        self.running = False    # 72 - Encerra o loop principal se a seleção estiver completa;
            self.clock.tick(30)  # 72 - Limita o FPS para 30;
        return self.selected  # 73 - Retorna a lista de monstros selecionados;