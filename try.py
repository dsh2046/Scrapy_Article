from itertools import islice
import datetime

value = '\n\n\r    2017-01-12 .'
create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
print(create_date)
