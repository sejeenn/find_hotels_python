def foo():
    yield 1


f = foo()
next(f)
print(next(f))
