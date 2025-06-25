from settings import *  # Import game settings and constants;
from support import *   # Import utility functions for file handling and audio;
from monster import *   # Import monster-related classes and data;
from ui import *    # Import user interface classes for displaying game information;
from attack import AttackAnimationSprite    # Import class for handling attack animations;
from scenario import *  # Import scenario-related classes and data for the game environment;

# GamePvP.py 
class GamePvP:
    # Monster Battle PvP Game Class
    # Handles the main game loop, player actions, and monster interactions in a PvP setting; **********************************
    # Initializes the game with selected monsters for both players and sets up the game environment;
    def __init__(self, p1_selected, p2_selected):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Monster Battle PvP')
        self.clock = pygame.time.Clock()
        self.running = True
        self.import_assets()
        self.audio['music'].play(-1)
        self.monster_lock = threading.Lock() # Lock to ensure thread safety when accessing monster data; ******************************************
        self.font = pygame.font.Font(join('data', 'Oxanium-Bold.ttf'))
        self.health_lock = threading.Semaphore() # Semaphore to control access to monster health; ********************************************

        #groups
        self.all_sprites = pygame.sprite.Group()

        #player 1
        self.p1_monsters = [Monster(name, self.back_surfs[name]) for name in p1_selected]
        self.p1_monster = self.p1_monsters[0]
        self.all_sprites.add(self.p1_monster)

        #player
        self.p2_monsters = [Monster(name, self.front_surfs[name]) for name in p2_selected]
        self.p2_monster = self.p2_monsters[0]
        self.all_sprites.add(self.p2_monster)

        #uis
        self.ui = UI(self.p1_monster, self.p1_monsters, self.simple_surfaces, self.get_input)
        self.p2_ui = OpponentUI(self.p2_monster)

        #turns
        self.active_player = 1

    def import_assets(self):
        self.front_surfs = folder_importer('images', 'front')
        self.back_surfs = folder_importer('images', 'back')
        self.bg_surfs = folder_importer('images', 'other')
        self.simple_surfaces = folder_importer('images', 'simple')
        self.attack_frames = tile_importer(4, 'images', 'attacks')
        self.audio = audio_importer('audio')

    def get_input(self, state, data = None):
        if self.active_player == 1:
            self.ui.monster = self.p1_monster
            self.ui.player_monsters = self.p1_monsters
        else:
            self.ui.monster = self.p2_monster
            self.ui.player_monsters = self.p2_monsters
        self.p2_ui.monster = self.p2_monster
            
        if state == 'attack':
            attacker = self.p1_monster if self.active_player == 1 else self.p2_monster
            target = self.p2_monster if self.active_player == 1 else self.p1_monster
            
            self.apply_attack(attacker, target, data)
            
        elif state == 'heal':
            acting_monster = self.p1_monster if self.active_player == 1 else self.p2_monster
            
            with self.health_lock:
                acting_monster.health += 50
                AttackAnimationSprite(acting_monster, self.attack_frames['green'], self.all_sprites)
                self.audio['green'].play()
                
        elif state == 'switch':
            acting_monster = self.p1_monster if self.active_player == 1 else self.p2_monster
            acting_monster.kill()
            acting_monster = data
            self.all_sprites.add(acting_monster)
            if self.active_player == 1:
                self.p1_monster = acting_monster
            else:
                self.p2_monster = acting_monster
                self.p2_ui.monster = self.p2_monster
                
        elif state == 'escape':
            self.running = False
            
        self.active_player = 2 if self.active_player == 1 else 1    
        self.ui.monster = self.p1_monster
        self.ui.player_monsters = self.p1_monsters
        self.p2_ui.monster = self.p2_monster

    def apply_attack(self, attacker, target, attack):
        attack_data = ABILITIES_DATA[attack]
        
        with self.health_lock:
            attack_multiplier = ELEMENT_DATA[attack_data['element']][target.element]
            target.health -= attack_data['damage'] * attack_multiplier
            AttackAnimationSprite(target, self.attack_frames[attack_data['animation']], self.all_sprites)
            self.audio[attack_data['animation']].play()
            
        if target.health <= 0:
            target.health = 0
            target.kill()

            if target == self.p1_monster:
                self.p1_monster = self.nextMonster(self.p1_monsters)
                if self.p1_monster:
                    self.all_sprites.add(self.p1_monster)
                    self.ui.monster = self.p1_monster
                else:
                    self.winner(player = 2)

            else:
                self.p2_monster = self.nextMonster(self.p2_monsters)
                if self.p2_monster:
                    self.all_sprites.add(self.p2_monster)
                    self.p2_ui.monster = self.p2_monster
                else:
                    self.winner(player = 1)
                    
    def nextMonster(self, monster_list):
        for monster in monster_list:
            if monster.health > 0:
                return monster
        return None
    
    def winner(self, player):
        self.running = False

    def draw_monster_floor(self):
        for sprite in self.all_sprites:
            if isinstance(sprite, Creature):
                floor_rect = self.bg_surfs['floor'].get_rect(center=sprite.rect.midbottom + pygame.Vector2(0, -10))
                self.display_surface.blit(self.bg_surfs['floor'], floor_rect)

    def run(self, bg):
        while self.running:
            dt = self.clock.tick() / 1000
            
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                    self.running = False
                    
            self.all_sprites.update(dt)       

            self.display_surface.blit(bg, (0, 0))
            self.p1_monster.rect.midbottom = (WINDOW_WIDTH // 4, WINDOW_HEIGHT)
            self.p2_monster.rect.midbottom = (WINDOW_WIDTH * 3 // 4, WINDOW_HEIGHT // 2 - 100)
            
            self.draw_monster_floor()
            self.all_sprites.draw(self.display_surface)
            
            self.ui.draw()
            self.p2_ui.draw()
            
            self.ui.update()
            self.p2_ui.update()
            
            pygame.display.update()
        pygame.quit()