from string import ascii_letters
from string import digits
from string import punctuation
import hashlib
import itertools
import os
import time
import tqdm

ALPHABET = ascii_letters + digits + punctuation # try changing this, what happens?
FUNCTIONS = ("md5", "sha1", "sha224", "sha256", "sha384", "sha512")

def brute_force_attack(password, function):   # where the magic happens!
  print("Target Hash:", password)
  start_time = time.time()

  results = {
    "password": None,
    "cracked": False,
    "attempts": 0,
    "duration": 0,
  }

  # this is where the hard work happens

  for length in range(0, 16):
    print("Hashing passwords of length:", length)
    wordlist = itertools.product(ALPHABET, repeat=length)

    for word in tqdm.tqdm(wordlist): # this will happen for every single combination
      results["attempts"] += 1
      guess = function("".join(word).encode("utf-8")).hexdigest()

      if guess == password:
        end_time = round(time.time() - start_time, 2)
        results["password"] = "".join(word)
        results["duration"] = end_time
        results["cracked"] = True   # gotcha!
        return results

  # and the hard work is done!

  end_time = round(time.time() - start_time, 2)
  results["duration"] = end_time
  return results

def dictionary_attack(password, function, dictionary="rockyou.txt"):
  print("Target Hash:", password)
  start_time = time.time()

  results = {
    "password": None,
    "cracked": False,
    "attempts": 0,
    "duration": 0,
  }

  with open(dictionary, "r", errors="ignore") as file:
    wordlist = file.read().split("\n")

  for word in tqdm.tqdm(wordlist):
    results["attempts"] += 1
    guess = function(word.encode("utf-8")).hexdigest()

    if guess == password:
      end_time = round(time.time() - start_time, 2)
      results["password"] = "".join(word)
      results["duration"] = end_time
      results["cracked"] = True   # gotcha!
      return results

  end_time = round(time.time() - start_time, 2)
  results["duration"] = end_time
  return results

def main():
  password = input("Enter password: ").encode("utf-8")
  function = input("Enter hash function: ").strip().lower()

  if function not in FUNCTIONS:
    raise Exception("Unsupported hash function.") # check the FUNCTIONS list
  else:
    function = getattr(hashlib, function)

  print("1. Brute Force Search")
  print("2. Dictionary Attack")

  mode = int(input("Choose method of attack: ").strip())
  password = function(password).hexdigest() # password is hashed here

  if mode == 1:
    results = brute_force_attack(password, function)
  elif mode == 2:
    dictionary = input("Dictionary file (rockyou.txt): ").strip()
    if dictionary == "":
      dictionary = "rockyou.txt"
    results = dictionary_attack(password, function, dictionary)
  else:
    raise Exception("Unsupported attack method.")

  if results["cracked"]:
    print("Cracked! Password is: \'", results["password"], "\'", sep="") # printing our results
  else:
    print("Password not found.", end=" ")

  print("Took", results["attempts"], "attempts and", results["duration"], "seconds to compute.")

if __name__ == "__main__":
  main() # run the program
