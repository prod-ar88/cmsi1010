def blocks(n):
    return 0 if n <= 0 else blocks(n-1) + n


def factorial(n):
    return 1 if n <= 1 else n * factorial(n - 1)


def print_count_down(n):
    if n <= 0:
        print("BOOM")
    else:
        print(n)
        print_count_down(n - 1)


print_count_down(5)

print("------------------")

print(blocks(8))
print(blocks(0))
print(blocks(-1))
print(blocks(1))
print(blocks(5))
print(blocks(10))

print("------------------")

print(factorial(67))
print(factorial(30))
print(factorial(40))
print(factorial(1))
print(len(str(factorial(52))))
print(factorial(9))
