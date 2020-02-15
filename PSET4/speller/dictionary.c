// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>

#include "dictionary.h"

// Functions
unsigned int size(void);
bool check(const char *word);
bool unload(void);


// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;


// Represents a hash table (value N is hardcoded above at 26)
node *hashtable[N];

// Total dict words loaded
unsigned int dict_words = 0;

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    // Value of 'a' is 97.
    return tolower(word[0]) - 'a';
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary (FILE is included in <stdio.h>)
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {

        // Hash the word (this will return the index of a bucket in the hash table)
        int word_hash = hash(word);

        // Free up memory for each node that is created.
        // Creates the "boxes" that hold the address and next.
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            unload();
            return false;
        }

        // Copy word into new_node
        strcpy(new_node->word, word);

        // Point the new node to head to hold position and not break link
        // Same as new_node.next = hashtable[word_hash]
        new_node->next = hashtable[word_hash];

        // Insert the word into the hash table.
        hashtable[word_hash] = new_node;

        // Count number of words added to dictionary. This will be passed into size.
        dict_words++;

    }

    // Close dictionary
    fclose(file);

    // Print the size of the dicitonary.
    printf("Size of dict: %i", size());

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // Get the number of words added to the dictionary. dict_words comes from the main loop.
    if (dict_words)
    {
        return dict_words;
    }
    return 0;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Set the head
    node *head = hashtable[hash(word)];

    // Make a copy of the head to be safe.
    node *cursor = head;

    // Loop until the pointer is null which represents the end of the table.
    while (cursor != NULL)
    {
        // Compare the text word with dictionary word.
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        else
        {
            // Reassign cursor to the next node it points to.
            cursor = cursor->next;
        }
    }
    // Return false if word is not in dictionary.
    return false;


}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    unsigned int index = 0;

    // Check N amount of buckets.
    if (index < N)
    {
        // Loop through each bucket and free each linked list node.
        for (int i = 0; i < N; i++)
        {

            // Set the head
            node *head = hashtable[i];

            // Copy head to cursor.
            node *cursor = head;

            while (cursor != NULL)
            {
                node *temp = cursor;
                cursor = cursor->next;
                free(temp);
            }

            free(cursor);
            index++;
        }
        return true;
    }
    return false;
}
