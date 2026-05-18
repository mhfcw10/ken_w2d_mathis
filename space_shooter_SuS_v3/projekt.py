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
    def __init__(self, speed_orange):                                                  
        super().__init__()														# brauchst du nicht zu wissen
        self.image  = pygame.image.load("res/images/Orange.png").convert_alpha()	# Bild laden
        self.image = pygame.transform.scale(self.image, (60,60))				# Bild skalieren (vergrössern/verkleinern)
        self.rect   = self.image.get_rect()										# Umrechteck bestimmen
        self.rect.x = random.randint(50,750)												# x-Startpunkt
        self.rect.y = random.randint(100,300)
        self.speed= speed_orange


class Ziel(pygame.sprite.Sprite):                                        
    def __init__(self):                                                  
        super().__init__()														# brauchst du nicht zu wissen
        self.image  = pygame.image.load("res/images/Ziel Bild.png").convert_alpha()	# Bild laden
        self.image = pygame.transform.scale(self.image, (60,60))				# Bild skalieren (vergrössern/verkleinern)
        self.rect   = self.image.get_rect()										# Umrechteck bestimmen
        self.rect.x = 740					# x-Startpunkt
        self.rect.y = 0

def check_collisions():
    for paceracer in player_sprites:
        if paceracer.rect.colliderect(ziel.rect):
            return "gewonnen"
    for orange in orangen_sprites:
        if orange.rect.colliderect(pace_racer.rect):
            pace_racer.lives -= 1
            orange.kill()

    if pace_racer.lives <= 0:
        return "game_over"

    return "game"
          
            
        
def draw_game():
    screen.blit(background_image_game, (0,0))			# Hintergrund wird gezeichnet an Stelle 0,0
    player_sprites.draw(screen)         				# Objekte in Gruppe player_sprites werden gezeichnet
    orangen_sprites.draw(screen)
    ziel_sprites.draw(screen)
    for i in range(0, pace_racer.lives):
        screen.blit(heart_image, (10 + i * 35, 10))

def move_players():
    keys = pygame.key.get_pressed()						# Abfrage aller Tasten
    if keys[pygame.K_UP] and pace_racer.rect.y > 0:						 	# True falls w gedrückt wird
        pace_racer.rect.y -= pace_racer.speed
    if keys [pygame.K_RIGHT]  and pace_racer.rect.x < screen_width - pace_racer.rect.width:
        pace_racer.rect.x += pace_racer.speed 
    if keys [pygame.K_LEFT]  and pace_racer.rect.x > 0:
        pace_racer.rect.x -= pace_racer.speed
    if keys[pygame.K_DOWN] and pace_racer.rect.y < screen_height - pace_racer.rect.height:
        pace_racer.rect.y += pace_racer.speed

def move_orangen():
    for orange in orangen_sprites:
        orange.rect.y += orange.speed
        if orange.rect.y > screen_height:
            orange.kill()


def draw_game_over():
    screen.blit(game_over_image, (0,0))



def create_orangen(last_spawn_time):
    current_time = pygame.time.get_ticks()

    # neues Ufo nach zufälliger Zeit von 1 bis 4 Sekunden
    if current_time - last_spawn_time > 500 + random.randint(0, 2000):
        orange = Orange(random.randint(2, 7))
        orangen_sprites.add(orange)
        last_spawn_time = current_time

    return last_spawn_time



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

game_over_image = pygame.image.load("res/images/Game Over Bild.png")
game_over_image = pygame.transform.scale(game_over_image, (screen_width, screen_height))

my_bg_music = pygame.mixer.Sound("res/sounds/background_sound.mp3")
pygame.mixer.Sound.play(my_bg_music, -1)
# Spielstatus zu Beginn
game_status = "game"
pace_racer = PaceRacer(screen_width / 100  , screen_height * 3.15 / 4)			 # Erstellen eines Space Ships
orange = Orange(2)
ziel = Ziel()

player_sprites = pygame.sprite.Group()       # Gruppe der player Sprites
player_sprites.add(pace_racer)               # Die Spieler in die Gruppe legen

orangen_sprites = pygame.sprite.Group()       # Gruppe der player Sprites
orangen_sprites.add(orange)

ziel_sprites = pygame.sprite.Group()       # Gruppe der player Sprites
ziel_sprites.add(ziel)


####################################################################################
# Spielschleife
# ----------------------------------------------------------------------------------

last_spawn_time = pygame.time.get_ticks()

is_game_running = True
while is_game_running:
    for event in pygame.event.get():						# Events wie Mausklick werden abgearbeitet
        if event.type == pygame.QUIT:						# Falls auf x geklickt wird
            is_game_running = False
   
    if game_status == "game":
        draw_game()
        move_players()
        last_spawn_time = create_orangen(last_spawn_time)
        move_orangen()
        game_status = check_collisions()

    if game_status == "game_over":
        draw_game_over()

         
    pygame.display.update()  								# Fenster updaten
    clock.tick(60)  							# Setzt die Anzahl Frames per Second auf 60

pygame.quit()