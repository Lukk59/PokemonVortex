from settings import *  # 1 - Importa as configurações globais definidas no arquivo settings.py (cores, FPS, etc.)

class AttackAnimationSprite(pygame.sprite.Sprite):  # 2 - Define uma classe para representar animações de ataque como sprites animados
    def __init__(self, target, frames, groups):  # 3 - Construtor da classe, recebe o alvo, os quadros da animação e os grupos de sprites
        super().__init__(groups)  # 4 - Inicializa a sprite base e adiciona este sprite aos grupos fornecidos
        self.frames, self.frame_index = frames, 0  # 5 - Armazena os quadros da animação e inicializa o índice de quadros
        self.image = self.frames[self.frame_index]  # 6 - Define a imagem atual da sprite como o primeiro quadro da animação
        self.rect = self.image.get_frect(center = target.rect.center)  # 7 - Posiciona a sprite no centro do alvo

    def update(self, dt):  # 8 - Método chamado a cada frame para atualizar a animação; recebe o delta time (dt)
        self.frame_index += 5 * dt  # 9 - Avança o índice da animação com base no tempo decorrido (5 quadros por segundo)
        if self.frame_index < len(self.frames):  # 10 - Se ainda houver quadros restantes na animação
            self.image = self.frames[int(self.frame_index)]  # 11 - Atualiza a imagem atual com base no novo índice
        else:  # 12 - Quando todos os quadros já foram exibidos
            self.kill()  # 13 - Remove a sprite do(s) grupo(s) e da memória (animação finalizada)
