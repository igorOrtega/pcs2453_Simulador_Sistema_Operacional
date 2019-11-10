x = [1 , 2, 3]

try:
    next(i for i in x if i == 2)
    print("ok")
except:
    pass