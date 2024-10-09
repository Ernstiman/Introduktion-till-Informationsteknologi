
import os

class User():

  def __init__(self, username, password):
    self.username = username
    self.password = password
    self.items = []

  def importItems(self, file):
    items = file.readline()
    items = items.split()
    for item in items:
      if item not in self.items:
        self.items.append(item)


def checkForFile(user):
  items_file_name = f'{user.username}_items.txt'
  login_file_name = f'{user.username}_login.txt'
  login_list = os.listdir(os.getcwd() + "/logins")
  item_list = os.listdir(os.getcwd() + "/items")

  if(items_file_name not in item_list):
    items_file = open(os.getcwd() + "/items/" + items_file_name, "x+")
  else: 
    items_file = open(os.getcwd() + "/items/" + items_file_name, "r+")

  if(login_file_name not in login_list):
    login_file = open(os.getcwd() + "/logins/" + login_file_name, "x+")
  else: 
    login_file = open(os.getcwd() + "/logins/" + login_file_name, "r+")

  return(login_file, items_file)

def checkAccountDetails(users, username, password):
  for user in users:
    if (user.username == username and user.password == password):
      return True
  return False

def logIn(users):
  print("")
  username = input("User: ")
  password = input("Password:")

  if checkAccountDetails(users, username, password):
    for user in users:
      if (user.username == username and user.password == password):
        print("")
        print(f'Välkommen {username}')
        print("")
        menu(user)
  else:
    print("\nInvalid username or password!\n")
    tryAgain(logIn, users)

def checkIput():
  print("\nDu behöver ange ett av de angivna valen!!!\n")
  

def tryAgain(function, users = None):
  print("r) Try again")
  print("q) Quit ")
  val = input("\nOption: ")
  if val == "r":
    function(users)
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

def saveLogin(file, user):
  login_text = f'{user.username} {user.password}'
  file.write(login_text)
  file.close()
  pass

def quit(login_file, items_file,user):
  item_text = " " + " ".join(user.items)
  items_file.write(item_text)
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


def listItems(user):
  index = 1
  print("")
  for item in user.items:
    print(f'{index}. {item}')
    index += 1

def lookThroughFiles(users):
  for files in os.listdir(os.getcwd() + "/logins"):
      my_files = open(os.getcwd() + "/logins/" + files, "r")
      files = my_files.readline()
      files = files.split()
      print(files)
      users.append(User(files[0], files[1]))
      my_files.close()

def createAccount(users):
  username = input("Enter your username: ")
  password = input("Enter your password: ")

  while True:
    val = input(f'Are you sure you want the username: {username} and the password: {password}(y/n)? ')
    if val == "y":
      new_user = User(username, password)
      users.append(new_user)
      loginFile,_ = checkForFile(new_user)
      saveLogin(loginFile, new_user)
      break
    elif val == "n":
      createAccount(users)
      break
    else: 
      checkIput()


def main():
  users = []
  lookThroughFiles(users)
  while True: 
    print("\nWelcome to Lagra (TM) \n")
    print("l) Log in")
    print("c) Create account")
    print("q) Quit")
    val = input("\nOption: ")
    if val == "l": 
      logIn(users)
    elif val == "q":
      break
    elif val == "c":
      createAccount(users)
    else:
      checkIput()

if __name__ == "__main__":
  main()
