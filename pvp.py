from settings import *
from pvpc import *

class PokePvP():
    def __init__(self, simples_surfs):
        pygame.init()
        self.display = Display()
        self.display_surface = self.display.display_surface
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.p1 = PokeSelect(simples_surfs)
        self.p2 = PokeSelect(simples_surfs)
        self.p1.left = WINDOW_WIDTH / 2 - 550
        self.p2.left = (WINDOW_WIDTH * 3) // 4 - 200
        
        self.p1.selected = []
        self.p2.selected = []
        self.p1.index = 0
        self.p2.index  = 0
        
        self.all_monsters = list(self.p1.simple_surfs.keys())
        self.visible_monsters = 5
        self.max_select = 1
        
    def draw_panel(self, surface, index, center, label, selected):
        font = self.p1.font  
        
        rect = pygame.Rect(center[0] - 210, center[1] - 200, 420, 400)
        pygame.draw.rect(surface, COLORS['white'], rect, 0, 4)
        pygame.draw.rect(surface, COLORS['gray'], rect, 4, 4)

        label_surf = font.render(label, True, (255, 255, 255))
        surface.blit(label_surf, (rect.centerx - label_surf.get_width() // 2, rect.top - 40))

        monster_names = list(self.p1.simple_surfs.keys())

        v_offset = 0 if index < self.visible_monsters else -(index - self.visible_monsters + 1) * rect.height / self.visible_monsters
        for i in range(len(monster_names)):
            x = rect.centerx
            y = rect.top + rect.height / (self.visible_monsters * 2) + rect.height / self.visible_monsters * i + v_offset
            name = self.all_monsters[i]
            color = COLORS['red'] if name in selected else (COLORS['gray'] if i == index else COLORS['black'])

            monster_img = self.p1.simple_surfs[name]
            img_rect = monster_img.get_frect(center=(x - 100, y))

            name_surf = font.render(name, True, color)
            name_rect = name_surf.get_frect(midleft=(x, y))

            if rect.collidepoint(name_rect.center):
                surface.blit(name_surf, name_rect)
                surface.blit(monster_img, img_rect)

        selected_text = "Selected: " + ", ".join(selected)
        selected_surf = font.render(selected_text, True, (200, 200, 200))
        surface.blit(selected_surf, (rect.centerx - selected_surf.get_width() // 2, rect.bottom + 10))


    def run(self):
        selecting_p1 = True
        while self.running:
            self.display_surface.fill((30, 30, 30))

            rect_width, rect_height = 420, 400
            rect_y = (WINDOW_HEIGHT - rect_height) // 2

            rect1 = pygame.Rect(WINDOW_WIDTH // 8 - rect_width // 2, rect_y, rect_width, rect_height)
            rect2 = pygame.Rect(WINDOW_WIDTH * 7 // 8 - rect_width // 2, rect_y, rect_width, rect_height)
            center_y = rect_y + rect_height // 2

            # Draw both panels using the improved menu logic
            self.draw_panel(self.display_surface, self.p1.index, (rect1.centerx, center_y),
                            'Player 1' + (" (Your turn!)" if selecting_p1 else ""), self.p1.selected)
            self.draw_panel(self.display_surface, self.p2.index, (rect2.centerx, center_y),
                            'Player 2' + ("" if selecting_p1 else " (Your turn!)"), self.p2.selected)
            pygame.display.update()

            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if selecting_p1:
                        if event.key == pygame.K_w:
                            self.p1.index = (self.p1.index - 1) % len(self.all_monsters)
                        elif event.key == pygame.K_s:
                            self.p1.index = (self.p1.index + 1) % len(self.all_monsters)
                        elif event.key == pygame.K_d:
                            monster = self.all_monsters[self.p1.index]
                            if monster in self.p1.selected:
                                self.p1.selected.remove(monster)
                            elif len(self.p1.selected) < self.max_select:
                                self.p1.selected.append(monster)
                        if len(self.p1.selected) == self.max_select:
                            selecting_p1 = False
                    else:
                        if event.key == pygame.K_UP:
                            self.p2.index = (self.p2.index - 1) % len(self.all_monsters)
                        elif event.key == pygame.K_DOWN:
                            self.p2.index = (self.p2.index + 1) % len(self.all_monsters)
                        elif event.key == pygame.K_RIGHT:
                            monster = self.all_monsters[self.p2.index]
                            if monster in self.p2.selected:
                                self.p2.selected.remove(monster)
                            elif len(self.p2.selected) < self.max_select:
                                self.p2.selected.append(monster)
                        if len(self.p2.selected) == self.max_select:
                            self.running = False

            self.clock.tick(15)
        return self.p1.selected, self.p2.selected