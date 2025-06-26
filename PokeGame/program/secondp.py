from settings import *  # 1 - Importa constantes e dados do jogo (como largura da janela e dados dos monstros)
from support import *  # 2 - Importa funções auxiliares (ex: folder_importer)
from monster import *  # 3 - Importa classes relacionadas aos monstros
from ui import *  # 4 - Importa interfaces de usuário
from attack import AttackAnimationSprite  # 5 - Importa classe para animação de ataque
from scenario import *  # 6 - Importa seleção e carregamento de cenário

class GamePvP:  # 7 - Classe principal para o modo jogador vs jogador
    # Monster Battle PvP Game Class
    # Handles the main game loop, player actions, and monster interactions in a PvP setting; **********************************
    # Initializes the game with selected monsters for both players and sets up the game environment;
    def __init__(self, p1_selected, p2_selected):  # 8 - Construtor que recebe os times selecionados pelos jogadores
        pygame.init()  # 9 - Inicializa o pygame
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # 10 - Cria a tela principal
        pygame.display.set_caption('Monster Battle PvP')  # 11 - Define título da janela
        self.clock = pygame.time.Clock()  # 12 - Controlador de tempo do jogo
        self.running = True  # 13 - Flag principal de execução
        self.import_assets()  # 14 - Importa imagens, sons e outros ativos
        self.audio['music'].play(-1)  # 15 - Toca a música em loop
        self.monster_lock = threading.Lock()  # 16 ****** - Lock para controlar acesso entre ações simultâneas; Lock to ensure thread safety when accessing monster data; ******************************************
        self.font = pygame.font.Font(join('data', 'Oxanium-Bold.ttf'))  # 17 - Fonte padrão do jogo
        self.health_lock = threading.Semaphore()  # 18 ****** - Semáforo para evitar acesso simultâneo à vida dos monstros; Semaphore to control access to monster health; ********************************************

        self.all_sprites = pygame.sprite.Group()  # 19 - Grupo de sprites animadas

        self.p1_monsters = [Monster(name, self.back_surfs[name]) for name in p1_selected]  # 20 - Cria monstros do jogador 1
        self.p1_monster = self.p1_monsters[0]  # 21 - Monstro ativo do jogador 1
        self.all_sprites.add(self.p1_monster)  # 22 - Adiciona à lista de animações

        self.p2_monsters = [Monster(name, self.front_surfs[name]) for name in p2_selected]  # 23 - Cria monstros do jogador 2
        self.p2_monster = self.p2_monsters[0]  # 24 - Monstro ativo do jogador 2
        self.all_sprites.add(self.p2_monster)  # 25 - Adiciona à lista de animações

        self.ui = UI(self.p1_monster, self.p1_monsters, self.simple_surfaces, self.get_input)  # 26 - Interface para jogador ativo
        self.p2_ui = OpponentUI(self.p2_monster)  # 27 - Interface de oponente (usada para mostrar o outro monstro)

        self.ready_to_spawn = threading.Event()
        self.wait_switch = False
        self.dead_monster = None
        self.active_player = 1  # 28 - Define quem é o jogador atual (1 ou 2)

    def import_assets(self):  # 29 - Carrega recursos visuais e sonoros
        self.front_surfs = folder_importer('images', 'front')  # 30 - Importa sprites de frente dos monstros
        self.back_surfs = folder_importer('images', 'back')  # 31 - Importa sprites de trás dos monstros
        self.bg_surfs = folder_importer('images', 'other')  # 32 - Importa imagens de fundo e outros elementos
        self.simple_surfaces = folder_importer('images', 'simple')  # 33 - Importa sprites simples dos monstros
        self.attack_frames = tile_importer(4, 'images', 'attacks')  # 34 - Importa frames de animação de ataques
        self.audio = audio_importer('audio')  # 35 - Importa arquivos de áudio (músicas e efeitos sonoros);

    def get_input(self, state, data=None):  # 36 - Trata entrada do jogador atual
        if self.active_player == 1:  # 37 - Verifica se é o turno do jogador 1
            self.ui.monster = self.p1_monster  # 38 - Define monstro ativo na interface do jogador 1
            self.ui.player_monsters = self.p1_monsters  # 39 - Define lista de monstros do jogador 1 na interface;
        else:
            self.ui.monster = self.p2_monster  # 40 - Define monstro ativo na interface do jogador 2;
            self.ui.player_monsters = self.p2_monsters  # 41 - Define lista de monstros do jogador 2 na interface;
        self.p2_ui.monster = self.p2_monster  # 42 - Atualiza monstro ativo na interface do oponente;

        if state == 'attack':  # 43 - Se o jogador atacou
            attacker = self.p1_monster if self.active_player == 1 else self.p2_monster  # 44 - Define o monstro atacante;
            target = self.p2_monster if self.active_player == 1 else self.p1_monster  # 45 - Define o monstro alvo;
            self.apply_attack(attacker, target, data)  # 46 - Aplica o ataque;

        elif state == 'heal':  # 47 - Se o jogador usou cura;
            acting_monster = self.p1_monster if self.active_player == 1 else self.p2_monster  # 48 - Define o monstro que está agindo (curando);

            with self.health_lock:  # 49 ****** - Garante que só um jogador pode alterar a vida de um monstro por vez;
                acting_monster.health += 50  # 50 - Aumenta a vida do monstro que está agindo;
                AttackAnimationSprite(acting_monster, self.attack_frames['green'], self.all_sprites)  # 51 - Cria animação de cura;
                self.audio['green'].play()  # 52 - Toca o som de cura;

        elif state == 'switch':  # 53 - Troca de monstro
            acting_monster = self.p1_monster if self.active_player == 1 else self.p2_monster  # 54 - Define o monstro que está agindo (trocando);
            acting_monster.kill()  # 55 - Remove visualmente;
            acting_monster = data  # 56 - Novo monstro;
            self.all_sprites.add(acting_monster)  # 57 - Adiciona o novo monstro à lista de animações;
            if self.active_player == 1:  # 58 - Verifica se é o turno do jogador 1;
                self.p1_monster = acting_monster  # 59 - Atualiza o monstro ativo do jogador 1;
            else:
                self.p2_monster = acting_monster  # 60 - Atualiza o monstro ativo do jogador 2;
                self.p2_ui.monster = self.p2_monster  # 61 - Atualiza o monstro ativo na interface do oponente;

        elif state == 'escape':  # 62 - Encerrar partida;
            self.running = False  # 63 - Encerra o loop principal do jogo;

        self.active_player = 2 if self.active_player == 1 else 1  # 64 - Alterna turno;
        self.ui.monster = self.p1_monster  # 65 - Atualiza monstro ativo na interface do jogador 1
        self.ui.player_monsters = self.p1_monsters  # 66 - Atualiza lista de monstros do jogador 1 na interface;
        self.p2_ui.monster = self.p2_monster  # 67  - Atualiza monstro ativo na interface do oponente;

    def apply_attack(self, attacker, target, attack):  # 68 - Aplica dano de um ataque ao alvo
        attack_data = ABILITIES_DATA[attack]  # 69  - Obtém dados do ataque (dano, elemento, animação)

        with self.health_lock:  # 70 ****** - Garante consistência no ajuste de vida ao aplicar dano;
            attack_multiplier = ELEMENT_DATA[attack_data['element']][target.element]  # 71 - Calcula multiplicador de dano baseado no elemento do ataque e do alvo;
            target.health -= attack_data['damage'] * attack_multiplier  # 72 - Aplica dano ao alvo com multiplicador de elemento;
            AttackAnimationSprite(target, self.attack_frames[attack_data['animation']], self.all_sprites)  # 73 - Cria animação de ataque no alvo;
            self.audio[attack_data['animation']].play()  # 74 - Toca o som do ataque;

        if target.health <= 0: # 75 - Verifica se o alvo foi derrotado;
            target.health = 0 # 76 - Garante que a vida não fique negativa;
            target.kill() # 77 - Remove o alvo da lista de animações;

            self.wait_switch = True # 78 - Indica que o jogo deve esperar para trocar de monstro;
            self.dead_monster = target # 79 - Armazena o monstro derrotado para troca posterior;
            self.ready_to_spawn.clear() # 80 - Limpa o evento de pronto para spawn;

            threading.Thread(target=self.delayed_spawn, daemon=True).start() # 81 - Inicia thread para esperar antes de trocar de monstro;

    def nextMonster(self, monster_list):  # 89 - Busca o próximo monstro disponível;
        for monster in monster_list:  # 90 - Itera sobre a lista de monstros do jogador;
            if monster.health > 0:  # 91 - Verifica se o monstro ainda está vivo;
                return monster  # 92 - Retorna o primeiro monstro vivo encontrado;
        return None  # 93 - Retorna None se não houver monstros disponíveis;

    def delayed_spawn(self): # 94 - Aguarda um tempo antes de permitir a troca de monstro;
        pygame.time.wait(2000) # 95 - Espera 2 segundos para dar tempo de ver a animação de morte;
        self.ready_to_spawn.set() # 96 - Define o evento de pronto para spawn, permitindo a troca de monstro;

    def winner(self, player):  # 94 - Define o vencedor e encerra o jogo;
        self.show_winner_screen(player) # 95 - Exibe a tela de vencedor;
        self.running = False  # 95 - Encerra o loop principal do jogo;

    # Exibe a tela de vencedor;
    # Displays the winner screen with a message indicating which player won;
    def show_winner_screen(self, player):  # 96 - Exibe a tela de vencedor;
        winner_text = f'Jogador {player} venceu!'   # 96 - Mensagem de vencedor;
        font = pygame.font.Font(join('data', 'Oxanium-Bold.ttf'), 60)   # 97 - Fonte para o texto do vencedor;
        text_surf = font.render(winner_text, True, COLORS['white']) # 98 - Renderiza o texto do vencedor;
        text_rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))  # 99 - Centraliza o texto na tela;

        self.display_surface.fill(COLORS['black'])  # 100 - Limpa a tela com fundo preto;
        self.display_surface.blit(text_surf, text_rect) # 101 - Desenha o texto do vencedor na tela;
        pygame.display.update() # 102 - Atualiza a tela para mostrar o texto;

        pygame.time.wait(10000) # 103 - Aguarda 10 segundos para que o jogador veja a mensagem antes de fechar o jogo;

    def draw_monster_floor(self):  # 96 - Desenha sombra abaixo dos monstros
        for sprite in self.all_sprites:  # 97 - Itera sobre todos os sprites na lista de animações;
            if isinstance(sprite, Creature):  # 98 - Verifica se o sprite é uma criatura;
                floor_rect = self.bg_surfs['floor'].get_rect(center=sprite.rect.midbottom + pygame.Vector2(0, -10))  # 99 - Cria um retângulo para a sombra abaixo do monstro;
                self.display_surface.blit(self.bg_surfs['floor'], floor_rect)  # 100 - Desenha a sombra na tela;

    def run(self, bg):  # 101 - Laço principal do jogo
        while self.running:  # 102 - Enquanto o jogo estiver rodando;
            dt = self.clock.tick() / 1000  # 103 - Delta time (tempo entre frames) em segundos;

            key = pygame.key.get_pressed()  # 104 - Captura as teclas pressionadas;
            for event in pygame.event.get():  # 105 - Processa eventos do Pygame;
                if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:  # 106 - Se o usuário fechar a janela ou apertar ESC;
                    self.running = False  # 107 - Encerra o loop principal;

            self.all_sprites.update(dt)  # 108 - Atualiza animações;

            self.display_surface.blit(bg, (0, 0))  # 109 - Desenha fundo;
            
            # PLAYER 1: posiciona a base do monstro exatamente na base da tela - melhorado;
            self.p1_monster.rect.bottom = WINDOW_HEIGHT # 110 - Ajusta a posição vertical do monstro do jogador 1;
            self.p1_monster.rect.centerx = max(self.p1_monster.rect.width // 2, min(WINDOW_WIDTH // 4, WINDOW_WIDTH - self.p1_monster.rect.width // 2)) # 111 - Ajusta a posição horizontal do monstro do jogador 1;

            # PLAYER 2: evita ultrapassar os limites laterais e a parte superior - melhorado;
            self.p2_monster.rect.bottom = WINDOW_HEIGHT // 2  # Ajuste vertical mais elevado;
            self.p2_monster.rect.centerx = max(self.p2_monster.rect.width // 2, min(WINDOW_WIDTH * 3 // 4, WINDOW_WIDTH - self.p2_monster.rect.width // 2)) # 112 - Ajusta a posição horizontal do monstro do jogador 2;

            self.draw_monster_floor()  # 112 - Desenha a sombra abaixo dos monstros;
            self.all_sprites.draw(self.display_surface)  # 113 - Desenha todos os sprites na tela;

            self.ui.draw()  # 114 - Desenha a interface do jogador 1;
            self.p2_ui.draw()  # 115 - Desenha a interface do oponente (jogador 2);

            if self.wait_switch and self.ready_to_spawn.is_set(): # 116 - Verifica se é hora de trocar de monstro;
                self.wait_switch = False # 117 - Reseta a flag de espera para troca de monstro;
                dead = self.dead_monster # 118 - Obtém o monstro que foi derrotado;
                if dead == self.p1_monster: # 119 - Verifica se o monstro derrotado é do jogador 1;
                    self.p1_monster = self.nextMonster(self.p1_monsters) # 120 - Busca o próximo monstro do jogador 1;
                    if self.p1_monster: # 121 - Se houver um monstro disponível;
                        self.all_sprites.add(self.p1_monster) # 122 - Adiciona o novo monstro à lista de animações;
                        self.ui.monster = self.p1_monster # 123 - Atualiza o monstro ativo na interface do jogador 1;
                    else:
                        self.winner(player=2) # 124 - Se não houver mais monstros, o jogador 2 vence;
                else:
                    self.p2_monster = self.nextMonster(self.p2_monsters) # 125 - Busca o próximo monstro do jogador 2;
                    if self.p2_monster: # 126 - Se houver um monstro disponível;
                        self.all_sprites.add(self.p2_monster) # 127 - Adiciona o novo monstro à lista de animações;
                        self.p2_ui.monster = self.p2_monster # 128 - Atualiza o monstro ativo na interface do jogador 2;
                    else:
                        self.winner(player=1) # 129 - Se não houver mais monstros, o jogador 1 vence;

                self.dead_monster = None # 130 - Reseta o monstro derrotado;

            self.ui.update()  # 116 - Atualiza a interface do jogador 1;
            self.p2_ui.update()  # 117 - Atualiza a interface do oponente (jogador 2);

            pygame.display.update()  # 118 - Atualiza a tela para mostrar as mudanças;
        pygame.quit()  # 119 - Encerra o Pygame quando o loop principal termina;