class Student(object):
    _name = 'keke'

    def __init__(self, name=None):
        if name is not None:
            self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = 'HHHHH' + value


stu = Student('zhouxy')
stu.name = '123'
print(stu.name)
