from settings import *
from button import Button

class MainMenu:
    def __init__(self):
        pygame.init()
        
        self.load_font(0)
        self.display = Display()
        self.display_surface = self.display.display_surface
        pygame.display.set_caption('PokeGame')
        self.running = self.display.running
        self.clock = pygame.time.Clock()
        self.mode_selected = None
        
        self.backg_frames = self.load_gif(join('images/menu', 'Tela-Inicial.gif'))
        self.frame_count = len(self.backg_frames)
        self.frame_idx = 0

        while self.running:
            self.display_surface.blit(self.backg_frames[self.frame_idx], (0, 0))
            self.frame_idx = (self.frame_idx + 1) % self.frame_count
            
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.running = False
                        self.mode_selected = self.SubMenu()
                    
            self.clock.tick(30)
            pygame.display.update()
            
    def SubMenu(self):
        self.load_font(0)
        self.running = True
        self.frame_idx = 0
        
        self.pvp_button = Button(image = pygame.image.load(join('images/menu', 'Play Rect.png')).convert_alpha(), 
                                  pos = (WINDOW_WIDTH // 2, 250), text_input = 'PvP', 
                                  font = self.load_font(75), base_color = '#d7fcd4', 
                                  hovering_color = '#ffffff')
        
        self.pvpc_button = Button(image = pygame.image.load(join('images/menu', 'Play Rect.png')).convert_alpha(), 
                                  pos = (WINDOW_WIDTH // 2, 350), text_input = 'PvPc', 
                                  font = self.load_font(75), base_color = '#d7fcd4', 
                                  hovering_color = '#ffffff')
        
        while self.running:
            self.mouse_pos = pygame.mouse.get_pos()
            
            self.display_surface.blit(self.backg_frames[self.frame_idx], (0, 0))
            self.frame_idx = (self.frame_idx + 1) % self.frame_count
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                    self.running = False
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mode = self.checkMode(self.mouse_pos, self.pvp_button, self.pvpc_button)
                    if mode:
                        self.running = False
                        return mode
            
            self.pvp_button.changeColors(self.mouse_pos)
            self.pvp_button.update(self.display_surface)
            
            self.pvpc_button.changeColors(self.mouse_pos)
            self.pvpc_button.update(self.display_surface)
            
            pygame.display.update()
            self.clock.tick(30)
        
    def checkMode(self, pos, pvp_button, pvpc_button):
        if hasattr(self, 'pvp_button') and self.pvp_button.checkForInput(pos):
             return 'PvP'
        if hasattr(self, 'pvpc_button') and self.pvpc_button.checkForInput(pos):
            return 'PvPc'
        return None

    def load_gif(self, path):
        pil_img = Image.open(path)
        frames = []
        try:
            while True:
                frame = pil_img.convert('RGBA').copy()
                mode = frame.mode
                size = frame.size
                data = frame.tobytes()
                py_image = pygame.image.fromstring(data, size, mode)
                py_image = pygame.transform.smoothscale(py_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
                frames.append(py_image)
                pil_img.seek(pil_img.tell() + 1)
        except EOFError:
            pass
        return frames
    
    def load_font(self, size):
        return pygame.font.Font(join('data', 'Oxanium-Bold.ttf'), size)