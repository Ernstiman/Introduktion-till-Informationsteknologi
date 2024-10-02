import random as rand


gameOver = False
shots = 5
shotBoard = [1, 1, 1, 1, 1]
hitChance = 50


def splash():
    splash_length = 30
    row_1 = "Biathlon"
    row_2 = "A hit or miss game"
    row_1_space = int((splash_length - len(row_1)) / 2)
    row_2_space = int((splash_length - len(row_2)) / 2)
    print("\n" + "~" * splash_length + "\n" + " " * row_1_space + row_1 +"\n" + " " * row_2_space + row_2 + "\n" + "~" * splash_length)

def showHits(list):
    for x in shotBoard:
        if x == 1:
            print("*",end=" ")
        elif x == 0:
            print("0",end = " ")
    print("\n")

def shoot(index, list):
    index -= 1
    if list[index] == 0:
        print("Hit on closed target")
    else:
        hit = rand.randint(1,2)
        if hit == 1:
            list[index] = 0
            print("Hit on closed target")
        else: print("Miss!")

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
    





    
splash()
print(f'You have {shots} shots')
while shots > 0:
    showHits(shotBoard)
    shotPos = (input(f'Shot number {6 - shots} at: '))
    if checkIndex(shotPos, shotBoard):
        shotPos = int(shotPos)
        shoot(shotPos, shotBoard)
        shots -= 1
    else: continue
    



        
