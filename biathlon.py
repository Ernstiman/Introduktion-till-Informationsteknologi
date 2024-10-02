import random

bullets = 5
board = [1, 1, 1, 1, 1]
threshold = 50
hits = 0

def splash():
    splash_length = 30
    row_1 = "Biathlon"
    row_2 = "A hit or miss game"
    row_1_space = int((splash_length - len(row_1)) / 2)
    row_2_space = int((splash_length - len(row_2)) / 2)
    print("\n" + "~" * splash_length + "\n" + " " * row_1_space + row_1 +"\n" + " " * row_2_space + row_2 + "\n" + "~" * splash_length)

def shoot(shot, threshold, hitChance): 
    
    if hitChance >= threshold:
        board[shot-1] = 0
        print("Hit!", "\n")
        threshold = threshold * 1.2

    else:
        print("Miss!", "\n")
        threshold = threshold * 0.8
        
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