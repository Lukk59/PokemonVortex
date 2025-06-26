from settings import *  # 1 - Importa configurações globais, como tamanho da janela e caminhos
from button import Button  # 2 - Importa a classe de botão para uso no menu

class MainMenu:  # 3 - Classe que representa o menu principal do jogo
    def __init__(self):  # 4 - Construtor do menu principal
        pygame.init()  # 5 - Inicializa o Pygame
        
        self.load_font(0)  # 6 - Carrega a fonte (tamanho 0 usado apenas para garantir inicialização)
        self.display = Display()  # 7 - Cria o objeto de exibição da tela
        self.display_surface = self.display.display_surface  # 8 - Superfície onde tudo será desenhado
        pygame.display.set_caption('PokeGame')  # 9 - Define o título da janela
        self.running = self.display.running  # 10 - Verifica se o menu está rodando
        self.clock = pygame.time.Clock()  # 11 - Controla o FPS
        self.mode_selected = None  # 12 - Armazena o modo escolhido pelo jogador
        
        self.backg_frames = self.load_gif(join('images/menu', 'Tela-Inicial.gif'))  # 13 - Carrega os frames do GIF de fundo
        self.frame_count = len(self.backg_frames)  # 14 - Total de frames da animação
        self.frame_idx = 0  # 15 - Índice atual do frame exibido

        while self.running:  # 16 - Loop principal do menu inicial
            self.display_surface.blit(self.backg_frames[self.frame_idx], (0, 0))  # 17 - Desenha o frame atual na tela
            self.frame_idx = (self.frame_idx + 1) % self.frame_count  # 18 - Atualiza o frame para a próxima iteração
            
            keys = pygame.key.get_pressed()  # 19 - Captura teclas pressionadas
            for event in pygame.event.get():  # 20 - Itera sobre os eventos do Pygame
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:  # 21 - Sai do jogo se fechar janela ou pressionar ESC
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:  # 22 - Se pressionar alguma tecla
                    if event.key == pygame.K_RETURN:  # 23 - Se for ENTER, abre submenu
                        self.running = False
                        self.mode_selected = self.SubMenu()  # 24 - Executa o submenu
        
            self.clock.tick(30)  # 25 - Mantém 30 frames por segundo
            pygame.display.update()  # 26 - Atualiza a tela com as mudanças
            
    def SubMenu(self):  # 27 - Cria e exibe o submenu com os modos de jogo
        self.load_font(0)  # 28 - Recarrega a fonte
        self.running = True  # 29 - Ativa o loop do submenu
        self.frame_idx = 0  # 30 - Reinicia o frame da animação
        
        # 31 - Cria botão PvP;
        self.pvp_button = Button(image = pygame.image.load(join('images/menu', 'Play Rect.png')).convert_alpha(),   #  # 31 - Carrega imagem do botão PvP;
                                  pos = (WINDOW_WIDTH // 2, 250), text_input = 'PvP',   # 32 - Define posição e texto do botão PvP;
                                  font = self.load_font(75), base_color = '#d7fcd4',    # 33 - Define cor base do botão PvP;
                                  hovering_color = '#ffffff')   # 34 - Define cor ao passar o mouse sobre o botão PvP;
        
        # 32 - Cria botão PvPc;
        self.pvpc_button = Button(image = pygame.image.load(join('images/menu', 'Play Rect.png')).convert_alpha(),  # 35 - Carrega imagem do botão PvPc;
                                  pos = (WINDOW_WIDTH // 2, 350), text_input = 'PvPc',  # 36 - Define posição e texto do botão PvPc;
                                  font = self.load_font(75), base_color = '#d7fcd4',    # 37 - Define cor base do botão PvPc;
                                  hovering_color = '#ffffff')   # 38 - Define cor ao passar o mouse sobre o botão PvPc;
        
        while self.running:  # 33 - Loop do submenu;
            self.mouse_pos = pygame.mouse.get_pos()  # 34 - Captura posição atual do mouse;
            
            self.display_surface.blit(self.backg_frames[self.frame_idx], (0, 0))  # 35 - Desenha o frame de fundo
            self.frame_idx = (self.frame_idx + 1) % self.frame_count  # 36 - Atualiza o frame

            for event in pygame.event.get():  # 37 - Processa eventos
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # 38 - Fecha o jogo;
                    pygame.quit()   # 39 - Encerra o Pygame;
                    sys.exit()  # 40 - Sai do programa;
                if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:  # 39 - Volta ao menu anterior
                    self.running = False    # 40 - Encerra o loop do submenu;
                    return None # 41 - Retorna None para voltar ao menu principal;
                elif event.type == pygame.MOUSEBUTTONDOWN:  # 40 - Clique do mouse;
                    mode = self.checkMode(self.mouse_pos, self.pvp_button, self.pvpc_button)  # 41 - Verifica se clicou em algum botão
                    if mode:    # 42 - Se um modo foi selecionado;
                        self.running = False    # 43 - Encerra o loop do submenu;
                        return mode  # 42 - Retorna modo selecionado;

            self.pvp_button.changeColors(self.mouse_pos)  # 43 - Altera cor do botão PvP se mouse estiver sobre ele
            self.pvp_button.update(self.display_surface)  # 44 - Desenha o botão PvP
            
            self.pvpc_button.changeColors(self.mouse_pos)  # 45 - Altera cor do botão PvPc
            self.pvpc_button.update(self.display_surface)  # 46 - Desenha o botão PvPc
            
            pygame.display.update()  # 47 - Atualiza a tela
            self.clock.tick(30)  # 48 - Limita o FPS do submenu

    def checkMode(self, pos, pvp_button, pvpc_button):  # 49 - Verifica qual botão foi clicado
        if hasattr(self, 'pvp_button') and self.pvp_button.checkForInput(pos):  # 50 - Clicou no PvP?
             return 'PvP'   # 50 - Retorna 'PvP' se o botão PvP foi clicado;
        if hasattr(self, 'pvpc_button') and self.pvpc_button.checkForInput(pos):  # 51 - Clicou no PvPc?
            return 'PvPc'   # 51 - Retorna 'PvPc' se o botão PvPc foi clicado;
        return None  # 52 - Nenhum botão clicado;
    
    # 53 - Carrega um GIF animado e converte seus frames para imagens do Pygame;
    # Utiliza a biblioteca PIL para manipulação de imagens;
    def load_gif(self, path):  # 53 - Carrega e converte um GIF animado para frames do Pygame
        pil_img = Image.open(path)  # 54 - Abre o GIF com PIL
        frames = []  # 55 - Lista de frames;
        # Verifica se o GIF tem múltiplos frames;
        # Se sim, converte cada frame para uma imagem do Pygame;
        try:
            while True:  # 56 - Loop até acabar os frames
                frame = pil_img.convert('RGBA').copy()  # 57 - Converte e copia o frame atual
                mode = frame.mode  # 58 - Modo de cor
                size = frame.size  # 59 - Tamanho do frame
                data = frame.tobytes()  # 60 - Converte imagem para bytes
                py_image = pygame.image.fromstring(data, size, mode)  # 61 - Converte para imagem do Pygame
                py_image = pygame.transform.smoothscale(py_image, (WINDOW_WIDTH, WINDOW_HEIGHT))  # 62 - Redimensiona
                frames.append(py_image)  # 63 - Adiciona à lista
                pil_img.seek(pil_img.tell() + 1)  # 64 - Vai para o próximo frame
        except EOFError:  # 65 - Fim do GIF
            pass    #  - Ignora erro de fim de arquivo;
        return frames  # 66 - Retorna os frames carregados;

    def load_font(self, size):  # 67 - Carrega a fonte com tamanho especificado;
        return pygame.font.Font(join('data', 'Oxanium-Bold.ttf'), size)  # 68 - Retorna fonte carregada;