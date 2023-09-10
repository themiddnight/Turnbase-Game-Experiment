import pygame
pygame.init()
pygame.mixer.init()
firstSound = pygame.mixer.music("/Users/Pathompong/Downloads/pokemon.mid")
secondSound = pygame.mixer.music("/Users/Pathompong/Downloads/cavern.mid")
firstSound.play()
secondSound.play()