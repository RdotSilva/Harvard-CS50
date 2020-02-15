from sys import argv
from cs50 import get_string


def main():
    # Check command line arguments to make sure they are valid.
    if len(argv) == 2:
        k = int(argv[1])
        if k > 0:
            print(k)
        else:
            print("NO")
    else:
        print("Invalid Input")
        exit(1)

    # Prompt user for plain text.
    plain_text = get_plain("plaintext: ")
    print("ciphertext: ", end="")

    # Loop through every letter in plain text.
    for letter in plain_text:
        if (letter.isalpha()):
            if (letter.isupper()):
                new_letter = (ord(letter) - ord('A') + k) % 26
                print(chr(new_letter + ord('A')), end="")
            elif (letter.islower()):
                new_letter = (ord(letter) - ord('a') + k) % 26
                print(chr(new_letter + ord('a')), end="")
        else:
            print(letter, end="")
    print()


# Get plain text string.
def get_plain(prompt):
    return get_string(prompt)


if __name__ == "__main__":
    main()