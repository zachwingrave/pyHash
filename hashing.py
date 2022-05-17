import time
import hashlib
import tqdm


def compute_hashes(dictionary="rockyou.txt", function="md5"):
    function = getattr(hashlib, "md5")
    averages = []

    with open(dictionary, "r", errors="ignore") as file:
        wordlist = file.read().split("\n")

    for word in tqdm.tqdm(wordlist):
        hash_start_time = time.time()
        function(word.encode("utf-8"))
        hash_duration = time.time() - hash_start_time
        averages.append(hash_duration)

    averages_total = 0
    for avg in averages:
        averages_total += avg

    average_time = averages_total / len(averages)

    return average_time


to_compare = ["md5", "sha1", "sha256", "sha512"]

for function in to_compare:
    print("Getting {} averages...".format(function.upper()))
    average_time = compute_hashes(function=function)
    print("Average Hash Time: {:e}".format(average_time))
