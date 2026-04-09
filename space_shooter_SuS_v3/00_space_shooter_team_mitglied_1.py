import pygame
import random
# adfafk
# Pygame initialisieren
pygame.init()
        # Hilfsfunktion, um Bilder zu laden 
def load_images(path,names,ending,number,xpix,ypix): 
# In Animation werden die Pygame-Bilder gespeichert 
    animation = [] 
    for i in range(number): 
        file_name = path + names + str(i) + ending 
        img = pygame.image.load(file_name).convert_alpha()  
        animation.append(pygame.transform.scale(img, (xpix, ypix))) 
    return animation 

class Button(pygame.sprite.Sprite):
    def __init__(self,path,names,ending,number,xpix,ypix):
        super().__init__()
        self.list_images = load_images(path,names,ending,number,xpix,ypix)
        self.image = self.list_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = screen_width / 2
        self.rect.y = screen_height / 2

    
####################################################################################
# Baupläne (=Klassendefinitionen)
# ----------------------------------------------------------------------------------

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, x_coordinate, y_coordinate):
        super().__init__()
        self.image = pygame.image.load("res/images/space_ship.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (46, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x_coordinate
        self.rect.y = y_coordinate
        self.speed = 15
        self.lives = 5


class Ufo(pygame.sprite.Sprite):
    def __init__(self, ufo_speed):
        super().__init__()
        self.image = pygame.image.load("res/images/ufo.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 56))
        self.rect = self.image.get_rect()
     # Hilfsfunktion um Bilder zu laden
        # zufällige x-Koordinate innerhalb des Fensters
        self.rect.x = random.randint(0, screen_width - self.rect.width)

        # direkt oberhalb des Fensters starten
        self.rect.y = -self.rect.height

        self.speed = ufo_speed


####################################################################################
# Funktionsdefinitionen
# ----------------------------------------------------------------------------------

def move_players():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and space_ship.rect.y > 0:
        space_ship.rect.y -= space_ship.speed
    if keys[pygame.K_s] and space_ship.rect.y + space_ship.rect.height < screen_height:
        space_ship.rect.y += space_ship.speed
    if keys[pygame.K_a] and space_ship.rect.x > 0:
        space_ship.rect.x -= space_ship.speed
    if keys[pygame.K_d] and space_ship.rect.x + space_ship.rect.width < screen_width:
        space_ship.rect.x += space_ship.speed

    if keys[pygame.K_UP] and space_ship2.rect.y > 0:
        space_ship2.rect.y -= space_ship2.speed
    if keys[pygame.K_DOWN] and space_ship2.rect.y + space_ship2.rect.height < screen_height:
        space_ship2.rect.y += space_ship2.speed
    if keys[pygame.K_LEFT] and space_ship2.rect.x > 0:
        space_ship2.rect.x -= space_ship2.speed
    if keys[pygame.K_RIGHT] and space_ship2.rect.x + space_ship2.rect.width < screen_width:
        space_ship2.rect.x += space_ship2.speed


def move_ufos():
    for ufo in ufo_sprites:
        ufo.rect.y += ufo.speed

        # Ufo löschen, wenn es unten aus dem Fenster fliegt
        if ufo.rect.y > screen_height:
            ufo.kill()


def create_ufos(last_spawn_time):
    current_time = pygame.time.get_ticks()

    # neues Ufo nach zufälliger Zeit von 1 bis 4 Sekunden
    if current_time - last_spawn_time > 1000 + random.randint(0, 3000):
        ufo = Ufo(random.randint(2, 7))
        ufo_sprites.add(ufo)
        last_spawn_time = current_time

    return last_spawn_time


def update_danger_zone():
    global danger_zone_height

    current_time = pygame.time.get_ticks()

    # alle 2 Sekunden wächst die Zone etwas nach oben
    if current_time - danger_zone_last_growth > 2000:
        return current_time, danger_zone_height + danger_zone_growth

    return danger_zone_last_growth, danger_zone_height


def check_collisions():
    for ufo in ufo_sprites:
        if ufo.rect.colliderect(space_ship.rect):
            space_ship.lives -= 1
            ufo.kill()

        elif ufo.rect.colliderect(space_ship2.rect):
            space_ship2.lives -= 1
            ufo.kill()


def check_danger_zone_collision():
    danger_rect = pygame.Rect(0, screen_height - danger_zone_height, screen_width, danger_zone_height)

    if space_ship.rect.colliderect(danger_rect) or space_ship2.rect.colliderect(danger_rect):
        return True

    return False


def check_game_over():
    if space_ship.lives <= 0 or space_ship2.lives <= 0:
        return "game_over"

    if check_danger_zone_collision():
        return "game_over"

    return "game"


def draw_game():
    screen.blit(background_image_game, (0, 0))
    player_sprites.draw(screen)
    ufo_sprites.draw(screen)

    # Gefahrenzone zeichnen
    danger_rect = pygame.Rect(0, screen_height - danger_zone_height, screen_width, danger_zone_height)
    pygame.draw.rect(screen, (255, 0, 0), danger_rect)

    # Herzen für Spieler 1 links oben
    for i in range(space_ship.lives):
        screen.blit(heart_image, (10 + i * 35, 10))

    # Herzen für Spieler 2 rechts oben
    for i in range(space_ship2.lives):
        screen.blit(heart_image, (screen_width - 10 - (i + 1) * 35, 10))


def draw_game_over():
    screen.fill((0, 0, 0))
    screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 4))


####################################################################################
# Globale Variablen initialisieren
# ----------------------------------------------------------------------------------

# Grösse des Spielfensters setzen
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

# Schrift für Game Over
my_font = pygame.font.SysFont("Comic Sans MS", 96)
game_over_text = "Game Over"
text = my_font.render(game_over_text, True, (255, 0, 0))

# Hintergrundbild laden
background_image_game = pygame.image.load("res/images/background_game.jpg")
background_image_game = pygame.transform.scale(background_image_game, (screen_width, screen_height))

# Herzbild laden
heart_image = pygame.image.load("res/images/heart.png").convert_alpha()
heart_image = pygame.transform.scale(heart_image, (25, 22))

# Spielstatus
game_status = "game"

# Spieler erstellen
space_ship = SpaceShip(screen_width / 3, screen_height / 4 * 3)
space_ship2 = SpaceShip(screen_width / 4, screen_height / 4 * 3)

# Spieler-Gruppen
player_sprites = pygame.sprite.Group()
player_sprites.add(space_ship)
player_sprites.add(space_ship2)

# erstes Ufo erstellen
ufo = Ufo(2)

# Ufo-Gruppe
ufo_sprites = pygame.sprite.Group()
ufo_sprites.add(ufo)

# Zeitpunkt speichern, wann zuletzt ein Ufo erstellt wurde
last_spawn_time = pygame.time.get_ticks()

# Gefahrenzone
danger_zone_height = 20          # Anfangshöhe
danger_zone_growth = 10          # wächst pro Schritt um 10 Pixel
danger_zone_last_growth = pygame.time.get_ticks()

####################################################################################
# Spielschleife
# ----------------------------------------------------------------------------------

is_game_running = True

while is_game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_game_running = False

    if game_status == "game":
        move_players()
        last_spawn_time = create_ufos(last_spawn_time)
        move_ufos()
        check_collisions()

        danger_zone_last_growth, danger_zone_height = update_danger_zone()

        game_status = check_game_over()
        draw_game()

    if game_status == "game_over":
        draw_game_over()

    pygame.display.update()
    clock.tick(60)

pygame.quit()