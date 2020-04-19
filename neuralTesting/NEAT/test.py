a = [1,2,3,4,5,6,7,8,9,10]

i = 2 - 1
while i+1 < len(a):
    print("BEFORE", a)
    i+= 1
    a.pop(i)
    i-= 1
    print("AFTER", a)

print("done")
