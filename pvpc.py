from settings import *

class PokeSelect:
    def __init__(self, simple_surfs):
        pygame.init()
        
        self.display = Display()
        self.display_surface = self.display.display_surface
        pygame.display.set_caption('PokeGame')
        self.running = self.display.running
        
        self.left = WINDOW_WIDTH / 2 - 250
        self.top = WINDOW_HEIGHT / 2 - 70
        self.simple_surfs = simple_surfs
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(join('data', 'Oxanium-Bold.ttf'), 36)
        
        self.all_monsters = list(MONSTER_DATA.keys())
        self.visible_monsters = 5
        self.selected = []
        self.index = 0
        self.max_select = 4
        
    def draw_panel(self, surface, index, center, label, selected):
        font = self.font
 
        label_surf = font.render(label, True, (255, 255, 255))
        surface.blit(label_surf, (center[0] - label_surf.get_width() // 2, center[1] - 120))

        monster_names = list(self.simple_surfs.keys())
        for i, monster_name in enumerate(monster_names):
            y_offset = (i - index) * 60
            x, y = center[0], center[1] + y_offset

            color = COLORS['red'] if monster_name in selected else (COLORS['gray'] if i == index else COLORS['black'])

            monster_img = self.simple_surfs[monster_name]
            img_rect = monster_img.get_rect(center=(x - 100, y))
            name_surf = font.render(monster_name, True, color)
            name_rect = name_surf.get_rect(midleft=(x, y))
            
            if abs(i - index) <= 2:
                surface.blit(name_surf, name_rect)
                surface.blit(monster_img, img_rect)

            surface.blit(name_surf, name_rect)
            surface.blit(monster_img, img_rect)

        selected_text = "Selected: " + ", ".join(selected)
        selected_surf = font.render(selected_text, True, (200, 200, 200))
        surface.blit(selected_surf, (center[0] - selected_surf.get_width() // 2, center[1] + 120))
        
    def menu(self):
        rect = pygame.Rect(self.left + 40, self.top - 140, 420, 400)
        pygame.draw.rect(self.display_surface, COLORS['white'], rect, 0, 4)
        pygame.draw.rect(self.display_surface, COLORS['gray'], rect, 4, 4)
        
        v_offset = 0 if self.index < self.visible_monsters else -(self.index - self.visible_monsters + 1) * rect.height / self.visible_monsters
        for i in range(len(self.all_monsters)):
            x = rect.centerx
            y = rect.top + rect.height / (self.visible_monsters * 2) + rect.height / self.visible_monsters * i + v_offset
            name = self.all_monsters[i]
            color = COLORS['red'] if name in self.selected else (COLORS['gray'] if i == self.index else COLORS['black'])
            
            simple_surf = self.simple_surfs[name]
            simple_rect = simple_surf.get_frect(center = (x - 100, y))
            
            text_surf = self.font.render(name, True, color)
            text_rect = text_surf.get_frect(midleft = (x, y))
            if rect.collidepoint(text_rect.center):
                self.display_surface.blit(text_surf, text_rect)
                self.display_surface.blit(simple_surf, simple_rect)
                
    def draw(self):
        self.menu()
        
    def run(self):
        while self.running:
            self.display_surface.fill((30, 30, 30))
            self.menu()
            pygame.display.update()
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                        self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.index = (self.index - 1) % len(self.all_monsters)
                    elif event.key == pygame.K_DOWN:
                        self.index = (self.index + 1) % len(self.all_monsters)
                    elif event.key == pygame.K_SPACE:
                        monster = self.all_monsters[self.index]
                        if monster in self.selected:
                            self.selected.remove(monster)
                        elif len(self.selected) < self.max_select:
                            self.selected.append(monster)
                    elif event.key == pygame.K_RETURN and len(self.selected) == self.max_select:
                        self.running = False
            self.clock.tick(30)
        return self.selected