from hashlib import md5

class Defender:

  def __init__(self):
    return

  def hash_md5(self, string):
    return md5(string.encode("utf-8"))
