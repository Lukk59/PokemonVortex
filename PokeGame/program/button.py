class Button():  # 1 - Define uma classe para criar e gerenciar botões com texto
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):  # 2 - Construtor do botão
        self.base_color = base_color  # 3 - Cor padrão do texto
        self.hovering_color = hovering_color  # 4 - Cor do texto quando o mouse passa sobre o botão
        
        self.pos_x = pos[0]  # 5 - Coordenada X da posição do botão
        self.pos_y = pos[1]  # 6 - Coordenada Y da posição do botão
        
        self.image = image  # 7 - Imagem de fundo do botão (pode ser None)
        self.rect = self.image.get_rect(center = (self.pos_x, self.pos_y))  # 8 - Define o retângulo da imagem com base na posição central
        
        if self.image is None:  # 9 - Se não houver imagem, usa o texto como imagem
            self.image = self.text  # 10 - (Obs: aqui há um erro — `self.text` ainda não foi definido nesta linha)
        
        self.text_input = text_input  # 11 - Texto a ser exibido no botão
        self.font = font  # 12 - Fonte usada para renderizar o texto
        self.text = self.font.render(self.text_input, True, self.base_color)  # 13 - Renderiza o texto com a cor base
        self.text_rect = self.text.get_rect(center = (self.pos_x, self.pos_y))  # 14 - Posiciona o texto no centro do botão
        
    def update(self, display_surface):  # 15 - Atualiza a exibição do botão na tela
        if self.image is not None:  # 16 - Se houver imagem, desenha-a primeiro
            display_surface.blit(self.image, self.rect)  # 17 - Desenha a imagem do botão
        display_surface.blit(self.text, self.text_rect)  # 18 - Desenha o texto por cima da imagem (ou sozinho)

    def checkForInput(self, pos):  # 19 - Verifica se o clique do mouse ocorreu dentro do botão
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):  # 20 - Verifica se as coordenadas estão dentro do retângulo
            return True  # 21 - Retorna verdadeiro se o clique foi dentro do botão
        return False  # 22 - Caso contrário, retorna falso
            
    def changeColors(self, pos):  # 23 - Muda a cor do texto ao passar o mouse sobre o botão
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):  # 24 - Verifica se o mouse está sobre o botão
            self.text = self.font.render(self.text_input, True, 'green')  # 25 - Muda a cor do texto para verde
        else:
            self.text = self.font.render(self.text_input, True, 'white')  # 26 - Volta à cor branca se o mouse sair do botão