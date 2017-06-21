from itertools import islice
import os

x = {'a': 1, 'b': 2}
y = {'b': 3, 'c': 4}
z = {**x, **y}
print(os.getcwd())
print(os.path.abspath(os.path.dirname(__file__)))
