from settings import *
from support import folder_importer

class cenarioSelect:
    def __init__(self):
        pygame.init()
        self.display = Display()
        self.display_surface = self.display.display_surface
        pygame.display.set_caption('CENARIO')
        self.running = self.display.running
        self.clock = pygame.time.Clock()

        self.cenarios = folder_importer('images', 'cenarios')
        self.cenario_names = list(self.cenarios.keys())
        self.selected_index = 0
        self.selected_cenario = None

    def run(self):
        while self.running:
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.selected_index = (self.selected_index + 1) % len(self.cenario_names)
                    elif event.key == pygame.K_LEFT:
                        self.selected_index = (self.selected_index - 1) % len(self.cenario_names)
                    elif event.key == pygame.K_RETURN:
                        self.selected_cenario = self.cenario_names[self.selected_index]
                        self.running = False

            # Mostra o cenário selecionado como fundo
            selected_cenario_img = self.cenarios[self.cenario_names[self.selected_index]]
            self.display_surface.blit(selected_cenario_img, (0, 0))

            # Centraliza as miniaturas na tela e destaca o selecionado
            thumb_width = 100
            thumb_height = 100
            selected_thumb_width = 140
            selected_thumb_height = 140
            spacing = 40
            total_width = (len(self.cenario_names) - 1) * (thumb_width + spacing) + selected_thumb_width

            screen_width = self.display_surface.get_width()
            thumb_y = self.display_surface.get_height() // 2 + 120
            start_x = (screen_width - total_width) // 2

            x = start_x
            for i, name in enumerate(self.cenario_names):
                if i == self.selected_index:
                    img = pygame.transform.scale(self.cenarios[name], (selected_thumb_width, selected_thumb_height))
                    rect = img.get_rect(topleft=(x, thumb_y - 20))
                    border_color = (255, 255, 0)
                    pygame.draw.rect(self.display_surface, border_color, rect.inflate(12, 12), 6)
                    self.display_surface.blit(img, rect)
                    x += selected_thumb_width + spacing
                else:
                    img = pygame.transform.scale(self.cenarios[name], (thumb_width, thumb_height))
                    rect = img.get_rect(topleft=(x, thumb_y))
                    border_color = (255, 255, 255)
                    pygame.draw.rect(self.display_surface, border_color, rect.inflate(8, 8), 4)
                    self.display_surface.blit(img, rect)
                    x += thumb_width + spacing

            pygame.display.update()
            self.clock.tick(60)

        return self.selected_cenario