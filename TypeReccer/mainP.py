import keyboard
import os
import random
import time
import threading

#text = "Hej där mitt namn är Viktor Forslund"
os.system('cls')
index = 0 

reset = '\033[0m'
green = '\033[32m'
red = '\033[31m'
blue = '\033[94m'
underline = '\033[4m' #length: 4


counter = 0

monkey_lock = threading.Lock()
monkey_counter = 0
monkey_skill = random.randint(15, 28)
monkey_wpm = 0

def monkey():
  global monkey_counter
  with monkey_lock:
    while monkey_counter != len(monkey_text) + 1:
      time.sleep(0.005)
      randMonkeyNum = random.randint(1, monkey_skill)
      if randMonkeyNum == 1:
        monkey_counter += 1
      

def print_progress_bar(current, total, bar_length=50):
  final_monkey_wpm = 0
  progress = current / total
  green_squares = int(progress * bar_length)
  red_squares = bar_length - green_squares
  green_bar = '\033[32m' + "■" * green_squares  
  red_bar = '\033[31m' + "■" * red_squares 
  monkey_elapsed_time = (time.time() - start_time)

  monkey_wpm = ((monkey_counter * 10) / (monkey_elapsed_time / 6)) // 5
  print("Monkey:")
  print(f"\r{blue} --> | {reset} {green_bar}{red_bar}{reset} |")
  print(f"{blue}-->{reset} {monkey_wpm} WPM \n")
  

def generateText():
  with open("texts.txt", 'r') as textFile:
    lines = textFile.readlines()
    randNum = random.randint(0, 9)
    text = lines[randNum].strip()  
    return text



def calculateWPM():
  if elapsed_time > 0:
    wpm = (index / (elapsed_time / 6)) // 5
    print(f"{blue}-->{reset} {wpm} WPM \n")
  else:
    print(f"{blue}-->{reset} 0 WPM \n") 

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
    text = text[:index-4] + letter + text[index + 5:]
    index -= 4
  return text, index

def checkLetter(index, text, input_letter, current_letter = ""):
  text, index = removeUnderline(text, index)
  if input_letter == "space":
    input_letter = " "
  if input_letter == "backspace":
    if text[index - 5] == " " and text.count(red) == 0:
      pass
    else: 
      text = deleteColor(text[index - 5], text, index)
      index -= 10

  elif current_letter == input_letter and text.count(red) == 0 and current_letter != "":
    text, new_letter = changeColor(green, reset,input_letter, text, index)
    index += len(new_letter)
  elif (current_letter != input_letter or text.count(red) > 0) and current_letter != "":
    text, new_letter = changeColor(red, reset,current_letter, text, index)
    index += len(new_letter)
  return index, text, red

def changeColor(color,base_color,input_letter, text, index):
  new_letter = f'{color}{input_letter}{base_color}'
  text = text[:index] + new_letter + text[index + 1:]
  return text, new_letter

def deleteColor(input_letter, text, index):
  text = text[:(index - 10)] + input_letter + text[index:]
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
    if ask == 'r':
      return True
    elif ask == 'q':
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


text = generateText()
monkey_text = text
text, index = underliner(text, index)
current_word = ""


splash()
input(f"Press{green} Enter{reset} to Start: ")
print("\n",text)
print("\nYou: ")
print(f"{blue}-->{reset} {current_word}")
print(f"{blue}-->{reset} 0 WPM \n")
print("Monkey: ")
print(f"{blue}-->{reset}")
print(f"{blue}-->{reset} 0 WPM \n")

while True:
  current_letter = checkIndex(text, index)
  input_letter = keyboard.read_event()

  if(input_letter.event_type == keyboard.KEY_DOWN):

    input_letter = input_letter.name
    monkey_thread = threading.Thread(target=monkey)  ##################
    monkey_thread.start()

    if input_letter == "esc":
      monkey_counter = len(monkey_text)
      break
      
    if counter == 0:
      start_time = time.time()
    
    if input_letter != "skift":
      index, text, red = checkLetter(index, text, input_letter, current_letter)
      if text.count(red) > 0:
          current_word = red + current_word
      if text.count(red) == 0 and current_word.count(red) > 0:
        current_word = current_word[(current_word.count(red) * 5):]
      if input_letter == "space" and text.count(red) == 0:
        current_word = ""
      if input_letter == "backspace" and index != 0:
        current_word = current_word[:len(current_word) - 1]
      else:
        if input_letter == "space":
          current_word += " "
        else: current_word += input_letter

      os.system('cls')
      print(text)
      print("\nYou: ")
      print(f"{blue}-->{reset} {current_word}")
      calculateWPM()  
      print_progress_bar(monkey_counter, len(monkey_text))
      counter += 1
      text, index = underliner(text, index)


  elapsed_time = (time.time() - start_time)
  if index >= len(text) and text.count(red) == 0:
    break

  

print(reset)
print("done")