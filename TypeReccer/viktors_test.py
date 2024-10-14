import keyboard
import os
text = "Hej där mitt namn är Viktor Forslund"
print(text)

index = 0

def checkLetter(index, text, input_letter, current_letter = ""):
  reset = '\033[0m'
  green = '\033[32m'
  red = '\033[31m'
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
while True:
  
  current_letter = checkIndex(text, index)
  input_letter = keyboard.read_event()
  if(input_letter.event_type == keyboard.KEY_DOWN):
    input_letter = input_letter.name
    if input_letter != "skift":
      index, text, red = checkLetter(index, text, input_letter, current_letter)
      os.system('cls')
      print(text)
  if index >= len(text) and text.count(red) == 0:
    break