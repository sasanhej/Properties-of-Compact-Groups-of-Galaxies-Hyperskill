import itertools

x=0
for i in itertools.chain(countries):
    if int(list(i.values())[1]) > 100:
        x += 1
print(x)
