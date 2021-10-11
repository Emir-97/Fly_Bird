import pygame, sys, random

#Se crea una función para que se ejecute la imagen del floor
def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,400))
    screen.blit(floor_surface,(floor_x_pos + 288,400))

#Se crea la función para que aparescan las tuberías
def create_pipe():
    #Se crean los pipes en alturas aleatorias
    random_pipe_pos = random.choice(pipe_height)
    #Se crean los pipes top and bottom
    bottom_pipe = pipe_surface.get_rect(midtop = (300,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (300,random_pipe_pos - 150))
    return bottom_pipe, top_pipe

#Función para el movimiento de las tuberías
def move_pipes(pipes):
    for pipe in pipes:
        #Itera a travez de la lista y las desplaza hacia la izquierda
        pipe.centerx -= 2
    return pipes

#Se dibujan las pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            #Rota the image the pipe for that top_pipe are well
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

#Se define the function for the pipe collisions with bird
def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
           death_sound.play()
           can_score = True
           return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 400:
        can_score = True
        return False

    return True

#Created the function for rotate for bird image
def rotate_bird(bird):
    #Toma tres parametros que son la imagen, el angulo de rotación en este caso sentido horario y el tamaño en scala que es 1
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

#Create the sequece and position for the bird
def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect

#The score for the application is created
def score_display(game_state):
    if game_state == 'main_game':
      #Created the text, clarity and color for the score
      score_sourface = game_font.render('Score: '+ str(int(score)), True, (255,255,255))
      #The position
      score_rect = score_sourface.get_rect(center = (144, 50))
      #is added to the app
      screen.blit(score_sourface, score_rect)

    if game_state == 'game_over':
      score_sourface = game_font.render(f'Score: {int(score)}', True, (255,255,255))
      score_rect = score_sourface.get_rect(center = (144, 50))
      screen.blit(score_sourface, score_rect)

      #High Score
      high_score_sourface = game_font.render(f'High score: {int(score)}', True, (255,255,255))
      high_score_rect = high_score_sourface.get_rect(center = (144, 380))
      screen.blit(high_score_sourface, high_score_rect)

#Function update score for score
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

#Segunda manera para el score
#def pipe_score_check():
#	global score, can_score
#
#	if pipe_list:
#		for pipe in pipe_list:
#			if 95 < pipe.centerx < 105 and can_score:
#				score += 1
#				score_sound.play()
#				can_score = False
#			if pipe.centerx < 0:
#				can_score = True

#Para reproducir los sounds sin ningún tiempo de atraso se debe
#iniciar el mixer con la frequency, size, buffer(calidad de sonido) y channels(son 2) por defecto excepto que el game lo requiera
#pygame.mixer.pre_init(frequency=44100, size=8, channels=1,  buffer=256)
pygame.init()

screen = pygame.display.set_mode((288,512))
clock = pygame.time.Clock()
#Se establece el tipo de fuente (letra y tamaño) para la app
game_font = pygame.font.SysFont('04B_19.ttf',40)

#Game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

#Se importa la imagen de fondo de la app, lo convierte para ser más facil de trabajar
bg_surface = pygame.image.load('assets/background-day.png').convert()

#Se carga la imagen para el piso
floor_surface = pygame.image.load('assets/base.png').convert()
#Se fija la posición inicial para el movimiento de la image
floor_x_pos = 0

bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
#Se almacena todas las imagenes en una lista para generar una secuencia de movimiento
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
#Se establece la imagen inicial
bird_surface = bird_frames[bird_index]
#Its position is fixed
bird_rect = bird_surface.get_rect(center = (100,266))

#Se establece el evento para el cambio de imagen y así su secuencia
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

#Se carga la imagen del bird, convert_alpha elimina el cuadrado negro que lo cubre
#bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
#bird_rect = bird_surface.get_rect(center = (100,266))

#Se carga las imagenes de las tuberías
pipe_surface = pygame.image.load('assets/pipe-green.png')
#Se crea una lista para el  almacenamiento de las tuberías
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 380, 350, 400, 300]

#image game over
game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (144,226))

#import sound's app
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            #Se realiza la funcionalidad de salto para la tecla space
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
                flap_sound.play()
            #Se establece la funcionalidad para reactivar el juego
            if event.key == pygame.K_SPACE and game_active==False:
                game_active = True
                #Se reinician the pipe and center the bird
                pipe_list.clear()
                bird_rect.center = (100, 266)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            #Cuando surja el event se crea una nueva pipe y se almacena en la lista
            pipe_list.extend(create_pipe())

        #Se establece el event para la secuencia de movimiento
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            #Cuando se llega a la última image se reinicia la secuencia
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    #Se fija la imagen de fondo de la app
    screen.blit(bg_surface,(0,0))
    if game_active:

       bird_movement += gravity
       #Fixed the bird image with rotate_bird
       rotated_bird = rotate_bird(bird_surface)
       bird_rect.centery

       #Se fija el bird
       screen.blit(rotated_bird, bird_rect)
       bird_rect.centery += bird_movement
       game_active = check_collision(pipe_list)

       #Pipes
       pipe_list = move_pipes(pipe_list)
       draw_pipes(pipe_list)

       #Se aumenta el score
       score += 0.01
       #pipe_score_check()
       score_display('main_game')
       #Se establece la reproducción del score_sound y se reinicia la reproducción cuando llega a 0 o menos
       score_sound_countdown -= 1
       if score_sound_countdown <= 0:
          score_sound.play()
          score_sound_countdown = 100
    else:
       screen.blit(game_over_surface, game_over_rect)
       high_score = update_score(score, high_score)
       score_display('game_over')

    #Se itera la imagen del floor
    floor_x_pos -= 1
    #Se establece el suelo
    draw_floor()

    #Se realiza por medio de un if la continuidad de la imagen
    #al pasar con los valores limites la posición de la imagen regrese a su estado inicial
    if floor_x_pos <= -288:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
