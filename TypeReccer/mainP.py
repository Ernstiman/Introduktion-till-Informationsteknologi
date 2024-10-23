import keyboard
import os
import random
import time
import threading
import matplotlib.pyplot as plt

# TEXT STYLES
reset = '\033[0m'
underline = '\033[4m' #length: 4
bold = "\033[1m"

# TEXT COLORS
black = "\033[30m"
yellow = "\033[33m"
magenta = "\033[35m"
cyan = "\033[36m"
green = '\033[32m'
red = '\033[31m'
untouched_red = '\033[31m'
blue = "\033[34m"
white = "\033[37m"

# BACKGROUD COLORS
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

kill_monkey = False
# ---------------------------------------------------- MONKEY CLASS
class Monkey():
  def __init__(self, monkey_skill, monkey_text, name):

    def monkeyNames(name):
      with open('monkey_names.txt', 'r', encoding = 'utf-8') as nameFile:
        lines = nameFile.readlines()
        randNum = random.randint(0, len(lines) - 1)
        name = lines[randNum].strip()  
        return name

    self.monkey_skill = monkey_skill
    self.monkey_counter = 0
    self.monkey_text = monkey_text
    self.monkey_lock = threading.Lock()
    self.monkey_thread = threading.Thread(target = lambda:monkeyWrite(self,self.monkey_lock, self.monkey_text, monkey_skill))
    self.name = monkeyNames(name)
    self.final_monkey_wpm = 0


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
      
    if red_squares == 0:
      print(self.name)
      print(f"\r{blue}--> {reset} [{green_bar}{red_bar}{reset}]")
      print(f"{blue}-->{reset} {self.final_monkey_wpm} WPM \n")
    else:
      print(self.name)
      print(f"\r{blue}--> {reset} [{green_bar}{red_bar}{reset}]")
      print(f"{blue}-->{reset} {monkey_wpm} WPM \n")


  def __str__(self):
    return (self.name)
  
  def __del__(self):
    pass

# ---------------------------------------------------- MONKEY FUNCTIONS


def difficultySelection(monkey_skill):
  while True:
    try:
      difficulty = int(input(f"{bold}Enter Game Difficulty:{reset}\n1){green} Easy{reset}\n2){blue} Medium{reset}\n3){untouched_red} Hard{reset}\n4) {BG_RED}{bold}{white}!!!MONKEY DEATH!!!{reset}\n5) Quit\nOption: "))
      if difficulty == 1:
        monkey_skill = random.randint(30, 40)
        print(f"\nYou Selected{green} Easy!{reset}")
        break
      elif difficulty == 2:
        monkey_skill = random.randint(20, 30)
        print(f"\nYou Selected{blue} Medium!{reset}")
        break
      elif difficulty == 3:
        monkey_skill = random.randint(5, 15)
        print(f"\nYou Selected{untouched_red} Hard!{reset}")
        break
      elif difficulty == 4:
        monkey_skill = random.randint(2, 10)
        print(f"\n{BG_RED}{bold}{white}You Selected MONKEY DEATH!!!{reset}")
        break
      elif difficulty == 5:
        os.system('cls')
        exit()
      else:
        inputError()
    except ValueError:
      inputError()
  return monkey_skill

def inputError():
  os.system('cls')
  splash()
  print(f"{BG_YELLOW}{black}!! ERROR: ENTER VALID INPUT !!{reset}")

def monkeyWrite(monkey,monkey_lock, monkey_text, monkey_skill):

  start_time = time.time()
  with monkey_lock:
    while (monkey.monkey_counter != len(monkey_text) + 1 and not kill_monkey):
      time.sleep(0.005)
      randMonkeyNum = random.randint(1, monkey_skill)
      if randMonkeyNum == 1:
        monkey.monkey_counter += 1
      
  elapsed_time = time.time() - start_time
  if elapsed_time > 0:
    monkey.final_monkey_wpm = (monkey.monkey_counter / (elapsed_time / 60)) // 5

def checkAmountOfMonkeys(amount):
  if amount > 0:
    return True
  else: 
    return False

def killMonkeys(monkeys):
  for monkey in monkeys:
    monkey.monkey_count = len(monkey.monkey_text) + 1

# ---------------------------------------------------- TEXT AND STRING FUNCTIONS
def generateText():
  with open("texts.txt", 'r', encoding='utf-8') as textFile:
    lines = textFile.readlines()
    randNum = random.randint(0, len(lines)-1)
    text = lines[randNum].strip()  
    return text

def print_graph(wpms):
  wpms.pop(0)
  wpms.pop(0)
  avrg_amount = len(wpms) // 8
  start_index = 0
  count = 0
  avr_list = []
  for x in range(8):
    count = 0
    sum = 0
    for x in range(start_index, start_index + avrg_amount):
      count += 1
      sum += wpms[x]
    avr = int(sum/count)
    avr_list.append(avr)
    start_index += avrg_amount
    
  x_axis = [x + 1 for x in range(8)]
  plt.bar(x_axis, avr_list)
  plt.ylim([0, max(avr_list) + 20])
  plt.xlabel("Segment")
  plt.ylabel("WPM")
  plt.show()


  pass
def calculateWPM(elapsed_time, index, wpms):
  try:
    if elapsed_time > 0:
      wpm = int((index / (elapsed_time / 60)) / 5)
      wpms.append(wpm)
      print(f"{blue}-->{reset} {wpm} WPM \n")
      return wpm, wpms
    else:
      print(f"{blue}-->{reset} 0 WPM \n")
      return 0, wpms
  except: 
    return wpm, wpms
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


# ---------------------------------------------------- UI FUNCTIONS
def raceAgain(wpms):
  while True:
    ask = input(f"\n{bold} Do you want to race again or see race data?{reset} \n r){green} Race Again{reset} \n s){yellow} See race data{reset}\n q){untouched_red} Quit\n{reset}")
    print(ask)
    ask = " " + ask
    if ask[len(ask) - 1] == 'r':
      return True
    elif ask[len(ask) - 1] == 's':
      os.system('cls')
      print_graph(wpms)
    elif ask[len(ask) - 1] == 'q':
      os.system('cls')
      return False
    else:
      inputError()

def printRace(text, current_word, start_time, index, monkeys, wpms):
  print(f"{bold}MonkeyWrite™{reset}")
  print("--------------------------------------------------")
  print(text)
  print("--------------------------------------------------")
  print("\nYou: ")
  print(f"{blue}-->{reset} {current_word}")
  elapsed_time = (time.time() - start_time)
  calculateWPM(elapsed_time, index, wpms) 
  for monkey in monkeys:
    monkey.print_progress_bar(len(monkey.monkey_text), start_time)

def logo():
  print(f"{bold}MonkeyWrite™{reset}")

def printIntroScreen(text, current_word, monkeys):
  input(f"\nPress{green} Enter{reset} to Start: ")
  os.system('cls')
  logo()
  print("--------------------------------------------------")
  print(text)
  print("--------------------------------------------------")
  print("\nYou: ")
  print(f"{blue}-->{reset} {current_word}")
  print(f"{blue}-->{reset} 0 WPM \n")
  for monkey in monkeys:
    print(monkey.name)
    print(f"{blue}-->{reset}")
    print(f"{blue}-->{reset} 0 WPM \n")

def splash():
    splash_length = 40
    row_1 = "MonkeyWrite™"
    row_2 = "Can you type faster than a monkey?"
    row_1_space = int((splash_length - len(row_1)) / 2)
    row_2_space = int((splash_length - len(row_2)) / 2)
    print("\n" +bold +"~" * splash_length + "\n" + " " * row_1_space + row_1 +"\n" + " " * row_2_space + row_2 + "\n" + "~" * splash_length, reset)

def leaderboard(wpm, monkeys):
  scores = [(monkey.name, monkey.final_monkey_wpm) for monkey in monkeys]
  scores.append(("You", wpm))

  scores.sort(key=lambda x: x[1], reverse = True) # [(monkey, wpm), (monkey2, wpm2)] -> [wpm, wpm2]


  print("\nLeaderboard:")
  for rank, (name, wpm) in enumerate(scores, start=1):
    if name != "You":
      if wpm == 0:
        print(f"{rank}. {name}: {BG_RED}{white}DNF{reset}")
      else:
        print(f"{rank}. {name}: {untouched_red}{wpm}{reset} WPM ")
    else:
      print(f"{rank}. {name}: {green}{wpm}{reset} WPM ")

# ---------------------------------------------------- GAME LOOP
def main():
  global kill_monkey
  kill_monkey = False
  os.system('cls')
  counter = 0
  index = 0 
  text = generateText()
  text, index = underliner(text, index)
  current_word = ""
  monkey_skill = 0
  splash()
  monkey_skill = difficultySelection(monkey_skill)
  wpms = []
  wpm_index = 0

  while True:
    
    try:
        amount_of_monkeys = int(input("How many monkeys do you want to play against? --> "))
        if checkAmountOfMonkeys(amount_of_monkeys):  
          if amount_of_monkeys >= 10:
            monkey_overload = input(f"{BG_YELLOW}{white}!!WARNING!!{reset}\nToo many monkeys may cause your PC to explode. Are you sure you want to proceed?\n(Please note that we are not responsible for the destruction of your computer)\ny){green} Yes{reset}\nn){untouched_red} No{reset}\nOption: ")
            if monkey_overload.lower() == 'y':
              pass
            else:
              continue
          monkeys = [Monkey(monkey_skill, text, "Monkey " + str(monkey + 1)) for monkey in range(amount_of_monkeys)]
          break
        else:
            inputError()
    except ValueError:
        inputError()
  printIntroScreen(text, current_word, monkeys)


  while True:
    current_letter = checkIndex(text, index)
    input_letter = keyboard.read_event()

    if(input_letter.event_type == keyboard.KEY_DOWN):

      input_letter = input_letter.name

      if input_letter == "0":
        kill_monkey = True
        
      if counter == 0:
        start_time = time.time()
      elapsed_time = time.time() - start_time
      wpm, wpms = calculateWPM(elapsed_time, wpm_index, wpms)


      if input_letter != "skift" and input_letter != "right shift":
        wpm_index += 1
        index, text = checkLetter(index, text, input_letter, current_letter)
        current_word = updateCurrentWord(text, index, current_word, input_letter)

        if counter == 0:   
          [monkey.monkey_thread.start() for monkey in monkeys]

        os.system('cls')
        text, index = underliner(text, index)
        printRace(text, current_word, start_time, wpm_index, monkeys, wpms)
 
        counter += 1
        
    if index >= len(text) and text.count(red) == 0:
      for monkey in monkeys:
        if monkey.monkey_counter == len(monkey.monkey_text) + 1:
          print(BG_RED+"You're slower than a f*cking monkey."+reset)
          break
      else:
        print(BG_GREEN+"YOU WIN!"+reset)
      
      leaderboard(wpm, monkeys)
      kill_monkey = True


      if raceAgain(wpms):
        monkeys = []
        main()
      break

if __name__ == "__main__":
  main()
  