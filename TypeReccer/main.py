import keyboard
import os
import random
import time

#text = "Hej där mitt namn är Viktor Forslund"
index = 0 
startTime = time.time()


def generateText():
  with open("texts.txt", 'r') as textFile:
    lines = textFile.readlines()
    randNum = random.randint(0, 9)
    text = lines[randNum].strip()  
    return text

def timeStart():
  startTime 
  return startTime 
    
def timeStop():
  endTime = time.time() - startTime
  print(startTime)
  print(f"Elapsed time: {startTime:.2f} seconds")
  return (time.time() - startTime)

def calculateWPM():
  wordCount = text.count(" ") + 1
  print(elapsed_time)
  wpm = wordCount // elapsed_time
  print(f"WordCount: {wordCount}")
  print(f"elapsed_time {elapsed_time}")
  print(f"WPM: {wpm}")
  print(wordCount)
  


def checkLetter(index, text, input_letter, current_letter):
  reset = '\033[0m'
  red = '\033[31m'
  
  if input_letter == "space":
    input_letter = " "
  if current_letter == input_letter:
    new_letter = f'{red}{input_letter}{reset}'
    text = text[:index] + new_letter + text[index + 1:]
    index += len(new_letter)
  return index, text

text = generateText()
start_time = time.time()
while True:
  current_letter = text[index]
  input_letter = keyboard.read_event()
  if(input_letter.event_type == keyboard.KEY_DOWN):
    input_letter = input_letter.name
    index, text = checkLetter(index, text, input_letter, current_letter)
    os.system('cls')
    print(text)
  if index >= len(text):
    break

elapsed_time = (time.time() - start_time) // 60
# endTime = timeStop()
calculateWPM()