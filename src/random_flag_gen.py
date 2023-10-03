import string
import random


start = "".join([random.choice(string.ascii_letters) for _ in range(5)])

middle = "".join([random.choice(tuple(set(string.printable) - {"\t", "\n", "\r", "\x0b", "\x0c", "{", "}", "(", ")", "[", "]"})) for _ in range(15)])

print(f"{start}{{{middle}}}")
