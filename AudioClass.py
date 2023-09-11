check = True
try:
    import pygame
except ImportError:
    check = False


class PlayAudio:
    def __init__(self) -> None:
        if check == True:
            pygame.init()
            pygame.mixer.init()

            self.sound_path = "sound/"
            self.battleMusicFile = "battle.mid"
            self.battleWinFile = "win.mid"
            self.battleLoseFile = "lose.mid"

            attack_sound = pygame.mixer.Sound(self.sound_path + "/attack.mp3")
            heal_sound   = pygame.mixer.Sound(self.sound_path + "/heal.mp3")
            fail_sound   = pygame.mixer.Sound(self.sound_path + "/fail.mp3")
            pop_sound    = pygame.mixer.Sound(self.sound_path + "/pop.mp3")

            self.sfx_file = {"attack": attack_sound,
                            "heal": heal_sound,
                            "fail": fail_sound,
                            "pop": pop_sound}
            self.vol = 0.7
        else:
            pass
        
    def play_sfx(self, sound):
        if check == True:
            self.sfx_file[sound].play()
        else:
            pass

    def play_battle_music(self):
        if check == True:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.sound_path + self.battleMusicFile)
            pygame.mixer.music.set_volume(self.vol)
            pygame.mixer.music.play(-1)
        else:
            pass

    def play_win_music(self):
        if check == True:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.sound_path + self.battleWinFile)
            pygame.mixer.music.set_volume(self.vol)
            pygame.mixer.music.play()
        else:
            pass

    def play_lose_music(self):
        if check == True:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.sound_path + self.battleLoseFile)
            pygame.mixer.music.set_volume(self.vol)
            pygame.mixer.music.play()
        else:
            pass