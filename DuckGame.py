"""
-------------------------------------------------------------
Script Name : DuckGame.py
Author      : Mathis V.
Date Created: 26/12/2024
Last Update : 26/12/2024
Version     : v1

Description :
Jeu PyGame créé en moin de 10h 

Copyright © 2024 Mathis V.
All rights reserved. This script is the intellectual property
of the author. Unauthorized copying, modification, or distribution
of this script, via any medium, is strictly prohibited.
-------------------------------------------------------------
"""
import pygame
import sys
import random
import math


### Initialisation de Pygame

pygame.init()


### Variables Constantent

BLUE_SKY = (135, 206, 235)
WHITE = (255, 255, 255)  # Blanc
GRAY = (200, 200, 200)  # Gris clair
DARK_GRAY = (100, 100, 100)  # Gris foncé
YELLOW = (255, 223, 0)
BLACK = (0, 0, 0)

POLICE_FONT = 50
TITLE_FONT = 80
SCORE_FONT = 35

SOUNDS_PATH = "./sounds/"
IMAGES_PATH = "./images/"

HOVER_SOUND = SOUNDS_PATH + "Hover.wav"
CLICK_SOUND = SOUNDS_PATH + "Click.wav"
DIE_SOUND = SOUNDS_PATH + "Die.wav"

BIRD_1_IMAGE = IMAGES_PATH + "bird_step_1.png"
BIRD_2_IMAGE = IMAGES_PATH + "bird_step_2.png"
CLOUD_IMAGE = IMAGES_PATH + "cloud.png"
PLAYER_IMAGE = IMAGES_PATH + "joueur.png"

WINDOW_SIZE = 800
GAME_TITRE = "Envoles toi mon canard"
BIRD_MAX_SIZE_FOR_COLLISION = 60


### Variables d'initialisation

player_facing_right = True
player_speed = 100
player_pos = [WINDOW_SIZE // 2, WINDOW_SIZE // 2]

birds = []
bird_timer = 0
bird_animation_timer = 0
current_bird_image = BIRD_1_IMAGE 

clouds = []
cloud_timer = 0

play_hovered = False
quit_hovered = False
last_score = 0
best_score = 0
score = 0
in_menu = True
movement = {"up": False, "down": False, "left": False, "right": False}
running = True
second_rate = 5
createur = "Mathis V."


### Variables d'initialisation avec PyGame

bird_image1 = pygame.image.load(BIRD_1_IMAGE)
bird_image2 = pygame.image.load(BIRD_2_IMAGE)
bird_image1 = pygame.transform.scale(bird_image1, (40, 40))
bird_image2 = pygame.transform.scale(bird_image2, (40, 40))

cloud_image = pygame.image.load(CLOUD_IMAGE)  
cloud_image = pygame.transform.smoothscale(cloud_image, (50, 30))

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption(GAME_TITRE)

font = pygame.font.Font(None, POLICE_FONT)
title_font = pygame.font.Font(None, TITLE_FONT)
score_font = pygame.font.Font(None, SCORE_FONT)

play_button = pygame.Rect(300, 400, 200, 50)
quit_button = pygame.Rect(300, 500, 200, 50)

click_sound = pygame.mixer.Sound(CLICK_SOUND)
hover_sound = pygame.mixer.Sound(HOVER_SOUND)
die_sound = pygame.mixer.Sound(DIE_SOUND)

player_image_right = pygame.image.load(PLAYER_IMAGE).convert_alpha()  
player_image_right = pygame.transform.scale(player_image_right, (100, 100))
player_image_left = pygame.transform.flip(player_image_right, True, False)

clock = pygame.time.Clock()


### Les Fonctions

def draw_button(screen, button_rect, text, font, base_color, hover_color, mouse_pos):
    color = hover_color if button_rect.collidepoint(mouse_pos) else base_color
    pygame.draw.rect(screen, color, button_rect, border_radius=10)
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)

def draw_menu():
    title_text = title_font.render(GAME_TITRE, True, YELLOW)
    title_rect = title_text.get_rect(center=(WINDOW_SIZE // 2, 200))
    screen.blit(title_text, title_rect)

    last_score_text = score_font.render(f"Votre dernier score : {last_score}", True, WHITE)
    last_score_rect = last_score_text.get_rect(center=(WINDOW_SIZE // 2, 290))
    screen.blit(last_score_text, last_score_rect)

    best_score_text = score_font.render(f"Votre meilleur score : {best_score}", True, WHITE)
    best_score_rect = best_score_text.get_rect(center=(WINDOW_SIZE // 2, 320))
    screen.blit(best_score_text, best_score_rect)

    draw_button(screen, play_button, "Play", font, GRAY, DARK_GRAY, mouse_pos)
    draw_button(screen, quit_button, "Quitter", font, GRAY, DARK_GRAY, mouse_pos)

    credential_text = score_font.render(f"Creer par : {createur}", True, WHITE)
    credential_rect = credential_text.get_rect(center=(WINDOW_SIZE // 2, 750))
    screen.blit(credential_text, credential_rect)
    
def generate_cloud():
    angle = random.uniform(0, 360)  
    speed = 50  
    size = random.uniform(0, 15)
    return {"pos": [WINDOW_SIZE // 2, WINDOW_SIZE // 2], "angle": angle, "speed": speed, "size": size}

def generate_bird():
    size = 0
    angle = random.uniform(0, 360)  
    speed = random.uniform(50, 200)  
    return {"pos": [random.randint(0, WINDOW_SIZE) , random.randint(0, WINDOW_SIZE) ], "angle": angle, "speed": speed, "size": size}   

def flip_bird_image(image, angle):
    if 90 <= angle <= 270:
        return pygame.transform.flip(image, True, False) 
    return image

def reset_game():
    global birds, player_pos, movement, score, in_menu
    birds = [] 
    player_pos = [WINDOW_SIZE // 2, WINDOW_SIZE // 2] 
    movement = {"up": False, "down": False, "left": False, "right": False} 
    in_menu = True 


# Boucle principale

while running:
    #Variables
    last_score = int(score)
    dt = clock.tick(60) / 1000 
    cloud_timer += dt
    bird_timer += dt
    bird_animation_timer += dt
    if last_score > best_score : 
        best_score = int(last_score)

    # Gestion des événements
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if in_menu:  
            if play_button.collidepoint(mouse_pos):
                if not play_hovered: 
                    hover_sound.play()
                    play_hovered = True
            else:
                play_hovered = False
            if quit_button.collidepoint(mouse_pos):
                if not quit_hovered: 
                    hover_sound.play()
                    quit_hovered = True
            else:
                quit_hovered = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(mouse_pos):
                    click_sound.play()
                    score =0
                    in_menu = False 
                elif quit_button.collidepoint(mouse_pos):
                    click_sound.play()
                    running = False
        else:  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_menu = True  
                elif event.key == pygame.K_UP:
                    movement["up"] = True
                elif event.key == pygame.K_DOWN:
                    movement["down"] = True
                elif event.key == pygame.K_LEFT:
                    movement["left"] = True
                elif event.key == pygame.K_RIGHT:
                    movement["right"] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    movement["up"] = False
                elif event.key == pygame.K_DOWN:
                    movement["down"] = False
                elif event.key == pygame.K_LEFT:
                    movement["left"] = False
                elif event.key == pygame.K_RIGHT:
                    movement["right"] = False

    # Mouvement en Jeux
    if not in_menu:

        # joueur
        if movement["up"]:
            player_pos[1] -= player_speed * dt
        if movement["down"]:
            player_pos[1] += player_speed * dt
        if movement["left"]:
            player_pos[0] -= player_speed * dt
            if player_facing_right:  
                player_facing_right = False 
        if movement["right"]:
            player_pos[0] += player_speed * dt
            if not player_facing_right: 
                player_facing_right = True  

        player_pos[0] = max(0, min(WINDOW_SIZE, player_pos[0]))
        player_pos[1] = max(0, min(WINDOW_SIZE, player_pos[1]))

        # nuages
        if cloud_timer > random.uniform(4, 8):
            clouds.append(generate_cloud())
            cloud_timer = 0

        for cloud in clouds[:]:
            angle_rad = math.radians(cloud["angle"])
            cloud["pos"][0] += math.cos(angle_rad) * cloud["speed"] * dt
            cloud["pos"][1] += math.sin(angle_rad) * cloud["speed"] * dt

            cloud["size"] += cloud["speed"] * dt * 0.1

            if (
                cloud["pos"][0] < 0 - cloud["size"]
                or cloud["pos"][0] > WINDOW_SIZE + cloud["size"]
                or cloud["pos"][1] < 0 - cloud["size"]
                or cloud["pos"][1] > WINDOW_SIZE + cloud["size"]
            ):
                clouds.remove(cloud)

        # oiseaux
        if bird_timer > random.uniform(1, second_rate):
            birds.append(generate_bird())
            bird_timer = 0

        if score >= 20:
            second_rate =3
        if score >= 40:
            second_rate =1
        if score >= 60:
            second_rate =0

        for bird in birds[:]:
            angle_rad = math.radians(bird["angle"])
            bird["pos"][0] += math.cos(angle_rad) * bird["speed"] * dt
            bird["pos"][1] += math.sin(angle_rad) * bird["speed"] * dt

            bird["size"] += bird["speed"] * dt * 0.2

            if bird["size"] >= BIRD_MAX_SIZE_FOR_COLLISION:
                player_rect = pygame.Rect(player_pos[0] - 5, player_pos[1] - 5, 10, 10)
                bird_rect = pygame.Rect(bird["pos"][0] - bird["size"] // 2, bird["pos"][1] - bird["size"] // 2, bird["size"], bird["size"])
                if player_rect.colliderect(bird_rect):
                    die_sound.play()
                    reset_game()

            if (
                bird["pos"][0] < -50
                or bird["pos"][0] > WINDOW_SIZE + 50
                or bird["pos"][1] < -50
                or bird["pos"][1] > WINDOW_SIZE + 50
            ):
                birds.remove(bird)

        if bird_animation_timer > 0.2:  # Alterne les images toutes les 0.2 secondes
            current_bird_image = bird_image1 if current_bird_image == bird_image2 else bird_image2
            bird_animation_timer = 0

        # score
        score += 1 * dt


    # mise à jour de l'écran
    screen.fill(BLUE_SKY)
    if in_menu:
        # Affichage du menu
        draw_menu()  
    else:  
        # Afficher les nuages
        for cloud in clouds:
            resized_cloud = pygame.transform.smoothscale(cloud_image, (int(cloud["size"]), int(cloud["size"] * 0.6)))
            screen.blit(resized_cloud, (cloud["pos"][0] - cloud["size"] // 2, cloud["pos"][1] - cloud["size"] // 2))
            
        # Afficher les oiseaux 
        for bird in birds:
            resized_bird = pygame.transform.smoothscale(current_bird_image, (int(bird["size"]), int(bird["size"])))
            flipped_bird = flip_bird_image(resized_bird, bird["angle"])
            screen.blit(flipped_bird, (bird["pos"][0] - bird["size"] // 2, bird["pos"][1] - bird["size"] // 2))

        # Afficher le joueur 
        if player_facing_right:
            screen.blit(player_image_right, (player_pos[0] - 50, player_pos[1] - 50))
        else:
            screen.blit(player_image_left, (player_pos[0] - 50, player_pos[1] - 50))

        # Afficher le score
        score_text = score_font.render(f"Score : {int(score)}", True, YELLOW)
        screen.blit(score_text, (WINDOW_SIZE - 150, 10))  # En haut à droite


    # Mettre à jour l'écran   
    pygame.display.flip() 
    

# Fin
pygame.quit()
sys.exit()