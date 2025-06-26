from settings import *  # 1 - Importa todas as constantes e dados do arquivo settings.py

def folder_importer(*path):  # 2 - Função para importar imagens de um diretório específico e retornar como dicionário
    surfs = {}  # 3 - Dicionário que armazenará as superfícies carregadas
    for folder_path, _, file_names in walk(join(*path)):  # 4 - Percorre recursivamente os arquivos do caminho especificado
        for file_name in file_names:  # 5 - Itera sobre cada arquivo do diretório
            full_path = join(folder_path, file_name)  # 6 - Gera o caminho completo até o arquivo
            surfs[file_name.split('.')[0]] = pygame.image.load(full_path).convert_alpha()  # 7 - Carrega a imagem e remove fundo (transparente)
    return surfs  # 8 - Retorna dicionário com as imagens carregadas

def audio_importer(*path):  # 9 - Função para importar sons de um diretório
    audio_dict = {}  # 10 - Dicionário que armazenará os sons
    for folder_path, _, file_names in walk(join(*path)):  # 11 - Percorre recursivamente a pasta indicada
        for file_name in file_names:  # 12 - Itera sobre cada arquivo da pasta
            if file_name.endswith('.wav') or file_name.endswith('.ogg') or file_name.endswith('.mp3'):  # 13 - Verifica se é um arquivo de áudio
                full_path = join(folder_path, file_name)  # 14 - Cria caminho completo para o som
                sound = pygame.mixer.Sound(full_path)  # 15 - Carrega o som no mixer do pygame
                sound.set_volume(0.1)  # 16 - Define o volume padrão do som para 10%
                key = file_name.split('.')[0]  # 17 - Usa o nome do arquivo (sem extensão) como chave
                audio_dict[key] = sound  # 18 - Armazena o som no dicionário
    return audio_dict  # 19 - Retorna dicionário com os sons carregados

def tile_importer(cols, *path):  # 20 - Função para importar animações divididas em colunas (spritesheet)
    attack_frames = {}  # 21 - Dicionário que armazenará os quadros de cada animação
    for folder_path, _, file_names in walk(join(*path)):  # 22 - Percorre arquivos da pasta especificada
        for file_name in file_names:  # 23 - Itera sobre cada imagem na pasta
            full_path = join(folder_path, file_name)  # 24 - Caminho completo até o arquivo
            surf = pygame.image.load(full_path).convert_alpha()  # 25 - Carrega a spritesheet com transparência
            attack_frames[file_name.split('.')[0]] = []  # 26 - Cria lista vazia para os quadros da animação

            cutout_width = surf.get_width() / cols  # 27 - Calcula a largura de cada quadro (coluna)
            for col in range(cols):  # 28 - Para cada quadro na linha
                cutout_surf = pygame.Surface((cutout_width, surf.get_height()), pygame.SRCALPHA)  # 29 - Cria superfície transparente para o quadro
                cutout_rect = pygame.FRect(cutout_width * col, 0, cutout_width, surf.get_height())  # 30 - Define a área do quadro a recortar
                cutout_surf.blit(surf, (0, 0), cutout_rect)  # 31 - Recorta e cola o quadro na nova superfície
                attack_frames[file_name.split('.')[0]].append(cutout_surf)  # 32 - Adiciona o quadro à lista da animação
    return attack_frames  # 33 - Retorna dicionário com listas de quadros de animações;