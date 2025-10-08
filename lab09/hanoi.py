def move(n, source, destination, auxiliary):
    if n > 0:
        move(n - 1, source, auxiliary, destination)
        print(f"Move disk {n} from {source} to {destination}")
        move(n - 1, auxiliary, destination, source)


move(3, "A", "B", "C")
