class human:
    def __init__(self, name, age, color):
        self.name = name
        self.age = age
        self.color = color

    def get_age(self):
        return self.age


class Yuval(human):
    def __init__(self):
        super(Yuval, self).__init__("yuval", 17, "YA SHAHOR")

    def __repr__(self):
        return f"{self.name, self.age, self.color}"


Y = Yuval()

print(Y)
