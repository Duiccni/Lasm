def foo(bar: int) -> int:
    if bar == 2:
        return 2
    return bar * foo(bar - 1)


print(foo(5))
