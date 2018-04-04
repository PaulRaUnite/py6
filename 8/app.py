def debug(class_attrs=False, filter_builtin=True) -> callable:
    def decorator(cls):
        def cls_repr(cls) -> str:
            head = f"class {cls.__name__}\n"
            parents = f"parents {cls.__bases__}\n"
            methods = "methods:\n"
            static = "static:\n"
            for key in dir(cls):
                if filter_builtin and key.startswith("__"):
                    continue
                value = getattr(cls, key)
                if key in {"__module__", "__doc__", "__dict__"}:
                    continue
                if callable(value):
                    methods += f"    {key}() -> {value}\n"
                    continue
                if not key.startswith("__"):
                    static += f"    {key} = {value}\n"

            return head + parents + methods + static

        def repr(self) -> str:
            output = ""
            if class_attrs:
                output += cls_repr(self.__class__)
            output += "instance data:\n"
            for key, value in self.__dict__.items():
                if not key.startswith("__") and not callable(value):
                    output += f"    {key} = {value}\n"
            return output

        cls.__repr__ = repr
        return cls

    return decorator


@debug(class_attrs=True)
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


print(B())
print(A())
