def Vernam(name, L):
    str = ""
    i = 0
    for t in name:
            str += chr(ord(t) ^ ord(L[i %len(L)]))
            i += 1
    return str


def encrypt(word, n):
    str = ""
    for t in word:
        if t !=" ":
            x = ord(t) + n
            if x > ord('ת'):
                k = chr(x - 27)
            else:
                k = chr(x)

        else:
            k =" "
        str += k
    return str


def decrypte(word, n):
    str = ""
    for t in word:
        if t !=" ":
            x = ord(t) - n
            if x < ord('א'):
                k = chr(x + 27)
            else:
                k = chr(x)
        else:
            k= " "
        str += k
    return str


l = ['א','ב' ,'ג' ,'ד' ,'ה' ,'ו' ]
nl = ['ו','ה' ,'ד' ,'ג' ,'ב' ,'א' ]
n = 4
name1 = "9a 9d a0 a4 95 a6 20 90 a7 a6 a8 a5 95 a6 20 "
name2 = "90 97 a6 91 a8 a6 20 a7 a6 20 93 a0 a5 91"

# Rname1 ="d79ad79dd7a0d7a4d795d7a620d790d7a7d7a6d7a8d7a5d795d7a620d7"
# Rname2 ="90d797d7a6d791d7a8d7a620d7a7d7a620d793d7a0d7a5d791"
# name = "ךםנפוצ אקצרץוצ אחצברצ קצ דנץב"
# name = name1 + " " + name2
# Rname =Rname1 + " " + Rname2
# name1 ="62275c78303735"
name3 = "\x075;\x06\xd7\xb4\x05"

"\x075;\x06\xd7\xb4\x05"

h = Vernam(name3, l)
print(h)
# c = encrypt(name, n)
# print(c)
# i = Vernam(c, l)
# print(i)

# u = decrypte(i,n)
# print(u)
#
# print()
# c1 = Vernam(Rname, l)
# print(c1)
#
# i1 = encrypt(c1, n)
# print(i1)



