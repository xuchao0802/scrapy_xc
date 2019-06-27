def yield_test():
    a = "xuchao"
    b = "lin"
    name = yield a
    print(name)
    add = yield b
    print(add)

a = yield_test()
fanhui1 = next(a)
print(fanhui1)
fanhui2 = a.send("haha")
print(fanhui2)
