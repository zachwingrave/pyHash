from string import ascii_letters
from itertools import product
from time import time, sleep
from os import system, name
from hashlib import md5

def main():
  running = True
  while running:
    clear_screen()
    print("Hashing Playground v1.0 | MD5")
    print("=============================")
    print("1. Single Brute Force")
    print("2. List Brute Force")
    print("3. Single Dictionary")
    print("4. List Dictionary")
    print("5. Quit")

    option = int(input("\nEnter your choice: "))

    clear_screen()
    if option == 1:
      print("Brute Force Single")
      print("==================")
      password = input("Enter password (default = \"hash\"): ")
      if password == "":
        single_brute_force_md5()
      else:
        single_brute_force_md5(password)
      input("Press [ENTER] to continue.")
    elif option == 2:
      print("Under construction.", end=" ")
      input("Press [ENTER] to continue.")
    elif option == 3:
      print("Under construction.", end=" ")
      input("Press [ENTER] to continue.")
    elif option == 4:
      print("Under construction.", end=" ")
      input("Press [ENTER] to continue.")
    elif option == 5:
      running = False
    else:
      print("Invalid option.", end=" ")
      input("Press [ENTER] to continue.")
    option = None

  raise SystemExit

def single_brute_force_md5(password="hash"):
  alphabet = ascii_letters + "0123456789"
  utf_password = password.encode("utf-8")
  hashed_pass = md5(utf_password).hexdigest()
  print("MD5 Hash:", hashed_pass)
  cracked = False
  attempts = 0

  start_time = time()
  for length in range(1, 32):
    print("Hashing passwords of length:", length, end=" ")
    for word in product(alphabet, repeat=length):
      attempts += 1
      guess = "".join(word).encode("utf-8")
      hashed_guess = md5(guess).hexdigest()
      if hashed_guess == hashed_pass:
        end_time = time() - start_time
        cracked = True
        break
    print("... Done.")
    if cracked:
      break
  
  print_report(cracked, attempts, end_time)

def print_report(cracked, attempts, time):
  if cracked:
    print("Cracked!", end=" ")
  else:
    print("Password not found.", end=" ")
  print("Took", attempts, "attempts and", time, "seconds to compute.")

def clear_screen():
  if name == "nt":
    system("cls")   # System is running Windows.
  else:
    system("clear") # System is running Unix.

main()