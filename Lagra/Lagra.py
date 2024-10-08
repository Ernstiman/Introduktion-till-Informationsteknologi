
import os

class User():

  def __init__(self):
    self.username = "Viktor"
    self.password = "1234"
    self.items = []

  def importItems(self, file):
    items = file.readline()
    items = items.split()
    for item in items:
      if item not in items:
        self.items.append(item)


def checkForFile(user):
  items_file_name = f'{user.username}_items.txt'
  login_file_name = f'{user.username}_login.txt'
  list = os.listdir(os.getcwd())

  if(items_file_name not in list):
    items_file = open(items_file_name, "x+")
  else: 
    items_file = open(items_file_name, "r+")

  if(login_file_name not in list):
    login_file = open(login_file_name, "x+")
  else: 
    login_file = open(login_file_name, "r+")

  return(login_file, items_file)


  
def logIn(user):
  print("")
  username = input("User: ")
  password = input("Password:")

  if(user.username == username and user.password == password):
    print("")
    print(f'Välkommen {username}')
    print("")
    menu(user)
  else:
    print("\nInvalid username or password!\n")
    tryAgain(logIn, user)

def checkIput():
  print("\nDu behöver ange ett av de angivna valen!!!\n")
  

def tryAgain(function, user = None):
  print("r) Try again")
  print("q) Quit ")
  val = input("\nOption: ")
  if val == "r":
    function(user)
  elif val != "q":
    checkIput()

def menu(user):
  login_file,items_file = checkForFile(user)
  user.importItems(items_file)
  while True:
    print("\nSelect a option \n")
    print("a) Add items: ")
    print("l) List items: ")
    print("q) Log out: ")
    val = input("\nOption:")
    if val == "a":
      addItem(user)
    elif val == "l":
      listItems(user)
    elif val == "q":
      quit(login_file, items_file, user)
      break
    else: 
      checkIput()
    pass

def quit(login_file, items_file,user):
  login_text = f'{user.username} {user.password}'
  item_text = " ".join(user.items)
  login_file.write(login_text)
  items_file.write(item_text)
  login_file.close()
  items_file.close()

def addItem(user):
  item = input("\nWhat Item do you want to add -->")
  user.items.append(item)
  print(f'\n{item} has been added\n')



def fileOpener(user):
  name = f'{user.username}_items.txt'
  file = open(name, "r+")
  return file
  pass
def write(file):
  pass

def read(file):
  pass

def createFile(file):
  pass

def listItems(user):
  index = 1
  print("")
  for item in user.items:
    print(f'{index}. {item}')
    index += 1
  pass


def main():
  viktor = User()
  while True: 
    print("\nWelcome to Lagra (TM) \n")
    print("l) Log in")
    print("q) Quit")
    val = input("\nOption: ")
    if val == "l": 
      logIn(viktor)
    elif val == "q":
      break
    else:
      checkIput()

if __name__ == "__main__":
  main()
