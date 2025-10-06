def blocks(n):
    return 0 if n <= 0 else blocks(n-1) + n


print(blocks(8))
print(blocks(0))
print(blocks(-1))
print(blocks(1))
print(blocks(5))
print(blocks(10))
