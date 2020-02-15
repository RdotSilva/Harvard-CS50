from cs50 import get_string
from sys import argv


def main():
    # Check command line to make sure only 1 argument is provided and it contains .txt file extension.
    if len(argv) == 2:
        text_file = argv[1]
        if ".txt" in text_file:
            print(text_file)
        else:
            print("Must be txt file")
            exit(1)
    else:
        print("Invalid Input")
        exit(1)

    # Open and read the text file line by line, store each line LIST or SET (look em up)
    infile = text_file

    # Set of banned words.
    banned = set()

    # Open & read banned word text file.
    file = open(infile, "r")
    for line in file:
        banned.add(line.rstrip("\n"))
    file.close()

    # Get user phrase to censor.
    user_text = get_string("Provide a message to censor: ")

    # Split the word on spaces, then check each word against the banned list of words created above.
    split_text = user_text.split(" ")

    # Print the message user provided, if the word is banned replace it with *****.
    for word in split_text:
        if word.lower() in banned:
            word = "*" * len(word)
            print(word + " ", end="")
        else:
            print(word + " ", end="")

    print()


# Get user string.
def get_plain(prompt):
    return get_string(prompt)


if __name__ == "__main__":
    main()
