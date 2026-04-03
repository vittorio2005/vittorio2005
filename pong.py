import pygame
import random

pygame.init()

# SUONI
suono_muro = pygame.mixer.Sound("muro.wav")
suono_racchetta = pygame.mixer.Sound("racchetta.wav")
suono_punteggio = pygame.mixer.Sound("punteggio.wav")
# --- Costanti ---
WIDTH, HEIGHT = 800, 600
FPS = 60

# --- Schermo e clock ---
schermo = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# --- Colore ---
colore = (255, 255, 255)

# --- Racchette ---
y1 = 250.0  # sinistra
y2 = 250.0  # destra
velocita_racchetta = 8
racchetta_larghezza = 20
racchetta_altezza = 80

# --- Palla ---
diametro_palla = 18
Px = WIDTH / 2
Py = HEIGHT / 2
Vx = 8
Vy = 8

# --- Punteggio ---
score1 = 0
score2 = 0

# --- Funzione reset palla ---
def reset_palla():

    global Px, Py, Vx, Vy
    Px = WIDTH / 2
    Py = HEIGHT / 2 
    Vx = random.choice([-8, 8])
    Vy = random.choice([-8, 8])

# --- Loop principale ---
running = True
while running:
    clock.tick(FPS)  # limita il loop a 60 FPS

    # --- Gestione eventi ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Movimento racchette ---
    tasti = pygame.key.get_pressed()
    if tasti[pygame.K_w]:
        y1 -= velocita_racchetta
    if tasti[pygame.K_s]:
        y1 += velocita_racchetta
    if tasti[pygame.K_UP]:
        y2 -= velocita_racchetta
    if tasti[pygame.K_DOWN]:
        y2 += velocita_racchetta

    # --- Limite racchette dentro lo schermo ---
    y1 = max(0, min(y1, HEIGHT - racchetta_altezza))
    y2 = max(0, min(y2, HEIGHT - racchetta_altezza))

    # --- Movimento palla ---
    Px += Vx
    Py += Vy

    # --- Rimbalzo sopra/sotto ---
    if Py <= 0 or Py >= HEIGHT - diametro_palla:
        Vy *= -1
        suono_muro.play()

    # --- Collisione con racchette ---
    if Px <= 20 + racchetta_larghezza and y1 <= Py <= y1 + racchetta_altezza:
        Vx *= -1
        Vx += 1
        Vy += 1
        suono_racchetta.play()

    if Px + diametro_palla >= 770 and y2 <= Py <= y2 + racchetta_altezza:
        Vx *= -1
        Vx += 1
        Vy += 1
        suono_racchetta.play()

    # --- Controllo punteggio e reset ---
    if Px < 0:  # palla oltre la racchetta sinistra
        score2 += 1
        reset_palla()
        suono_punteggio.play()

    if Px > WIDTH:  # palla oltre la racchetta destra
        score1 += 1
        reset_palla()
        suono_punteggio.play()

    # --- Disegni ---
    schermo.fill((0, 0, 0))
    pygame.draw.rect(schermo, colore, (20, int(y1), racchetta_larghezza, racchetta_altezza))
    pygame.draw.rect(schermo, colore, (WIDTH - 40, int(y2), racchetta_larghezza, racchetta_altezza))
    pygame.draw.circle(schermo, colore, (int(Px), int(Py)), diametro_palla // 2)

    # --- Visualizzazione Punteggio ---
    font = pygame.font.Font(None, 50)
    text = font.render(f"{score1} : {score2}", True, colore)
    schermo.blit(text, (WIDTH//2 - 50, 20))

    # --- Aggiornamento display ---
    pygame.display.update()

pygame.quit()