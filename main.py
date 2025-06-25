from settings import *  # Importing settings for game constants and configurations;
from support import *   # Importing support functions for asset loading and other utilities;
from timer import Timer # Importing Timer class for managing timed events;
from monster import *   # Importing Monster and Opponent classes for handling monster data and behaviors;
from random import choice   # Importing choice function for random selections;
from ui import *    # Importing UI classes for managing user interface elements and interactions;
from attack import AttackAnimationSprite    # Importing class for handling attack animations;
from menu import MainMenu   # Importing MainMenu class for the game menu;
from pvpc import PokeSelect # Importing PokeSelect class for selecting monsters in PvP mode;
from pvp import PokePvP # Importing PokePvP class for handling PvP monster selection;
from scenario import *  # Importing scenario-related classes and functions for managing game environments;
from secondp import *   # Importing second player related classes and functions for handling PvP interactions;

class Game:
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
    def __init__(self, selected_monster):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Monster Battle')
        self.clock = pygame.time.Clock()
        self.running = True
        self.import_assets()
        self.audio['music'].play(-1)
        self.player_active = True
        self.monster_lock = threading.Lock() # Lock to ensure thread safety when accessing monster data; **********
        self.opponent_action = []

        #groups
        self.all_sprites = pygame.sprite.Group()

        #data
        player_monster_list = selected_monster
        self.player_monsters = [Monster(name, self.back_surfs[name]) for name in player_monster_list]
        self.monster = self.player_monsters[0]
        self.all_sprites.add(self.monster)
        opponent_name = choice(list(MONSTER_DATA.keys()))
        self.opponent = Opponent(opponent_name, self.front_surfs[opponent_name], self.all_sprites)

        #ui
        self.ui = UI(self.monster, self.player_monsters, self.simple_surfaces, self.get_input)
        self.opponent_ui = OpponentUI(self.opponent)

        #timers
        self.timers = {'player end': Timer(1000, func = self.opponent_turn), 'opponent end': Timer(1000, func = self.player_turn)}

    def get_input(self, state, data = None):
        if state == 'attack':
            self.apply_attack(self.opponent, data)
        elif state == 'heal':
            self.monster.health += 50
            AttackAnimationSprite(self.monster, self.attack_frames['green'], self.all_sprites)
            self.audio['green'].play()
        elif state == 'switch':
            self.monster.kill()
            self.monster = data
            self.all_sprites.add(self.monster)
            self.ui.monster = self.monster

        elif state == 'escape':
            self.running = False
        self.player_active = False
        self.timers['player end'].activate()

    def apply_attack(self, target, attack):
        with self.monster_lock:
            attack_data = ABILITIES_DATA[attack]
            attack_multiplier = ELEMENT_DATA[attack_data['element']][target.element]
            target.health -= attack_data['damage'] * attack_multiplier
            AttackAnimationSprite(target, self.attack_frames[attack_data['animation']], self.all_sprites)
            self.audio[attack_data['animation']].play()

    # This function handles the opponent's turn logic, including monster switching and attack selection; **********************************************
    # It runs in a separate thread to avoid blocking the main game loop, allowing for smoother gameplay;
    # The threading ensures that the game remains responsive while the opponent's actions are being processed; 
    def opponent_turn(self):
        def threaded_opponent_action(): # This function runs in a separate thread to avoid blocking the main game loop; ********************************
            with self.monster_lock:
                if self.opponent.health <= 0:
                    self.player_active = False
                    self.opponent.kill()
                    monster_name = choice(list(MONSTER_DATA.keys()))
                    self.opponent = Opponent(monster_name, self.front_surfs[monster_name], self.all_sprites)
                    self.opponent_ui.monster = self.opponent
                else:
                    attack = choice(self.opponent.abilities)
                    self.opponent_action.append(attack)
            self.timers['opponent end'].activate()
        t = threading.Thread(target=threaded_opponent_action) # Create a thread to handle the opponent's action; *********************
        t.daemon = True
        t.start()

    def player_turn(self):
        self.player_active = True
        if self.monster.health <= 0:
            available_monsters = [monster for monster in self.player_monsters if monster.health > 0]
            if available_monsters:
                self.monster.kill()
                self.monster = available_monsters[0]
                self.all_sprites.add(self.monster)
                self.ui.monster = self.monster
            else:
                self.running = False

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def import_assets(self):
        self.front_surfs = folder_importer('images', 'front')
        self.back_surfs = folder_importer('images', 'back')
        self.bg_surfs = folder_importer('images', 'other')
        self.simple_surfaces = folder_importer('images', 'simple')
        self.attack_frames = tile_importer(4, 'images', 'attacks')
        self.audio = audio_importer('audio')

    def draw_monster_floor(self):
        for sprite in self.all_sprites:
            if isinstance(sprite, Creature):
                floor_rect = self.bg_surfs['floor'].get_rect(center = sprite.rect.midbottom + pygame.Vector2(0, -10))
                self.display_surface.blit(self.bg_surfs['floor'], floor_rect)

    def run(self, bg):
        while self.running:
            dt = self.clock.tick() / 1000
            
            self.key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.key[pygame.K_ESCAPE]:
                    self.running = False

            #update
            self.update_timers()
            self.all_sprites.update(dt)
            if self.player_active:
                self.ui.update()
                
            if self.opponent_action:
                attack = self.opponent_action.pop(0)
                self.apply_attack(self.monster, attack)

            #draw
            self.display_surface.blit(bg, (0,0))
            self.draw_monster_floor()
            self.all_sprites.draw(self.display_surface)
            self.ui.draw()
            self.opponent_ui.draw()
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    menu = MainMenu()
    selected_mode = menu.mode_selected
    
    if selected_mode == 'PvPc':
        simple_surfs = folder_importer('images', 'simple')
        selected_monster = PokeSelect(simple_surfs).run()
        if not selected_monster or selected_monster is False:
            pygame.quit()
            sys.exit()
        else:
            selecao = cenarioSelect()
            cenario_escolhido = selecao.run()
            cenarios = folder_importer('images', 'cenarios')
            if cenario_escolhido is None or cenario_escolhido not in cenarios:
                pygame.quit()
                sys.exit()
            bg = cenarios[cenario_escolhido]
            game = Game(selected_monster)
            game.run(bg)
    elif selected_mode == 'PvP':
        simple_surfs = folder_importer('images', 'simple')
        pvp_select = PokePvP(simple_surfs)
        p1_selected, p2_selected = pvp_select.run()
        if not (p1_selected and p2_selected):
            pygame.quit()
            sys.exit()
        else:
            selecao = cenarioSelect()
            cenario_escolhido = selecao.run()
            cenarios = folder_importer('images', 'cenarios')
            if cenario_escolhido is None or cenario_escolhido not in cenarios:
                pygame.quit()
                sys.exit()
            bg = cenarios[cenario_escolhido]
            game = GamePvP(p1_selected, p2_selected)
            game.run(bg)