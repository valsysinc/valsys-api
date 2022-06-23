lst = [1, 2, 3, 4]

for i, l in enumerate(lst):
    print(i, l)
    if i == 1:
        lst.append('hello')
