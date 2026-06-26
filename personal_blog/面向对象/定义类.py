class People():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print('我是%s, 我今年%s岁' % (self.name, self.age))

people1 = People('张三', 18)
people1.introduce()

people2 = People('李四', 20)
people2.introduce()

people3 = People('王五', 22)
people3.introduce()