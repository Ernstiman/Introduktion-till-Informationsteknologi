
import random

# ------------ Colors ------------ #
red = '\033[31m'
blue = '\033[34m'
magenta = '\033[35m'
green = '\033[92m'
reset = '\033[39m'

# ------------ Player Class ------------ #
class Player:

# ------------ Player values ------------ #
    def __init__(self, name):
        self.name = name
        self.bullets = 5
        self.hits = 0
        self.board = [1, 1, 1, 1, 1]
        self.fatigue = 50

# ------------ Player shoot ------------ #
    def shoot(self): 
        hitChance = random.randint(1, 101)
        while True:

            shot = input(f"{self.name}, shoot at target (1-5) ")
            try:
                shot = int(shot)
            except ValueError:
                print("Enter int from 1, 5")
                continue

            if 1 <= shot <= 5: 
                break
            else: 
                print("Enter int from 1, 5")

        if hitChance >= self.fatigue:  
            if self.board[shot-1] == 0:
                print(f"!!! {blue}{self.name}{reset} hit {red}closed{reset} target !!!", "\n")
            else:
                self.board[shot-1] = 0
                print(f"!!! {blue}{self.name}{reset} hit {green}open{reset} target !!!", "\n")
                self.fatigue *= 1.2

        else:
            print("Miss", "\n")
            self.fatigue *= 0.8
        self.bullets -= 1
        return self.fatigue

# ------------ Print Board ------------ #
    def showHits(self):
        print("1 2 3 4 5")
        for _ in self.board:
            if _ == 1:
                print('*', end=" ")
            elif _ == 0:
                print(f"{red}O{reset}", end=" ")
        print("\n")
      
       

 
