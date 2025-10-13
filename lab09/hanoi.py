import sys


move_count = 0


def move(n, source, destination, auxiliary):
    global move_count
    if n > 0:
        move(n - 1, source, auxiliary, destination)
        move_count += 1
        print(f"Move {move_count}: Move disk {n} from {source} to {destination}")
        move(n - 1, auxiliary, destination, source)


print(sys.argv[0])
try:
    if len(sys.argv) != 2:
        raise ValueError("Exactly one argument is required")
    if not sys.argv[1].isdigit():
        raise ValueError("The argument must be a positive integer")
    number_of_disks = int(sys.argv[1])
    if number_of_disks < 1 or number_of_disks > 20:
        raise ValueError(
            "The argument must be between 1 and 20, inclusive")
    move(number_of_disks, "A", "B", "C")
    print(f"Total moves completed: {move_count}")
except ValueError as e:
    print(f"Error: {e}")
