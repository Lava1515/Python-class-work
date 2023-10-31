import random


class Tzora:

    def __init__(self, color, area, heikef):
        self.color = color
        self.S = area
        self.P = heikef

    def set_color(self, color):
        self.color = color

    def color(self):
        return self.color

    def shetah(self):
        return self.S

    def set_shetah(self, shetah):
        self.color = shetah

    def heikef(self):
        return self.P

    def set_heikef(self, heikef):
        self.color = heikef


class Rectangle(Tzora):
    def __init__(self, color, width, length):
        super().__init__(color, width*length, length*2 + width*2)
        self.width = width
        self.length = length

    def set_width(self, width):
        self.width = width
        super().set_heikef(self.width * 2 + self.length * 2)
        super().set_shetah(self.width * self.length)

    def set_length(self, length):
        self.length = length
        super().set_heikef(self.width * 2 + self.length * 2)
        super().set_shetah(self.width * self.length)

    def get_width(self):
        return self.width

    def get_length(self):
        return self.length

    def ADD_rectangles(self, rectangle2):
        new = Tzora("red", None, None)
        new.set_shetah(self.shetah() + rectangle2.shetah())
        new.set_heikef(self.heikef() + rectangle2.heikef())
        return new


class Circle(Tzora):
    def __init__(self, color, radius):
        super().__init__(color, radius*radius * 3.14, radius*2 * 3.14)
        self.radius = radius

    def set_radius(self, radius):
        self.radius = radius
        super().set_shetah(self.radius*radius * 3.14)
        super().set_heikef(self.radius*2 * 3.14)

    def get_radius(self):
        return self.radius


class Square(Rectangle):
    def __init__(self, color, zela):
        super().__init__(color, zela, zela)
        self.zela = zela

    def get_zela(self):
        return self.zela

    def ADD_rectangle_square(self, rect):
        new = Tzora("red", None, None)
        new.set_shetah(self.shetah() + rect.shetah())
        new.set_heikef(self.heikef() + rect.heikef())
        return new

    def ADD_squares(self, square2):
        new = Tzora("red", None, None)
        new.set_shetah(self.shetah() + square2.shetah())
        new.set_heikef(self.heikef() + square2.heikef())
        return new


class Container():
    def __init__(self):
        self.lst: list[Tzora] = []
        self.colors = ["Green", "Red", "Blue", "Orange", "Pink", "Yellow",
                       "Violet", "Brown", "Purple", "Gray", "White", "Black",
                       "Gold", "Silver", "Cyan"]

    def genarate(self, x):
        for i in range(int(x)):
            k = random.randint(1, 3)
            if k == 1:
                n = random.randint(0, len(self.colors) - 1)
                rect = Rectangle(self.colors[n], random.randint(1, 100), random.randint(1, 100))
                self.lst.append(rect)

            elif k == 2:
                n = random.randint(0, len(self.colors) - 1)
                squ = Square(self.colors[n], random.randint(1, 100))
                self.lst.append(squ)

            elif k == 3:
                n = random.randint(0, len(self.colors) - 1)
                cir = Circle(self.colors[n], random.randint(1, 100))
                self.lst.append(cir)

    def sumAreas(self):
        Sum = 0
        for i in self.lst:
            Sum += i.shetah()
        return Sum

    def sumPerimeter(self):
        Sum = 0
        for i in self.lst:
            Sum += i.heikef()
        return Sum


my_container = Container()
my_container.genarate(100)
print("total area:", my_container.sumAreas())
print("total perimeter:", my_container.sumPerimeter())

