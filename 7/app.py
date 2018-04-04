class A:
    static = "static"

    def __init__(self):
        self.local = "local"

    def method(self):
        print(self.local)


class B(A):
    def __init__(self):
        super(B, self).__init__()
        self.local2 = "local2"

    def method2(self):
        print(self.local2)


print(A.__name__, A.__dict__, A.__bases__)
print(B.__name__, B.__dict__, B.__bases__)
print(dir(A))
print(dir(B))
print(dir(A()))
print(B().__class__.__name__, B().__dir__())