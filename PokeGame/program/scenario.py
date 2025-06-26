from settings import *  # 1 - Importa configurações do jogo (como tamanho da janela, cores, etc.)
from support import folder_importer  # 2 - Importa função para carregar imagens de uma pasta

class cenarioSelect:  # 3 - Classe responsável por exibir a tela de seleção de cenário
    def __init__(self):  # 4 - Construtor da classe
        pygame.init()  # 5 - Inicializa o Pygame
        self.display = Display()  # 6 - Cria o objeto da tela de exibição
        self.display_surface = self.display.display_surface  # 7 - Superfície onde tudo será desenhado
        pygame.display.set_caption('CENARIO')  # 8 - Define o título da janela
        self.running = self.display.running  # 9 - Controla o loop de execução
        self.clock = pygame.time.Clock()  # 10 - Controlador de FPS

        # Importa as imagens dos cenários
        # 11 - Carrega as imagens dos cenários de uma pasta específica;
        original_cenarios = folder_importer('images', 'cenarios')   # 11 - Importa imagens dos cenários da pasta 'images/cenarios';
        self.cenarios = {name: pygame.transform.scale(img, (WINDOW_WIDTH, WINDOW_HEIGHT)) for name, img in original_cenarios.items()}   # 12 - Redimensiona as imagens para caber na janela do jogo; - melhorado;


        self.cenario_names = list(self.cenarios.keys())  # 12 - Lista os nomes dos cenários disponíveis
        self.selected_index = 0  # 13 - Índice do cenário atualmente selecionado
        self.selected_cenario = None  # 14 - Nome do cenário escolhido (retornado ao final)

    def run(self):  # 15 - Método principal que executa a seleção
        while self.running:  # 16 - Loop principal da interface
            key = pygame.key.get_pressed()  # 17 - Captura as teclas pressionadas
            for event in pygame.event.get():  # 18 - Processa os eventos da fila
                if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:  # 19 - Encerra se o usuário fechar a janela ou apertar ESC
                    self.running = False    # 19 - Define running como False para sair do loop principal;
                elif event.type == pygame.KEYDOWN:  # 20 - Verifica se alguma tecla foi pressionada;
                    if event.key == pygame.K_RIGHT:  # 21 - Avança para o próximo cenário;
                        self.selected_index = (self.selected_index + 1) % len(self.cenario_names)   # 21 - Avança para o próximo cenário;
                    elif event.key == pygame.K_LEFT:  # 22 - Volta para o cenário anterior;
                        self.selected_index = (self.selected_index - 1) % len(self.cenario_names)   # 22 - Volta para o cenário anterior;
                    elif event.key == pygame.K_RETURN:  # 23 - Confirma seleção com Enter;
                        self.selected_cenario = self.cenario_names[self.selected_index] # 23 - Define o cenário selecionado;
                        self.running = False    # 24 - Sai do loop principal se Enter for pressionado;

            # Mostra o cenário selecionado como plano de fundo;
            selected_cenario_img = self.cenarios[self.cenario_names[self.selected_index]]  # 24 - Imagem do cenário atual
            self.display_surface.blit(selected_cenario_img, (0, 0))  # 25 - Desenha a imagem como fundo

            # --- Desenho das miniaturas abaixo do fundo principal ---
            thumb_width = 100  # 26 - Largura padrão das miniaturas;
            thumb_height = 100  # 27 - Altura padrão das miniaturas;
            selected_thumb_width = 140  # 28 - Largura da miniatura selecionada;
            selected_thumb_height = 140  # 29 - Altura da miniatura selecionada;
            spacing = 40  # 30 - Espaçamento horizontal entre miniaturas;
            total_width = (len(self.cenario_names) - 1) * (thumb_width + spacing) + selected_thumb_width  # 31 - Largura total da faixa de miniaturas

            screen_width = self.display_surface.get_width()  # 32 - Largura da tela
            thumb_y = self.display_surface.get_height() // 2 + 120  # 33 - Posição vertical das miniaturas
            start_x = (screen_width - total_width) // 2  # 34 - Posição inicial horizontal para centralizar as miniaturas

            x = start_x  # 35 - Inicia a posição horizontal de desenho das miniaturas
            for i, name in enumerate(self.cenario_names):  # 36 - Itera por todos os cenários
                if i == self.selected_index:  # 37 - Se for o cenário selecionado
                    img = pygame.transform.scale(self.cenarios[name], (selected_thumb_width, selected_thumb_height))  # 38 - Redimensiona imagem em destaque
                    rect = img.get_rect(topleft=(x, thumb_y - 20))  # 39 - Posição da miniatura selecionada
                    border_color = (255, 255, 0)  # 40 - Cor da borda amarela para destacar
                    pygame.draw.rect(self.display_surface, border_color, rect.inflate(12, 12), 6)  # 41 - Desenha borda ao redor
                    self.display_surface.blit(img, rect)  # 42 - Desenha a miniatura selecionada
                    x += selected_thumb_width + spacing  # 43 - Avança a posição horizontal
                else:  # 44 - Miniaturas não selecionadas
                    img = pygame.transform.scale(self.cenarios[name], (thumb_width, thumb_height))  # 45 - Redimensiona normalmente
                    rect = img.get_rect(topleft=(x, thumb_y))  # 46 - Posição da miniatura
                    border_color = (255, 255, 255)  # 47 - Cor da borda branca
                    pygame.draw.rect(self.display_surface, border_color, rect.inflate(8, 8), 4)  # 48 - Desenha a borda
                    self.display_surface.blit(img, rect)  # 49 - Desenha a miniatura
                    x += thumb_width + spacing  # 50 - Avança a posição horizontal

            pygame.display.update()  # 51 - Atualiza a tela com todos os elementos desenhados
            self.clock.tick(60)  # 52 - Limita a taxa de atualização a 60 FPS

        return self.selected_cenario  # 53 - Retorna o nome do cenário selecionado;