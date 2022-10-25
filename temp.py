class Foo(object):
    def __eq__(self, other):
        return True


print(Foo() == None)