import keyboard
import os
text = "Hej där mitt namn är Viktor Forslund"

index = 0

def checkLetter(e, input_letter, current_letter):
  global text, index
  reset = '\033[0m'
  red = '\033[31m'
  if current_letter == input_letter:
    new_letter = f'{red}{input_letter}{reset}'
    text = text.replace(current_letter, new_letter, 1)
    index += 1



while True:
  print(text)
  current_letter = text[index]
  input_letter = keyboard.read_event()
  if(input_letter.event_type == keyboard.KEY_DOWN):
    input_letter = input_letter.name
    print(index)
  
    keyboard.on_press(lambda e: checkLetter(e,input_letter, current_letter))