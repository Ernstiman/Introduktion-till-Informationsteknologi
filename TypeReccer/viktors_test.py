import keyboard
import os
text = "Hej där mitt namn är Viktor Forslund"

index = 0

def checkLetter(index, text, input_letter, current_letter):
  reset = '\033[0m'
  red = '\033[31m'
  if current_letter == input_letter:
    new_letter = f'{red}{input_letter}{reset}'
    text = text.replace(current_letter, new_letter, 1)
    index += len(new_letter)
  return index, text



while True:
  print(text)
  current_letter = text[index]
  input_letter = keyboard.read_event()
  if(input_letter.event_type == keyboard.KEY_DOWN):
    input_letter = input_letter.name
    print(index)
    index, text = checkLetter(index, text, input_letter, current_letter)