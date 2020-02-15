from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    # Split each string at new line.
    list_a = a.splitlines()
    list_b = b.splitlines()

    # Initialize a set.
    list_c = set()

    # Iterate through every line in first list.
    for line in list_a:
        if line in list_b:
            list_c.add(line)

    # Cast the set into a list and return.
    return list(list_c)


def sentences(a, b):
    """Return sentences in both a and b"""

    # Split each string into sentences.
    list_a = sent_tokenize(a, language='english')
    list_b = sent_tokenize(b, language='english')

    # Initialize a set.
    list_c = set()

    # Iterate through every sentence in first list.
    for sentence in list_a:
        if sentence in list_b:
            list_c.add(sentence)

    # Cast the set into a list and return.
    return list(list_c)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    list_a = substring_helper(a, n)
    list_b = substring_helper(b, n)

    # Initialize a set.
    list_c = set()

    # Iterate through every substring in first list.
    for substring in list_a:
        if substring in list_b:
            list_c.add(substring)

    # Cast the set into a list and return.
    return list(list_c)


def substring_helper(string, n):
    """Substring helper returns substrings of n length"""

    length = len(string) + 1
    return [string[i:i+j] for i in range(length-n) for j in range(n, n+1)]