import keyboard
import os
text = "Hej där mitt namn är Viktor Forslund"

index = 0
print(text)

def checkLetter(index, text, input_letter, current_letter):
  reset = '\033[0m'
  green = '\033[32m'
  red = '\033[31m'
  if input_letter == "space":
    input_letter = " "
  elif input_letter == "backspace":
    text, new_letter = changeColor(reset, reset,input_letter, text, index)
    index -= len(new_letter)

  elif current_letter == input_letter:
    text, new_letter = changeColor(green, reset,input_letter, text, index)
    index += len(new_letter)
  elif current_letter != input_letter:
    text, new_letter = changeColor(red, reset,input_letter, text, index)
    index += len(new_letter)

  return index, text

def changeColor(color,base_color,input_letter, text, index):
  new_letter = f'{color}{input_letter}{base_color}'
  text = text[:index] + new_letter + text[index + 1:]
  return text, new_letter



while True:
  
  current_letter = text[index]
  input_letter = keyboard.read_event()
  if(input_letter.event_type == keyboard.KEY_DOWN):
    input_letter = input_letter.name
    index, text = checkLetter(index, text, input_letter, current_letter)
    if input_letter != "skift":
      os.system('cls')
      print(text)