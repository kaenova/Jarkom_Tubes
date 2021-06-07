import datetime

x = datetime.datetime.now()
print(str(x.date()))
print("{:%H:%M:%S}".format(x))