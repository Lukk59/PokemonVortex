from settings import *  # 1 - Importa configurações e constantes globais, se necessário

class Timer:  # 2 - Classe para criar e controlar temporizadores personalizados
    def __init__(self, duration, repeat = False, autostart = False, func = None):  # 3 - Inicializa o timer
        self.duration = duration  # 4 - Duração do timer em milissegundos
        self.start_time = 0  # 5 - Armazena o momento em que o timer foi ativado
        self.active = False  # 6 - Indica se o timer está em execução
        self.repeat = repeat  # 7 - Define se o timer deve reiniciar automaticamente após terminar
        self.func = func  # 8 - Função opcional a ser chamada quando o timer terminar

        if autostart:  # 9 - Se o autostart for True, o timer inicia automaticamente
            self.activate()  # 10 - Ativa o timer

    def __bool__(self):  # 11 - Permite usar o objeto Timer como booleano (ex: if timer:)
        return self.active  # 12 - Retorna True se o timer estiver ativo

    def activate(self):  # 13 - Ativa o timer
        self.active = True  # 14 - Marca o timer como ativo
        self.start_time = pygame.time.get_ticks()  # 15 - Armazena o tempo atual do pygame em milissegundos

    def deactivate(self):  # 16 - Desativa o timer
        self.active = False  # 17 - Marca o timer como inativo
        self.start_time = 0  # 18 - Zera o tempo de início
        if self.repeat:  # 19 - Se estiver configurado para repetir...
            self.activate()  # 20 - ...reativa automaticamente o timer

    def update(self):  # 21 - Deve ser chamado constantemente para verificar se o tempo acabou
        if self.active:  # 22 - Só verifica se o timer estiver ativo
            if pygame.time.get_ticks() - self.start_time >= self.duration:  # 23 - Se passou o tempo programado...
                if self.func and self.start_time != 0: self.func()  # 24 - Executa a função associada, se existir
                self.deactivate()  # 25 - Desativa (ou reinicia, se repeat=True);