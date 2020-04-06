from string import ascii_letters
from itertools import product
from time import time, sleep
from hashlib import md5

class Attacker:

  numbers = "0123456789"
  letters = ascii_letters
  special = " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
  alphabet = numbers + letters + special

  def __init__(self, defender):
    self.defender = defender
    self.reset()

  def single_brute_force_md5(self, string):  
    self.target = string.hexdigest()
    print("Target:", self.target)
    
    self.start_time = time()
    for length in range(0, 129):
      print("Hashing passwords of length:", length, end=" ")
      for string in product(self.alphabet, repeat=length):
        self.attempts += 1
        string = "".join(string)
        guess = self.defender.hash_md5(string).hexdigest()
        if guess == self.target:
          self.password = string
          self.end_time = time()
          self.cracked = True
          break
      print("... Done.")
      if self.cracked: break
    
    if not self.cracked: self.end_time = time()
    self.duration = self.end_time - self.start_time
    self.print_report()
    self.reset()
  
  def reset(self):
    self.password = None
    
    self.target = None
    self.cracked = False
    self.attempts = 0

    self.start_time = 0
    self.end_time = 0
    self.duration = 0

  def print_report(self):
    print("Cracked:", self.cracked)
    print("Attempts:", self.attempts)
    print("Duration:", self.duration)
    print("Password:", self.password)
