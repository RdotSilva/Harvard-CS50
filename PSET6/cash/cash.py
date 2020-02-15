from cs50 import get_float


def main():
    change = get_change("How much change: ")

    # Initialize coin count.
    coins = 0

    # Round change.
    rounded = (change * 100)

    # Check all types of coins.
    while rounded >= 25:
        rounded -= 25
        coins += 1

    while rounded >= 10:
        rounded -= 10
        coins += 1

    while rounded >= 5:
        rounded -= 5
        coins += 1

    while rounded >= 1:
        rounded -= 1
        coins += 1

    print(str(coins) + " coins")


# Prompt user change.
def get_change(prompt):
    while True:
        n = get_float(prompt)
        if n > 0:
            break
    return n


if __name__ == "__main__":
    main()