
from players import *
import time
import os


# ------------ Globala Variabler ------------ #
players = []
scores = []

# ------------ Title Screen ------------ #
def splash():
    splash_length = 30
    row_1 = "Biathlon"
    row_2 = "A hit or miss game"
    row_1_space = int((splash_length - len(row_1)) / 2)
    row_2_space = int((splash_length - len(row_2)) / 2)
    print("\n" + "~" * splash_length + "\n" + " " * row_1_space + row_1 +"\n" + " " * row_2_space + row_2 + "\n" + "~" * splash_length)

# ------------ Player Creation ------------ #
def playerSelection():
    while True:
        try:
            player_num = int(input("How many players? "))
            break

        except ValueError:
            os.system("cls")
            splash()
            print("!!! Enter an integer !!!")
            continue

    print("\n")
    for i in range(1, player_num + 1):
        username = input(f"Enter name for Player {i}: ").upper()
        players.append(Player(name = username))


# ------------ Game Start ------------ #
if __name__ == '__main__':
    splash()
    playerSelection()
    
    # ------------ Main Game Loop ------------ #
    game_over = False
    while not game_over:
        for player in players:
            
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(f"{blue}Name:{reset} {player.name} | {red}Bullets:{reset} {player.bullets} | {magenta}Fatigue:{reset} {format(player.fatigue, '.1f')}%")
            player.showHits(player.board)
            if player.bullets != 0:
                player.fatigue = player.shoot(player.fatigue)  
                time.sleep(0.5)
                player.hits = player.showHits(player.board)
                time.sleep(0.5)

        # ------------ Game Over ------------ #
        game_over = all(player.bullets == 0 for player in players)   


    print("Game Over!")
    for player in players:
        print(player.hits)
        for _ in player.board:
            if player.board[_] == 0:
                player.hits += 1
           

    print(f"name: {player.name} | {player.hits} hits | {player.board}")

