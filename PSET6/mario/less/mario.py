from cs50 import get_int


def main():
    height = get_height("Enter a number between 1-8 ")

    # Create pyramid based on height.
    for i in range(height):
        print(" " * ((height-i) - 1), end="")
        print("#" * (i+1), end="")
        print()


# Prompt user for height number.
def get_height(prompt):
    while True:
        n = get_int(prompt)
        if n > 0 and n <= 8:
            break
    return n


if __name__ == "__main__":
    main()