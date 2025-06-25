class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.base_color = base_color
        self.hovering_color = hovering_color
        
        #coordinates
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        
        #rect
        self.image = image
        self.rect = self.image.get_rect(center = (self.pos_x, self.pos_y))
        
        if self.image is None:
            self.image = self.text
        
        #text_input
        self.text_input = text_input
        self.font = font
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center = (self.pos_x, self.pos_y))
        
    def update(self, display_surface):
        if self.image is not None:
            display_surface.blit(self.image, self.rect)
        display_surface.blit(self.text, self.text_rect)
        
    def checkForInput(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
            
    def changeColors(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, 'green')
        else:
            self.text = self.font.render(self.text_input, True, 'white')