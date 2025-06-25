from settings import *

def folder_importer(*path):
    surfs = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            surfs[file_name.split('.')[0]] = pygame.image.load(full_path).convert_alpha()
    return surfs

def audio_importer(*path):
    audio_dict = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            if file_name.endswith('.wav') or file_name.endswith('.ogg') or file_name.endswith('.mp3'):
                full_path = join(folder_path, file_name)
                sound = pygame.mixer.Sound(full_path)
                sound.set_volume(0.1)
                key = file_name.split('.')[0]
                audio_dict[key] = sound
    return audio_dict

def tile_importer(cols, *path):
    attack_frames = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            surf = pygame.image.load(full_path).convert_alpha()
            attack_frames[file_name.split('.')[0]] = []
            cutout_width = surf.get_width() / cols
            for col in range(cols):
                cutout_surf = pygame.Surface((cutout_width, surf.get_height()), pygame.SRCALPHA)
                cutout_rect = pygame.FRect(cutout_width * col, 0, cutout_width, surf.get_height())
                cutout_surf.blit(surf, (0, 0), cutout_rect)
                attack_frames[file_name.split('.')[0]].append(cutout_surf)
    return attack_frames