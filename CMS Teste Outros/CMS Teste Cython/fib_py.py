def fib(n: int) -> int:
    a: int = 0
    b: int = 1

    for i in range(n):
        a, b = a + b, a

    return a