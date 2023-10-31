def Vernam(name, L):
    str = ""
    i = 0
    for t in name:
            str += chr(ord(t) ^ ord(L[i %len(L)]))
            i += 1
    return str

l = ['א','ב' ,'ג' ,'ד' ,'ה' ,'ו' ]

name = "שלום איתמר "
x = Vernam(name, l)
print(x)
y = Vernam(x, l)
print(y)
