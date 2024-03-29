from string import ascii_letters
from string import digits
from string import punctuation
import hashlib
import itertools
import time
import tqdm

ALPHABET = ascii_letters + digits + punctuation  # try changing this, what happens?
FUNCTIONS = ("md5", "sha1", "sha224", "sha256", "sha384", "sha512")


def brute_force_attack(
    password,
    alphabet=ALPHABET,
    function=getattr(hashlib, "md5"),
    empty=True,
    salt=None,
    saltpos=0,
):  # where the magic happens!
    print("Target Hash:", password)

    results = {
        "password": None,
        "cracked": False,
        "attempts": 0,
        "duration": 0,
        "fileLoadTime": None,
    }

    range_start = 0  # test empty string by default
    if empty == False:
        range_start = 1

    start_time = time.time()

    # this is where the hard work happens

    for length in range(range_start, 16):
        print("Hashing passwords of length:", length)
        wordlist = itertools.product(alphabet, repeat=length)

        for word in tqdm.tqdm(
            wordlist
        ):  # this will happen for every single combination
            if salt != None:
                word = tuple_to_string(word)
                if saltpos == 0:
                    word = tuple(salt + word)
                elif saltpos == 1:
                    word = tuple(word + salt)
                elif saltpos == 2:
                    word = tuple(salt + word + salt)

            results["attempts"] += 1
            guess = function("".join(word).encode("utf-8")).hexdigest()

            if guess == password:
                results["duration"] = round(time.time() - start_time, 2)
                results["password"] = "".join(word)
                results["cracked"] = True  # gotcha!
                return results

    # and the hard work is done!

    end_time = round(time.time() - start_time, 2)
    results["duration"] = end_time
    return results


def dictionary_attack(
    password,
    dictionary="rockyou.txt",
    function=getattr(hashlib, "md5"),
    salt=None,
    saltpos=0,
):
    print("Target Hash:", password)

    results = {
        "password": None,
        "cracked": False,
        "attempts": 0,
        "duration": 0,
        "fileLoadTime": None,
    }

    file_load_start = time.time()
    with open(dictionary, "r", errors="ignore") as file:
        wordlist = file.read().split("\n")
    results["fileLoadTime"] = round(time.time() - file_load_start, 2)

    start_time = time.time()

    for word in tqdm.tqdm(wordlist):
        if salt != None:
            word = tuple_to_string(word)
            if saltpos == 0:
                word = tuple(salt + word)
            elif saltpos == 1:
                word = tuple(word + salt)
            elif saltpos == 2:
                word = tuple(salt + word + salt)

        results["attempts"] += 1
        guess = function("".join(word).encode("utf-8")).hexdigest()

        if guess == password:
            results["duration"] = round(time.time() - start_time, 2)
            results["password"] = "".join(word)
            results["cracked"] = True  # gotcha!
            return results

    results["duration"] = round(time.time() - start_time, 2)
    return results


def power(n, m):
    """Return base 'n' to power of exponent 'm'"""
    if m == 0:
        return 1
    else:
        return n * power(n, m - 1)


def tuple_to_string(a):
    b = ""
    for i in a:
        b = b + i
    return b


def find_target_index(password, alphabet=ALPHABET, empty=True):
    current_power = len(password) - 1
    base = len(alphabet)
    pos = 0
    for char in password:
        char_pos = alphabet.find(char) + 1
        pos += char_pos * power(base, current_power)
        current_power -= 1
    if empty == True:
        return pos + 1  # empty string takes first position
    else:
        return pos


def hash_and_attack():
    password = input("Enter password: ")
    salt = input("Enter salt (no salt): ")

    if salt != "":
        saltpos = input("Enter salt position (1): ")
        if saltpos == "":
            saltpos = 1
        else:
            saltpos = int(saltpos)

        if saltpos == 0:
            password = salt + password
        elif saltpos == 1:
            password = password + salt
        elif saltpos == 2:
            password = salt + password + salt
    else:
        salt = None
        saltpos = None

    password = password.encode("utf-8")
    hash_function = input("Enter hash function (md5): ").strip().lower()

    if hash_function not in FUNCTIONS:
        if hash_function == "":
            hash_function = getattr(hashlib, "md5")
        else:
            raise Exception("Unsupported hash function.")  # check the FUNCTIONS list
    else:
        hash_function = getattr(hashlib, hash_function)

    print("1. Brute Force Search")
    print("2. Dictionary Attack")

    mode = input("Choose method of attack (brute force): ").strip()
    digest = hash_function(password).hexdigest()  # password is hashed here

    if mode == "":
        mode = 1
    else:
        mode = int(mode)

    if mode == 1:
        # prediction = find_target_index(password.decode('utf-8'))
        # print('Predicted position: ', prediction)
        results = brute_force_attack(
            password=digest, function=hash_function, salt=salt, saltpos=saltpos
        )
    elif mode == 2:
        dictionary = input("Dictionary file (rockyou.txt): ").strip()
        if dictionary == "":
            dictionary = "rockyou.txt"
        results = dictionary_attack(
            password=digest,
            dictionary=dictionary,
            function=hash_function,
            salt=salt,
            saltpos=saltpos,
        )
    else:
        raise Exception("Unsupported attack method.")

    if results["cracked"]:
        print(
            "Cracked! Password is: '", results["password"], "'", sep=""
        )  # printing our results
    else:
        print("Password not found.", end=" ")

    print(
        "Took",
        results["attempts"],
        "attempts and",
        results["duration"],
        "seconds to compute.",
    )

    if results["fileLoadTime"] != None:
        print("Dictionary file load time:", results["fileLoadTime"], "seconds to load.")


def attack_existing_hash():
    digest = input("Enter hash digest: ")
    salt = input("Enter salt (no salt): ")

    if salt != "":
        saltpos = input("Enter salt position (1): ")
        if saltpos == "":
            saltpos = 1
        else:
            saltpos = int(saltpos)
    else:
        salt = None
        saltpos = None

    hash_function = input("Enter hash function (md5): ").strip().lower()

    if hash_function not in FUNCTIONS:
        if hash_function == "":
            hash_function = getattr(hashlib, "md5")
        else:
            raise Exception("Unsupported hash function.")  # check the FUNCTIONS list
    else:
        hash_function = getattr(hashlib, hash_function)

    print("1. Brute Force Search")
    print("2. Dictionary Attack")

    mode = input("Choose method of attack (brute force): ").strip()

    if mode == "":
        mode = 1
    else:
        mode = int(mode)

    if mode == 1:
        # prediction = find_target_index(password.decode('utf-8'))
        # print('Predicted position: ', prediction)
        results = brute_force_attack(
            password=digest, function=hash_function, salt=salt, saltpos=saltpos
        )
    elif mode == 2:
        dictionary = input("Dictionary file (rockyou.txt): ").strip()
        if dictionary == "":
            dictionary = "rockyou.txt"
        results = dictionary_attack(
            password=digest,
            dictionary=dictionary,
            function=hash_function,
            salt=salt,
            saltpos=saltpos,
        )
    else:
        raise Exception("Unsupported attack method.")

    if results["cracked"]:
        print(
            "Cracked! Password is: '", results["password"], "'", sep=""
        )  # printing our results
    else:
        print("Password not found.", end=" ")

    print(
        "Took",
        results["attempts"],
        "attempts and",
        results["duration"],
        "seconds to compute.",
    )

    if results["fileLoadTime"] != None:
        print("Dictionary file load time:", results["fileLoadTime"], "seconds to load.")


def main():
    print("1. Hash and attack (demo)")
    print("2. Attack existing hash")

    mode = input("Enter your choice (1): ").strip()

    if mode == "":
        mode = 1
    else:
        mode = int(mode)

    if mode == 1:
        hash_and_attack()
    elif mode == 2:
        attack_existing_hash()


if __name__ == "__main__":
    main()  # run the program
