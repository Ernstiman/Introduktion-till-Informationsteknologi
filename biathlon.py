<<<<<<< HEAD
import random

bullets = 5
board = [1, 1, 1, 1, 1]
threshold = 50
hits = 0
=======
import random as rand

>>>>>>> 68b42d4eac935688010af338cb1ad029d90e3981


class Player:
    def __init__(self, name = ""):
        self.name = name
        self.shotBoard = [1, 1, 1, 1, 1]
        self.shots = 0
        self.threshold = 50
    
    def shoot(self, index):
        index -= 1
        if self.shotBoard[index] == 0:
            print("Hit on closed target")
        else:
            hit = rand.randint(1,100)
            if hit > self.threshold:
                self.shotBoard[index] = 0
                print("Hit!")
                self.threshold += 10
            else: 
                print("Miss!")
                self.threshold -= 5

    def showHits(self):
        print(f'{self.name}:', end = " ")
        for x in self.shotBoard:
            if x == 1:
                print("*",end=" ")
            elif x == 0:
                print("0",end = " ")
        print("\n")
        print(f'Hit chance: {int(100 - self.threshold)}% \n')

    
    
def splash():
    splash_length = 30
    row_1 = "Biathlon"
    row_2 = "A hit or miss game"
    row_1_space = int((splash_length - len(row_1)) / 2)
    row_2_space = int((splash_length - len(row_2)) / 2)
    print("\n" + "~" * splash_length + "\n" + " " * row_1_space + row_1 +"\n" + " " * row_2_space + row_2 + "\n" + "~" * splash_length)

<<<<<<< HEAD
def shoot(shot, threshold, hitChance): 
    
    if hitChance >= threshold:
        board[shot-1] = 0
        print("Hit!", "\n")
        threshold = threshold * 1.2

    else:
        print("Miss!", "\n")
        threshold = threshold * 0.8
=======


def checkIndex(index, list):
    try:
        list[int(index) - 1]
        return True
    except:
        print("Du måste ange ett tal mellan 1 och 5!!!")
        return False
    
def checkWin(list):
    counter = 0
    for x in list:
        if x != 0:
            counter += 1
    if counter == 0:
        return True

def changePlayer(player, player1, player2):
    if player == player1:
        return player2
    return player1

    
def main():
    splash()
    gameOver = False
    rounds = 10
    player1_name = str(input("Ange namn för spelare 1 -->"))
    player2_name = str(input("Ange namn för spelare 2 -->"))
    player1 = Player(player1_name)
    player2 = Player(player2_name)
    activePlayer = player1
    while player2.shots != rounds:
        print("")
        activePlayer.showHits()
        shotPos = (input(f'{activePlayer.name}: Shot number {activePlayer.shots} at: '))
        if checkIndex(shotPos, activePlayer.shotBoard):
            shotPos = int(shotPos)
            activePlayer.shoot(shotPos)
            activePlayer.shots += 1
            if checkWin(activePlayer.shotBoard):
                print(f'{activePlayer.name} vann!!!')
                gameOver = True
                break
            activePlayer = changePlayer(activePlayer, player1, player2)
        else: continue
    
    if not gameOver:
        if player1.shotBoard.count(0) > player2.shotBoard.count(0):
            print(f'{player1.name} vann!')
        else: 
            print(f'{player2.name} vann!')
    while True:
        svar = str(input("Vill du spela igen(y/n) -->"))
        if svar == "y":
            main()
        elif svar == "n":
            break
        

main()

>>>>>>> 68b42d4eac935688010af338cb1ad029d90e3981
        
    return threshold

def showHits(board):
    for x in board:
        if x == 1:
            print('*', end=" ")
        elif x == 0:
            print('O', end=" ")
    print("\n")

splash()
showHits(board)

while bullets != 0:
   
    hitChance = random.randint(1, 101)
    # print(f"Threshold: {threshold}%")
    # print(f"Hit Chance: {hitChance}%")
    if bullets == 1: print(f"You got {bullets} bullet")
    else: print(f"You got {bullets} bullets") 

    while True:
        shot = input("Shoot at ")
        try:
            shot = int(shot)

        except ValueError:
            print("Enter int from 1, 5")
            continue

        if 1 <= shot <= 5: break
        else: print("Enter int from 1, 5")

    threshold = shoot(shot, threshold, hitChance)
    showHits(board)
    
    bullets -= 1

for hit in board:
    if board[hit] == 0:
        hits += 1

print(f"Game Over! {hits}/5 hits!")