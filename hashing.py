from os import system, name

from attack import *
from defend import *

class Hashing:

  attacker = None
  defender = None
  running = False

  def __init__(self):
    self.defender = Defender()
    self.attacker = Attacker(self.defender)
    self.running = True

  def main(self):
    while self.running:
      self.clear()
      print("Hashing Playground v2.0")
      print("=======================")
      print("1. Single Brute Force MD5")
      print("2. List Brute Force MD5")
      print("3. Single Dictionary MD5")
      print("4. List Dictionary MD5")

      option = input("\nType [Q] to quit: ")
      
      if option == "q" or option == "Q":
        self.running = False
        self.clear()
        raise SystemExit
      else:
        option = int(option)

      string = input("Enter password: ")

      self.clear()
      if option == 1:
          print("Brute Force Single")
          print("==================")
          string = self.defender.hash_md5(string)
          self.attacker.single_brute_force_md5(string)
      elif option in [2,3,4]:
          print("Under construction.", end=" ")
      else:
          print("Invalid option.", end=" ")
      input("Press [ENTER] to continue.")

  def clear(self):
    if name == "nt":
        system("cls")   # System is running Windows.
    else:
        system("clear") # System is running Unix.

program = Hashing()
program.main()
