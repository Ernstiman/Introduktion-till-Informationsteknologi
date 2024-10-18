import keyboard
import os
import random
import time
import threading

reset = '\033[0m'
green = '\033[32m'
red = '\033[31m'
blue = '\033[94m'
underline = '\033[4m' #length: 4

class Monkey():
  def __init__(self, monkey_skill, monkey_text, name):
    self.monkey_skill = monkey_skill
    self.monkey_counter = 0
    self.monkey_text = monkey_text
    self.monkey_lock = threading.Lock()
    self.monkey_thread = threading.Thread(target = lambda:monkeyWrite(self,self.monkey_lock, self.monkey_text, monkey_skill))
    self.name = name
    pass

  def print_progress_bar(self, total,start_time, bar_length=50,):
    monkey_wpm = 0
    progress = self.monkey_counter / total
    green_squares = int(progress * bar_length)
    red_squares = bar_length - green_squares
    green_bar = '\033[32m' + "■" * green_squares  
    red_bar = '\033[31m' + "■" * red_squares 
    monkey_elapsed_time = (time.time() - start_time)
    if monkey_elapsed_time != 0:
      monkey_wpm = ((self.monkey_counter * 10) / (monkey_elapsed_time / 6)) // 5
    print(self.name)
    print(f"\r{blue} --> | {reset} {green_bar}{red_bar}{reset} |")
    print(f"{blue}-->{reset} {monkey_wpm} WPM \n")
    
    pass

  def __str__(self):
    return (self.name)
  
  def __del__(self):
    pass



def monkeyWrite(monkey,monkey_lock, monkey_text, monkey_skill):
  with monkey_lock:
    while monkey.monkey_counter != len(monkey_text) + 1:
      time.sleep(0.005)
      randMonkeyNum = random.randint(1, monkey_skill)
      if randMonkeyNum == 1:
        monkey.monkey_counter += 1
      

def print_progress_bar(total,start_time,monkeys, bar_length=50, ):
  for monkey in monkeys:
    monkey_wpm = 0
    progress = monkey.monkey_counter / total
    green_squares = int(progress * bar_length)
    red_squares = bar_length - green_squares
    green_bar = '\033[32m' + "■" * green_squares  
    red_bar = '\033[31m' + "■" * red_squares 
    monkey_elapsed_time = (time.time() - start_time)
    if monkey_elapsed_time != 0:
      monkey_wpm = ((monkey.monkey_counter * 10) / (monkey_elapsed_time / 6)) // 5
    print(monkey)
    print(f"\r{blue} --> | {reset} {green_bar}{red_bar}{reset} |")
    print(f"{blue}-->{reset} {monkey_wpm} WPM \n")
  

def generateText():
  with open("texts.txt", 'r') as textFile:
    lines = textFile.readlines()
    randNum = random.randint(0, 0)
    text = lines[randNum].strip()  
    return text



def calculateWPM(elapsed_time, index):
  try:
    if elapsed_time > 0:
      wpm = (index / (elapsed_time / 6)) // 5
      print(f"{blue}-->{reset} {wpm} WPM \n")
    else:
      print(f"{blue}-->{reset} 0 WPM \n")
  except: 
    pass 

def underliner(text, index):
  if index < len(text):
    letter = text[index]
    new_letter = f'{underline}{letter}{reset}'
    text = text[:index] + new_letter + text[index + 1:]
    index += 4
  return text, index

def removeUnderline(text, index):
  if index < len(text):
    letter = text[index]
    text = text[:index-len(underline)] + letter + text[index + len(reset) + 1:]
    index -= len(underline)
  return text, index

def checkLetter(index, text, input_letter, current_letter = ""):
  text, index = removeUnderline(text, index)

  if input_letter == "space":
    input_letter = " "

  if input_letter == "backspace":
    if index >= len(red):
      if text[index - len(red)] == " " and text.count(red) == 0:
        pass

      else: 
        text = deleteColor(text[index - 5], text, index)
        index -= (len(red) + len(reset) + 1)

        if index < 0: index = 0

  elif index != len(text):

    if current_letter == input_letter and text.count(red) == 0:
      text, new_letter = changeColor(green, input_letter, text, index)
      index += len(new_letter)

    else:
      text, new_letter = changeColor(red, current_letter, text, index)
      index += len(new_letter)

  return index, text

def changeColor(color,input_letter, text, index):
  new_letter = f'{color}{input_letter}{reset}'
  text = text[:index] + new_letter + text[index + 1:]
  return text, new_letter

def deleteColor(input_letter, text, index):
  print(input_letter)
  text = text[:(index - (len(red) + len(reset) + 1))] + input_letter + text[index:]
  return text

def checkIndex(text, index):
  try: 
    letter = text[index]
  except:
    letter = ""
  return letter

def raceAgain():
  while True:
    ask = input("Do you want to race again? \n r) Race Again \n q) Quit\n")
    print(ask)
    if ask[len(ask) - 1] == 'r':
      return True
    elif ask[len(ask) - 1] == 'q':
      return False
    else:
      print("Enter valid input")

def splash():
    splash_length = 40
    row_1 = "MonkeyWrite"
    row_2 = "Can you type faster than a monkey?"
    row_1_space = int((splash_length - len(row_1)) / 2)
    row_2_space = int((splash_length - len(row_2)) / 2)
    print("\n" + "~" * splash_length + "\n" + " " * row_1_space + row_1 +"\n" + " " * row_2_space + row_2 + "\n" + "~" * splash_length)

def updateCurrentWord(text, index, current_word, input_letter):
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y","z", "å", "ä","ö", ",", "-", ":", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    if text.count(red) > 0:
        current_word = red + current_word
    if text.count(red) == 0 and current_word.count(red) > 0:
      current_word = current_word[(current_word.count(red) * len(red)):]
    if input_letter == "space" and text.count(red) == 0:
      current_word = ""
    if input_letter == "backspace":
      current_word = current_word[:len(current_word) - 1]
    elif index != len(text) and input_letter.lower() in letters:
      if input_letter == "space":
        current_word += " "
      else: current_word += input_letter
    return current_word

def printRace(text, current_word, start_time, index, monkeys):
  print(text)
  print("\nYou: ")
  print(f"{blue}-->{reset} {current_word}")
  elapsed_time = (time.time() - start_time)
  calculateWPM(elapsed_time, index) 
  for monkey in monkeys:
    monkey.print_progress_bar(len(monkey.monkey_text), start_time)

def printIntroScreen(text, current_word, monkeys):
  splash()
  input(f"Press{green} Enter{reset} to Start: ")
  print("\n",text)
  print("\nYou: ")
  print(f"{blue}-->{reset} {current_word}")
  print(f"{blue}-->{reset} 0 WPM \n")
  for monkey in monkeys:
    print(monkey.name)
    print(f"{blue}-->{reset}")
    print(f"{blue}-->{reset} 0 WPM \n")
    
def checkAmountOfMonkeys(amount):
  try:
    int(amount)
    return True
  except:
    print("Ange ett heltal")
    return False

def killMonkeys(monkeys):
  for monkey in monkeys:
    monkey.monkey_count = len(monkey.monkey_text) + 1

def main():
  os.system('cls')
  counter = 0
  index = 0 
  text = generateText()
  text, index = underliner(text, index)
  current_word = ""

  while True:
    amount_of_monkeys = int(input("Hur många apor vill du spela emot? --> "))
    if checkAmountOfMonkeys(amount_of_monkeys):
      monkeys = [Monkey(random.randint(15,28), text,"Monkey " + str(monkey + 1) ) for monkey in range(amount_of_monkeys)]
      break

  printIntroScreen(text, current_word, monkeys)

  while True:
    current_letter = checkIndex(text, index)
    input_letter = keyboard.read_event()

    if(input_letter.event_type == keyboard.KEY_DOWN):

      input_letter = input_letter.name

      if input_letter == "esc":
        killMonkeys(monkeys)
        
        
      if counter == 0:
        start_time = time.time()

      if input_letter != "skift" and input_letter != "right shift":
        index, text = checkLetter(index, text, input_letter, current_letter)
        current_word = updateCurrentWord(text, index, current_word, input_letter)

        if counter == 0:   
          [monkey.monkey_thread.start() for monkey in monkeys]

        os.system('cls')
        text, index = underliner(text, index)
        printRace(text, current_word, start_time, index, monkeys)
        counter += 1
        
    if index >= len(text) and text.count(red) == 0:
      for monkey in monkeys:
        if monkey.monkey_counter == len(monkey.monkey_text) + 1:
          print("Du förlora")
          break
      else:
        print("Du vann!")
      for monkey in monkeys:
          monkey.monkey_counter = len(monkey.monkey_text) + 1  
      if raceAgain():
        monkeys = []
        main()
      break

if __name__ == "__main__":
  main()