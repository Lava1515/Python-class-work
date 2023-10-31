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
            k=" "
        str += k
    return str

name = "אבגדהו"
n = 9
print(name)
x = encrypt(name, n)
print(x)
k = decrypte(x,n)
print(k)
