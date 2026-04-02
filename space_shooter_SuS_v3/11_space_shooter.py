import pygame
import random

# Pygame initalisieren
pygame.init()

####################################################################################
# Baupläne (=Klassendefinitionen)
# ----------------------------------------------------------------------------------

class SpaceShip(pygame.sprite.Sprite):                                        
    def __init__(self, x_coordinate, y_coordinate):                                                  
        super().__init__()														# brauchst du nicht zu wissen
        self.image  = pygame.image.load("res/images/space_ship.png").convert_alpha()	# Bild laden
        self.image = pygame.transform.scale(self.image, (46,100))				# Bild skalieren (vergrössern/verkleinern)
        self.rect   = self.image.get_rect()										# Umrechteck bestimmen
        self.rect.x = x_coordinate												# x-Startpunkt
        self.rect.y = y_coordinate												# y-Startpunkt
        self.speed  = 2                                      					# Geschwindigkeit des Spielers
        self.lives = 3

class Ufo(pygame.sprite.Sprite):                                        
    def __init__(self, ufo_speed):                                                  
        super().__init__()														# brauchst du nicht zu wissen
        self.image  = pygame.image.load("res/images/ufo.png").convert_alpha()	# Bild laden
        self.image = pygame.transform.scale(self.image, (100,56))				# Bild skalieren (vergrössern/verkleinern)
        self.rect   = self.image.get_rect()										# Umrechteck bestimmen
        self.rect.x = random.randint(0, screen_width - self.rect.width)			# x-Startpunkt
        self.rect.y = -self.rect.height											# y-Startpunkt
        self.speed  = ufo_speed                                					# Geschwindigkeit des Spielers


####################################################################################
# Funktionsdefinitionen
# ----------------------------------------------------------------------------------

def move_players():
    keys = pygame.key.get_pressed()						# Abfrage aller Tasten
    if keys[pygame.K_w] and space_ship.rect.y > 0:  	# True falls w gedrückt wird
        space_ship.rect.y -= space_ship.speed			# Änderung der y-Koordinate des Space Ship
    if keys[pygame.K_s] and space_ship.rect.y < screen_height - space_ship.rect.height:  								# True falls s gedrückt wird
        space_ship.rect.y += space_ship.speed			# Änderung der y-Koordinate des Space Ship
    if keys[pygame.K_a] and space_ship.rect.x > 0:  	# True falls a gedrückt wird
        space_ship.rect.x -= space_ship.speed			# Änderung der x-Koordinate des Space Ship
    if keys[pygame.K_d] and space_ship.rect.x < screen_width - space_ship.rect.width:  								# True falls d gedrückt wird
        space_ship.rect.x += space_ship.speed			# Änderung der x-Koordinate des Space Ship
    
    if keys[pygame.K_UP] and space_ship2.rect.y > 0:  								# True falls Pfeiltaste nach oben gedrückt wird
        space_ship2.rect.y -= space_ship2.speed			# Änderung der y-Koordinate des Space Ship 2
    if keys[pygame.K_DOWN] and space_ship2.rect.y < screen_height - space_ship2.rect.height:  							# True falls Pfeiltaste nach unten gedrückt wird
        space_ship2.rect.y += space_ship2.speed			# Änderung der y-Koordinate des Space Ship 2
    if keys[pygame.K_LEFT] and space_ship2.rect.x > 0:  							# True falls Pfeiltaste nach links gedrückt wird
        space_ship2.rect.x -= space_ship2.speed			# Änderung der x-Koordinate des Space Ship 2
    if keys[pygame.K_RIGHT] and space_ship2.rect.x < screen_width - space_ship2.rect.width:  							# True falls Pfeiltaste nach rechts gedrückt wird
        space_ship2.rect.x += space_ship2.speed			# Änderung der x-Koordinate des Space Ship 2

def move_ufos():
    for ufo in ufo_sprites:
        ufo.rect.y += ufo.speed
        if ufo.rect.y > screen_height:
            ufo.kill()

def create_ufos(last_spawn_time):
    current_time = pygame.time.get_ticks()
    # Überprüfen, ob es Zeit ist, ein neues Ufo zu erstellen
    if current_time - last_spawn_time > 1000 + random.randint(0, 3000):  # 3 seconds + 0-5 random
        ufo = Ufo(random.randint(2,7))
        ufo_sprites.add(ufo)
        last_spawn_time = current_time
    return last_spawn_time

def check_collisions():
    for ufo in ufo_sprites:
        if ufo.rect.colliderect(space_ship.rect):
            space_ship.lives -= 1
            ufo.kill()
        if ufo.rect.colliderect(space_ship2.rect):
            space_ship2.lives -= 1
            ufo.kill()

def check_game_over():
    if space_ship.lives == 0 or space_ship2.lives == 0:
        return "game_over"
    return "game"

def draw_game():
    screen.blit(background_image_game, (0,0))			# Hintergrund wird gezeichnet an Stelle 0,0
    player_sprites.draw(screen)         				# Objekte in Gruppe player_sprites werden gezeichnet
    ufo_sprites.draw(screen)
    for i in range(0, space_ship.lives):
        screen.blit(heart_image, (10 + i * 35, 10))
    for i in range(0, space_ship2.lives):
        screen.blit(heart_image, (screen_width - 35 - i * 35, 10))
        
def draw_game_over():
    screen.fill((0,0,0))
    screen.blit(text,(screen_width/2 - text.get_width()/2, screen_height/4))   	# Text zeichnen
    

####################################################################################
# Globale variablen initialisieren
# ----------------------------------------------------------------------------------

# Grösse des Spielfenster setzen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))		# Fenstergrösse festlegen
pygame.display.set_caption("Space Shooter")							# Titel des Fensters setzen
clock = pygame.time.Clock() 					   					# Eine Pygame-Uhr um die Framerate zu kontrollieren

my_font = pygame.font.SysFont('Comic Sans MS', 96)     		   		# Schrift und Schriftgrösse laden
game_over_text = "Game Over"										# Game Over Text
text = my_font.render(game_over_text, True, (255,0,0))        		# Textfarbe

# Hintergrundbilder auf https://www.freepik.com/
background_image_game = pygame.image.load("res/images/background_game.jpg")		# Hintergrundbild laden
background_image_game = pygame.transform.scale(background_image_game, (screen_width, screen_height))	# Hintergrundbild skalieren

# Bild für Leben
heart_image = pygame.image.load("res/images/heart.png").convert_alpha()
heart_image = pygame.transform.scale(heart_image, (25, 22))

# Musik laden und abspielen
my_bg_music = pygame.mixer.Sound("res/sounds/background_sound.mp3")
pygame.mixer.Sound.play(my_bg_music, -1)

# Spielstatus zu Beginn
game_status = "game"
space_ship = SpaceShip(screen_width / 3, screen_height * 3 / 4)			 # Erstellen eines Space Ships
space_ship2 = SpaceShip(screen_width * 2/ 3, screen_height * 3 / 4)			 # Erstellen eines Space Ships

player_sprites = pygame.sprite.Group()       # Gruppe der player Sprites
player_sprites.add(space_ship)               # Die Spieler in die Gruppe legen
player_sprites.add(space_ship2)

ufo = Ufo(2)
ufo_sprites = pygame.sprite.Group()
ufo_sprites.add(ufo)

last_spawn_time = pygame.time.get_ticks()


####################################################################################
# Spielschleife
# ----------------------------------------------------------------------------------

is_game_running = True
while is_game_running:
    for event in pygame.event.get():						# Events wie Mausklick werden abgearbeitet
        if event.type == pygame.QUIT:						# Falls auf x geklickt wird
            is_game_running = False
   
    if game_status == "game":
        move_players()
        last_spawn_time = create_ufos(last_spawn_time)
        move_ufos()
        check_collisions()
        game_status = check_game_over()
        draw_game()
        
    if game_status == "game_over":
        draw_game_over()
         
    pygame.display.update()  								# Fenster updaten
    pygame.time.Clock().tick(60)  							# Setzt die Anzahl Frames per Second auf 60

pygame.quit()