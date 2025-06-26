from settings import *  # 1 - Importa configurações globais do jogo
from support import *  # 2 - Importa funções utilitárias de suporte
from timer import Timer  # 3 - Importa classe Timer para eventos com atraso
from monster import *  # 4 - Importa classes relacionadas aos monstros
from random import choice  # 5 - Importa função para escolher ataques aleatórios
from ui import *  # 6 - Importa a interface do jogador e do oponente
from attack import AttackAnimationSprite  # 7 - Importa a animação dos ataques
from menu import MainMenu  # 8 - Importa o menu principal
from pvpc import PokeSelect  # 9 - Importa a seleção de Pokémon para PvPc
from pvp import PokePvP  # 10 - Importa a seleção de Pokémon para PvP
from scenario import *  # 11 - Importa seleção de cenário
from secondp import *  # 12 - Importa lógica para segundo jogador

class Game:  # 13 - Classe principal para o modo PvPc
    # Monster Battle Game Class;
    # Handles the main game loop, player actions, and monster interactions in a single-player setting;
    # Initializes the game with selected monsters and sets up the game environment;
    # The game runs in a loop, allowing the player to perform actions like attacking, healing, switching monsters, or escaping;
    # The opponent's actions are handled in a separate thread to ensure smooth gameplay without blocking the main loop; *********************
    # The game also includes a timer system to manage turn transitions and actions;
    # This class is responsible for managing the game state, rendering graphics, and processing user input;
    # It uses Pygame for graphics and audio, and it incorporates threading to handle the opponent's actions without freezing the game; ******************
    # threading is used to ensure that the game remains responsive while the opponent's actions are being processed; *********************
    # The game features a turn-based combat system where the player can choose actions such as attacking, healing, or switching monsters;
    # The player can also escape from the battle, and the game ends when either the player or the opponent runs out of health;
    # The game includes a UI for displaying monster stats and available actions, and it handles monster switching, attacks, and healing actions;
    # The game ends when either the player or the opponent runs out of health, and it allows the player to escape or switch monsters during their turn;
    def __init__(self, selected_monster, enemy_team):  # 14 - Inicializa o jogo
        pygame.init()  # 15 - Inicia o Pygame
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # 16 - Cria a janela principal
        pygame.display.set_caption('Monster Battle')  # 17 - Define o título da janela
        self.clock = pygame.time.Clock()  # 18 - Cria o relógio para controlar FPS
        self.running = True  # 19 - Flag de controle do loop principal
        self.winner = None  # <- define o vencedor como None no início &
        self.import_assets()  # 20 - Carrega todos os recursos (sprites, áudio etc.)
        self.audio['music'].play(-1)  # 21 - Toca a música de fundo em loop
        self.player_active = True  # 22 - Indica se é a vez do jogador

        self.monster_lock = threading.Lock()  # 23 ****** - Cria um semáforo (lock) para controlar acesso aos dados do monstro; Lock to ensure thread safety when accessing monster data; *********
        self.opponent_action = []  # 24 - Lista para armazenar ações do oponente pendentes

        self.all_sprites = pygame.sprite.Group()  # 25 - Grupo que armazena todos os sprites da cena

        player_monster_list = selected_monster  # 26 - Lista de nomes dos monstros escolhidos pelo jogador
        self.player_monsters = [Monster(name, self.back_surfs[name]) for name in player_monster_list]  # 27 - Cria objetos dos monstros
        self.monster = self.player_monsters[0]  # 28 - Define o primeiro monstro ativo
        self.all_sprites.add(self.monster)  # 29 - Adiciona o monstro ao grupo de sprites
        self.enemy_team = enemy_team  # 30 - Equipe inimiga (nomes)
        self.enemy_index = 0  # 31 - Índice do inimigo atual
        first_enemy_name = self.enemy_team[0]  # 32 - Nome do primeiro oponente
        self.opponent = Opponent(first_enemy_name, self.front_surfs[first_enemy_name], self.all_sprites)  # 33 - Cria oponente inicial

        self.ui = UI(self.monster, self.player_monsters, self.simple_surfaces, self.get_input)  # 34 - Interface do jogador
        self.opponent_ui = OpponentUI(self.opponent)  # 35 - Interface do oponente

        self.timers = {  # 36 - Dicionário de timers para controle dos turnos
            'player end': Timer(1000, func=self.opponent_turn),  # 37 - Timer para passar ao turno do oponente
            'opponent end': Timer(1000, func=self.player_turn)  # 38 - Timer para devolver o turno ao jogador
        }

    def get_input(self, state, data=None):  # 39 - Recebe entrada da UI e executa a ação correspondente
        if state == 'attack':  # 40 - Se a ação for ataque
            self.apply_attack(self.opponent, data)  # 41 - Aplica ataque no oponente
        elif state == 'heal':  # 42 - Se for cura
            self.monster.health += 50  # 43 - Cura o monstro
            AttackAnimationSprite(self.monster, self.attack_frames['green'], self.all_sprites)  # 44 - Animação de cura
            self.audio['green'].play()  # 45 - Toca áudio de cura
        elif state == 'switch':  # 46 - Se for troca
            self.monster.kill()  # 47 - Remove o monstro atual
            self.monster = data  # 48 - Substitui pelo novo
            self.all_sprites.add(self.monster)  # 49 - Adiciona à cena
            self.ui.monster = self.monster  # 50 - Atualiza a UI
        elif state == 'escape':  # 51 - Se o jogador quiser fugir
            self.running = False  # 52 - Encerra o jogo

        self.player_active = False  # 53 - Desativa a jogada do jogador
        self.timers['player end'].activate()  # 54 - Ativa o timer para o turno do oponente

    def apply_attack(self, target, attack):  # 55 - Aplica um ataque em um alvo
        with self.monster_lock:  # 56 ****** - Garante exclusividade de acesso aos dados do monstro (evita race conditions)
            attack_data = ABILITIES_DATA[attack]  # 57 - Dados da habilidade
            attack_multiplier = ELEMENT_DATA[attack_data['element']][target.element]  # 58 - Multiplicador baseado nos elementos
            target.health -= attack_data['damage'] * attack_multiplier  # 59 - Reduz a vida do alvo
            AttackAnimationSprite(target, self.attack_frames[attack_data['animation']], self.all_sprites)  # 60 - Animação do ataque
            self.audio[attack_data['animation']].play()  # 61 - Toca o som do ataque
            
            if target.health <= 0:  # 62 - Se o alvo morreu
                target.kill()  # 63 - Remove o sprite

    # This function handles the opponent's turn logic, including monster switching and attack selection; **********************************************
    # It runs in a separate thread to avoid blocking the main game loop, allowing for smoother gameplay;
    # The threading ensures that the game remains responsive while the opponent's actions are being processed; 
    def opponent_turn(self):  # 64 - Define o turno do oponente
        def threaded_opponent_action():  # 65 - Ação interna que roda em thread; This function runs in a separate thread to avoid blocking the main game loop; ********************************
            with self.monster_lock:  # 66 ****** - Protege a lógica de ataque e troca do oponente
                if self.opponent.health <= 0:  # 67 - Se o oponente morreu
                    self.opponent.kill()  # 68 - Remove sprite
                    self.enemy_index += 1  # 69 - Passa para o próximo inimigo
                    if self.enemy_index < len(self.enemy_team):  # 70 - Se ainda há inimigos
                        next_name = self.enemy_team[self.enemy_index]  # 71 - Próximo inimigo
                        self.opponent = Opponent(next_name, self.front_surfs[next_name], self.all_sprites)  # 72 - Novo oponente
                        self.opponent_ui.monster = self.opponent  # 73 - Atualiza UI
                    else:
                        self.winner = '1'  # 74 - Vitória do jogador
                        self.running = False  # 74 - Vitória do jogador
                        #self.show_winner_screen(player='1')  # Jogador venceu; &
                        return
                else:
                    attack = choice(self.opponent.abilities)  # 75 - Escolhe um ataque aleatório
                    self.opponent_action.append(attack)  # 76 - Adiciona ataque à fila de ações
            self.timers['opponent end'].activate()  # 77 - Ativa o timer para devolver o turno ao jogador

        t = threading.Thread(target=threaded_opponent_action)  # 78 ****** - Cria uma thread para ação do oponente; Create a thread to handle the opponent's action; *********************
        t.daemon = True  # 79 - Define a thread como daemon
        t.start()  # 80 - Inicia a thread

    def player_turn(self):  # 81 - Define o início do turno do jogador
        self.player_active = True  # 82 - Libera controle ao jogador
        if self.monster.health <= 0:  # 83 - Se o monstro do jogador morreu
            available_monsters = [m for m in self.player_monsters if m.health > 0]  # 84 - Busca outros vivos
            if available_monsters:  # 85 - Se houver
                self.monster.kill()  # 86 - Remove o atual
                self.monster = available_monsters[0]  # 87 - Troca
                self.all_sprites.add(self.monster)  # 88 - Adiciona
                self.ui.monster = self.monster  # 89 - Atualiza UI
            else:   # 90 - Se não houver mais monstros vivos;
                self.winner = 'Pc'  # 90 - Computador venceu
                self.running = False  # 90 - Derrota
                #self.show_winner_screen(player='Pc')  # Computador venceu; &

    def update_timers(self):  # 91 - Atualiza todos os timers
        for timer in self.timers.values():  # 92 - Loop nos timers
            timer.update()  # 93 - Atualiza cada um

    def import_assets(self):  # 94 - Importa todos os recursos gráficos e sonoros
        self.front_surfs = folder_importer('images', 'front')  # 95 - Sprites dos monstros vistos de frente;
        self.back_surfs = folder_importer('images', 'back')  # 96 - Sprites dos monstros vistos de costas;
        self.bg_surfs = folder_importer('images', 'other')  # 97 - Sprites de fundo e outros elementos;
        self.simple_surfaces = folder_importer('images', 'simple')  # 98 - Sprites simples para seleção de Pokémon;
        self.attack_frames = tile_importer(4, 'images', 'attacks')  # 99 - Animações dos ataques;
        self.audio = audio_importer('audio')  # 100 - Importa todos os sons do jogo;

    def draw_monster_floor(self):  # 101 - Desenha o chão abaixo dos monstros;
        for sprite in self.all_sprites:  # 102 - Loop por todos os sprites;
            if isinstance(sprite, Creature):  # 103 - Se for um monstro;
                floor_rect = self.bg_surfs['floor'].get_rect(center = sprite.rect.midbottom + pygame.Vector2(0, -10))  # 104 - Posição do chão abaixo do monstro;
                self.display_surface.blit(self.bg_surfs['floor'], floor_rect)  # 105 - Desenha o chão na tela;

    def show_winner_screen(self, player):  # 127 - Mostra a tela de vitória;
        winner_text = f'Jogador {player} venceu!'   # 127 - Mensagem de vitória
        font = pygame.font.Font(join('data', 'Oxanium-Bold.ttf'), 60) # 127 - Fonte para o texto de vitória
        text_surf = font.render(winner_text, True, COLORS['white']) # 128 - Renderiza o texto
        text_rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))  # 129 - Centraliza o texto na tela

        self.display_surface.fill(COLORS['black'])  # 130 - Limpa a tela com fundo preto
        self.display_surface.blit(text_surf, text_rect) # 131 - Desenha o texto na tela
        pygame.display.update() # 132 - Atualiza a tela

        pygame.time.wait(10000)  # 133 - Espera 10 segundos antes de fechar o jogo;

        pygame.quit()        # Encerra o Pygame corretamente
        sys.exit()           # Finaliza a execução do programa

    def run(self, bg):  # 106 - Loop principal do jogo
        while self.running:  # 107
            dt = self.clock.tick() / 1000  # 108 - Delta time entre frames

            self.key = pygame.key.get_pressed()  # 109 - Captura teclas pressionadas
            for event in pygame.event.get():  # 110
                if event.type == pygame.QUIT or self.key[pygame.K_ESCAPE]:  # 111 - Fecha o jogo se apertar ESC ou sair
                    self.running = False  # 112

            self.update_timers()  # 113 - Atualiza timers
            self.all_sprites.update(dt)  # 114 - Atualiza todos os sprites
            if self.player_active:  # 115
                self.ui.update()  # 116

            if self.opponent_action:  # 117 - Se há ações do oponente pendentes
                attack = self.opponent_action.pop(0)  # 118 - Pega o próximo ataque
                self.apply_attack(self.monster, attack)  # 119 - Aplica no jogador

            self.display_surface.blit(bg, (0,0))  # 120 - Desenha fundo
            self.draw_monster_floor()  # 121 - Desenha o chão
            self.all_sprites.draw(self.display_surface)  # 122 - Desenha os sprites
            self.ui.draw()  # 123 - Desenha a UI do jogador
            self.opponent_ui.draw()  # 124 - Desenha a UI do oponente
            pygame.display.update()  # 125 - Atualiza a tela;

        if self.winner: # 126 - Se houver um vencedor
            self.show_winner_screen(self.winner)    # 126 - Mostra a tela de vitória ou derrota;

            # Forma melhor de ser feito encontrada;
            # Verifica se algum monstro morreu e atualiza o estado do jogo
            #if self.monster.health <= 0:    # 126 - Se o monstro do jogador morreu
            #    self.show_winner_screen('Pc')   # 126 - Mostra tela de derrota
            #elif self.opponent.health <= 0: # 126 - Se o monstro do oponente morreu
            #    self.show_winner_screen('1')    # 126 - Mostra tela de vitória

        pygame.quit()  # 126 - Sai do Pygame ao fim do loop;

    


# Execução principal
if __name__ == '__main__':  # 127 - Verifica se o script é o principal
    menu = MainMenu()  # 128 - Cria o menu principal
    selected_mode = menu.mode_selected  # 129 - Lê o modo selecionado
    import random  # 130 - Importa o random para seleção de inimigos

    if selected_mode == 'PvPc':  # 131 - Se for jogador vs computador
        simple_surfs = folder_importer('images', 'simple')  # 132 - Importa sprites simples;
        selected_monster = PokeSelect(simple_surfs).run()  # 133 - Abre menu de seleção de monstros
        all_names = list(MONSTER_DATA.keys())  # 134 - Lista de todos os nomes de monstros;
        enemy_team = random.sample(all_names, 6)  # 135 - Gera time inimigo;

        if not selected_monster or selected_monster is False:  # 136 - Se o jogador não selecionou um monstro;
            pygame.quit(); sys.exit()  # 137 - Encerra caso o jogador cancele
        else:
            selecao = cenarioSelect()  # 138 - Seleciona cenário
            cenario_escolhido = selecao.run()  # 139 Seleciona cenário escolhido pelo jogador;
            cenarios = folder_importer('images', 'cenarios')  # 140 - Importa cenários disponíveis;
            # Verifica se o cenário escolhido é válido;
            if cenario_escolhido is None or cenario_escolhido not in cenarios:  # 141 - Se o cenário não for válido;
                pygame.quit(); sys.exit()  # 142 - Encerra o jogo se não for válido;
            bg = cenarios[cenario_escolhido]  # 143 - Define o fundo do jogo com o cenário escolhido;
            game = Game(selected_monster, enemy_team)  # 144 - Cria a instância do jogo com o monstro selecionado e time inimigo;
            game.run(bg)  # 145 - Inicia o jogo;

    elif selected_mode == 'PvP':  # 146 - Se for jogador vs jogador;
        simple_surfs = folder_importer('images', 'simple')  # 147 - Importa sprites simples para seleção de Pokémon;
        pvp_select = PokePvP(simple_surfs)  # 148 - Cria a instância de seleção de Pokémon para PvP;
        p1_selected, p2_selected = pvp_select.run()  # 149 - Executa a seleção de Pokémon para PvP;
        if not (p1_selected and p2_selected):  # 150 - Se algum jogador não selecionou um Pokémon;
            pygame.quit(); sys.exit()  # 151 - Encerra o jogo se não houver seleção válida;
        else:
            selecao = cenarioSelect()  # 152 - Seleciona cenário para o jogo PvP;
            cenario_escolhido = selecao.run()  # 153 - Seleciona o cenário escolhido pelo jogador;
            cenarios = folder_importer('images', 'cenarios')  # 154 - Importa cenários disponíveis;
            if cenario_escolhido is None or cenario_escolhido not in cenarios:  # 155 - Se o cenário não for válido;
                pygame.quit(); sys.exit()  # 156 - Encerra o jogo se não for válido;
            bg = cenarios[cenario_escolhido]  # 157 - Define o fundo do jogo com o cenário escolhido;
            game = GamePvP(p1_selected, p2_selected)  # 158 - Cria a instância do jogo PvP com os Pokémon selecionados;
            game.run(bg)  # 159 - Inicia jogo PvP;