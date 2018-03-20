# Can be used if you don't want to use a whole class
# if you have to just create a function that catches some data.


class A:
    def __init__(self, i: int = 0):
        self.__value: int = i

    def f(self):
        print("A.f!", self.__value)


def gen(i: int = 0) -> callable:
    def g():
        print("g!", i)

    return g


def api_func(func: callable):
    func()


a = A()
api_func(a.f)
api_func(gen())


class Callbacked:
    def __init__(self):
        self.number: int = 0

    def callback(self) -> callable:
        def cl(x: int):
            self.number = x

        return cl

    def __repr__(self) -> str:
        return f"Callbacked: {self.number}"


obj = Callbacked()
obj.callback()(10)
print(obj)
