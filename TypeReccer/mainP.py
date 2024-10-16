import keyboard
import os
import random
import time

#text = "Hej där mitt namn är Viktor Forslund"
os.system('cls')
index = 0 

reset = '\033[0m'
green = '\033[32m'
red = '\033[31m'
underline = '\033[4m' #length: 4

def generateText():
  with open("texts.txt", 'r') as textFile:
    lines = textFile.readlines()
    randNum = random.randint(0, 9)
    text = lines[randNum].strip()  
    return text

def calculateWPM():
  wpm = (index / (elapsed_time / 6)) // 5
  print(f"WPM: {wpm}")

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

text = generateText()
text, index = underliner(text, index)
current_word = ""
print(text)
counter = 0

while True:
  current_letter = checkIndex(text, index)
  input_letter = keyboard.read_event()
  if(input_letter.event_type == keyboard.KEY_DOWN):
    input_letter = input_letter.name
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

      counter += 1
      text, index = underliner(text, index)
  elapsed_time = (time.time() - start_time) 

  if index >= len(text) and text.count(red) == 0:
    break

  if elapsed_time != 0:
    os.system('cls')
    print(text)
    print(f"\n --> {current_word}")
    calculateWPM()

calculateWPM()   

