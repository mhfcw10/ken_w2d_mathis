import pygame
import random

# Pygame initalisieren
pygame.init()

####################################################################################
# Baupläne (=Klassendefinitionen)
# ----------------------------------------------------------------------------------

class PaceRacer(pygame.sprite.Sprite):                                        
    def __init__(self, x_coordinate, y_coordinate):                                                  
        super().__init__()														# brauchst du nicht zu wissen
        self.image  = pygame.image.load("res/images/PaceRacer.png").convert_alpha()	# Bild laden
        self.image = pygame.transform.scale(self.image, (75,125))				# Bild skalieren (vergrössern/verkleinern)
        self.rect   = self.image.get_rect()										# Umrechteck bestimmen
        self.rect.x = x_coordinate												# x-Startpunkt
        self.rect.y = y_coordinate												# y-Startpunkt
        self.speed = 10
        self.lives = 3

class Orange(pygame.sprite.Sprite):                                        
    def __init__(self, x_coordinate, y_coordinate):                                                  
        super().__init__()														# brauchst du nicht zu wissen
        self.image  = pygame.image.load("res/images/Orange.png").convert_alpha()	# Bild laden
        self.image = pygame.transform.scale(self.image, (60,60))				# Bild skalieren (vergrössern/verkleinern)
        self.rect   = self.image.get_rect()										# Umrechteck bestimmen
        self.rect.x = x_coordinate												# x-Startpunkt
        self.rect.y = y_coordinate	


def draw_game():
    screen.blit(background_image_game, (0,0))			# Hintergrund wird gezeichnet an Stelle 0,0
    player_sprites.draw(screen)         				# Objekte in Gruppe player_sprites werden gezeichnet
    orangen_sprites.draw(screen)

    for i in range(0, pace_racer.lives):
        screen.blit(heart_image, (10 + i * 35, 10))

def move_players():
    keys = pygame.key.get_pressed()						# Abfrage aller Tasten
    if keys[pygame.K_UP]: 							 	# True falls w gedrückt wird
        pace_racer.rect.y -= pace_racer.speed
    if keys [pygame.K_RIGHT]:
        pace_racer.rect.x += pace_racer.speed 
    if keys [pygame.K_LEFT]:
        pace_racer.rect.x -= pace_racer.speed
    if keys[pygame.K_DOWN]:
        pace_racer.rect.y += pace_racer.speed

####################################################################################
# Globale variablen initialisieren
# ----------------------------------------------------------------------------------

# Grösse des Spielfenster setzen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))		# Fenstergrösse festlegen
pygame.display.set_caption("Space Shooter")							# Titel des Fensters setzen
clock = pygame.time.Clock() 					   					# Eine Pygame-Uhr um die Framerate zu kontrollieren


# Hintergrundbilder auf https://www.freepik.com/
background_image_game = pygame.image.load("res/images/orangenbaum.png")		# Hintergrundbild laden
background_image_game = pygame.transform.scale(background_image_game, (screen_width, screen_height))	# Hintergrundbild skalieren

heart_image = pygame.image.load("res/images/heart.png").convert_alpha()
heart_image = pygame.transform.scale(heart_image, (25, 22))

# Spielstatus zu Beginn
game_status = "game"
pace_racer = PaceRacer(screen_width / 100  , screen_height * 3.15 / 4)			 # Erstellen eines Space Ships
orange = Orange(screen_width/2, screen_height/2)

player_sprites = pygame.sprite.Group()       # Gruppe der player Sprites
player_sprites.add(pace_racer)               # Die Spieler in die Gruppe legen

orangen_sprites = pygame.sprite.Group()       # Gruppe der player Sprites
orangen_sprites.add(orange)
####################################################################################
# Spielschleife
# ----------------------------------------------------------------------------------

is_game_running = True
while is_game_running:
    for event in pygame.event.get():						# Events wie Mausklick werden abgearbeitet
        if event.type == pygame.QUIT:						# Falls auf x geklickt wird
            is_game_running = False
   
    if game_status == "game":
        draw_game()
        move_players()

         
    pygame.display.update()  								# Fenster updaten
    clock.tick(60)  							# Setzt die Anzahl Frames per Second auf 60

pygame.quit()