import pygame,random

BLANCO = (255, 255, 255)

class Roca(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("rocas.png").convert()  
        self.image.set_colorkey(BLANCO)
        self.rect = self.image.get_rect()

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("goku.png").convert()  
        self.image.set_colorkey(BLANCO)
        self.rect = self.image.get_rect()
        self.velocidad_en_x = 0
        self.velocidad_en_y = 0

    def cambio_velocidad(self, x):
        self.velocidad_en_x += x

    def update(self):
        self.rect.x += self.velocidad_en_x
        jugador.rect.y = 510

class Blast(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("disparo.png").convert()  
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 4

def mostrar_menu():
    screen.fill([255, 255, 255])
    font = pygame.font.Font(None, 36)

    title_text = font.render("Presiona 'S' para comenzar", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

    instructions_text = font.render("Presiona 'Q' para salir", True, (0, 0, 0))
    instructions_rect = instructions_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    screen.blit(title_text, title_rect)
    screen.blit(instructions_text, instructions_rect)

    pygame.display.flip()

    esperando_input = True
    while esperando_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    esperando_input = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def cargar_imagenes():
    # Carga de imágenes
    imagen_roca = pygame.image.load("rocas.png").convert()
    imagen_roca.set_colorkey(BLANCO)

    imagen_jugador = pygame.image.load("goku.png").convert()
    imagen_jugador.set_colorkey(BLANCO)

    imagen_blast = pygame.image.load("disparo.png").convert()
    return imagen_roca, imagen_jugador, imagen_blast

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

# Configuración de la pantalla
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Entrenamiento")

# Reloj para controlar la velocidad de actualización
clock = pygame.time.Clock()

# Banderas y variables del juego
terminado = False
puntos = 0

# Grupos de sprites
piedra_list = pygame.sprite.Group()
all_sprite_list = pygame.sprite.Group()
blast_list = pygame.sprite.Group()

# Carga de imágenes
imagen_roca, imagen_jugador, imagen_blast = cargar_imagenes()

# Creación de rocas
for i in range(10):
    roca = Roca()
    imagen_roca = imagen_roca
    roca.rect.x = random.randrange(SCREEN_WIDTH - 20)
    roca.rect.y = random.randrange(100, 300)
    piedra_list.add(roca)
    all_sprite_list.add(roca)

# Creación del jugador
jugador = Jugador()
imagen_jugador = imagen_jugador
all_sprite_list.add(jugador)

# Texto de juego finalizado
font = pygame.font.Font(None, 36)  
game_over_text = font.render("Juego finalizado", True, BLANCO)
game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

# Mostrar menú antes de iniciar el juego
mostrar_menu()

# Bucle principal del juego
while not terminado:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminado = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                jugador.cambio_velocidad(-3)
            if event.key == pygame.K_RIGHT:
                jugador.cambio_velocidad(3)
            if event.key == pygame.K_SPACE:
                blast = Blast()
                imagen_blast = imagen_blast
                blast.rect.x = jugador.rect.x + 45
                blast.rect.y = jugador.rect.y - 20
                blast_list.add(blast)
                all_sprite_list.add(blast)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                jugador.cambio_velocidad(3)
            if event.key == pygame.K_RIGHT:
                jugador.cambio_velocidad(-3)

    all_sprite_list.update()

    for blast in blast_list:
        piedra_hit_list = pygame.sprite.spritecollide(blast, piedra_list, True)
        for piedra in piedra_hit_list:
            all_sprite_list.remove(blast)
            blast_list.remove(blast)
            puntos += 1
            print(puntos)
        if blast.rect.y < -10:
            all_sprite_list.remove(blast)
            blast_list.remove(blast)

    screen.fill([255, 255, 255])
    all_sprite_list.draw(screen)

    if not piedra_list:
        screen.blit(game_over_text, game_over_rect)
        terminado = True

    pygame.display.flip()
    clock.tick(60)

# Salir del juego
pygame.quit()