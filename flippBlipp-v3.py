
def flippBlipp(n):
    result = ""
    if n%15 == 0:
        result = "flippblipp"
    elif n%5 == 0:
        result = "blipp"
    elif n%3 == 0:
        result = "flipp"
    else: return str(n)
    return result        
counter = 0
while True:
    counter += 1
    answer = input("Nästa: ")
    if answer == flippBlipp(counter):
        continue
    else:
        print(f'Fel - {flippBlipp(counter)}')
        print("Game Over")
        break
    
        
            