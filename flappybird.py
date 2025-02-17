import pygame
import sys
import random

x = 576
y = 1024

pygame.init()
screen = pygame.display.set_mode((x, y))
time = pygame.time.Clock()

#load_screen = pygame.image.load('./src/start.png').convert()
#screen.blit(load_screen, (0,0))

"""key_press = True
while key_press:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            key_press = False
"""     

background = pygame.image.load('./src/background-day.png')
background = pygame.transform.scale2x(background)
screen.blit(background, (0, 0))

base = pygame.image.load('./src/base.png')
base = pygame.transform.scale2x(base)
screen.blit(base, (0, 900))

bird_x = x/2 - 200
bird_y = y/2

bird_midflap = pygame.image.load('./src/redbird-midflap.png')
bird_midflap = pygame.transform.scale(bird_midflap, (51, 36))

bird_downflap = pygame.image.load('./src/redbird-downflap.png')
bird_downflap = pygame.transform.scale(bird_downflap, (51,  36))

bird_upflap = pygame.image.load('./src/redbird-upflap.png')
bird_upflap = pygame.transform.scale(bird_upflap, (51, 36))

progress_x = 0
progress_y = 900

frames = [bird_downflap, bird_midflap, bird_upflap]

def collision_check(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect

def create_pipe():
	random_pipe_pos = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 300))
	return bottom_pipe,top_pipe

def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= 5
	visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
	return visible_pipes

def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= 1024:
			screen.blit(pipe_surface,pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface,False,True)
			screen.blit(flip_pipe,pipe)

def score_display(game_state):
	if game_state == 'main_game':
		score_surface = game_font.render(str(int(score)),True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)
	if game_state == 'game_over':
		score_surface = game_font.render(f'Score: {int(score)}' ,True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)

		high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
		high_score_rect = high_score_surface.get_rect(center = (288,850))
		screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score

def pipe_score_check():
	global score, can_score 
	
	if pipe_list:
		for pipe in pipe_list:
			if 95 < pipe.centerx < 105 and can_score:
				score += 1
				score_sound.play()
				can_score = False
			if pipe.centerx < 0:
				can_score = True


gravity = 0.30
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

bird_index = 0
bird_surface = frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 512))
bird_movement = 0

game_font = pygame.font.Font('04B_19.ttf', 40)

pipe_surface = pygame.image.load('./src/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list=[]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height= [400, 600, 800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('./src/message.png'))
game_over_rect = game_over_surface.get_rect(center = (288, 512))

flap_sound = pygame.mixer.Sound('./sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('./sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

score_sound_countdown = 100
SCOREEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SCOREEVENT, 100)


BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 10
                flap_sound.play()
                print("You pressed space")
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                bird_rect.center  = (100, 512)
                bird_movement = 0
                score = 0
                pipe_list.clear()
                print("You presssed space")

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    screen.blit(background, (0, 0))

    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, (100, bird_rect.centery))

        game_active = collision_check(pipe_list)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        pipe_score_check()
        score_display("main_game")
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")

    progress_x -= 1
    screen.blit(base, (progress_x, progress_y))
    screen.blit(base, (progress_x + 576, progress_y))

    if(progress_x == -576):
        progress_x = 0


    pygame.display.update()
    time.tick(120)
