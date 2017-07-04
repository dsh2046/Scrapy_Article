from itertools import islice
import datetime
import random, re

a = 'asd sdsd D12213-2121'
print(re.findall(r'\bD.*', a))
