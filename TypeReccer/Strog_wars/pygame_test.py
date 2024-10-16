import pygame
from sys import exit

pygame.init()

clock = pygame.time.Clock()
canvas = pygame.display.set_mode((800, 800))
bg  = pygame.Surface((800,800))
bg.fill('black')
rect = pygame.image.load("strog.jpg")
rect = pygame.transform.scale(rect, (100, 100))
rect2 = pygame.image.load("strog.jpg")
rect2 = pygame.transform.scale(rect2, (100, 100))
game_active = True
x_kord = 100
y_kord = 100
x_kord2 = 100
y_kord2 = 100
while game_active:
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.type == pygame.QUIT:
        game_active = False
      if event.key == pygame.K_d:
        x_kord += 40
      if event.key == pygame.K_a:
        x_kord -= 40
      if event.key == pygame.K_w:
        y_kord -= 40
      if event.key == pygame.K_s:
        y_kord += 40
      if event.key == pygame.K_RIGHT:
        x_kord2 += 40
      if event.key == pygame.K_LEFT:
        x_kord2 -= 40
      if event.key == pygame.K_UP:
        y_kord2 -= 40
      if event.key == pygame.K_DOWN:
        y_kord2 += 40
  if x_kord > canvas.get_width():
    x_kord = 0 - rect.get_width()

  if x_kord < 0 - rect.get_width():
    x_kord = canvas.get_width()

  if y_kord > canvas.get_height():
    y_kord = 0 - rect.get_height()

  if y_kord < 0 - rect.get_height():
    y_kord = canvas.get_height()
  canvas.blit(bg, (0,0))
  canvas.blit(rect, (x_kord, y_kord))
  canvas.blit(rect2, ((x_kord2 + 200), (y_kord2 + 200)))
  pygame.display.update()
  clock.tick(60)

pygame.quit()

