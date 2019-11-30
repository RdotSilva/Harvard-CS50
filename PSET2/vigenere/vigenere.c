#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int shift(char c);
int shifted;

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        return 1;
    }
    
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (!isalpha(argv[1][i]))
        {
            return 1;
        }
    }
    
    int c;
    
    string text = get_string("plaintext: ");
    
    printf("ciphertext: ");
    
    int j = 0;
    
    for (int i = 0; i < strlen(text); i++)
    {
        int key = shift(argv[1][j]);
        
        if (isalpha(text[i])) 
        {
            if (j < strlen(argv[1]) - 1)
            {
                j++;
            }
            else
            {
                j = 0;
            }
        }
        
        if (isalpha(text[i])) 
        {
            if (isupper(text[i]))
            {
                c = (text[i] - 'A' + key) % 26;
                c = (c + 'A');
                printf("%c", c);
            }
            else if (islower(text[i]))
            {
                c = (text[i] - 'a' + key) % 26;
                c = (c + 'a');
                printf("%c", c);
            } 
        } 
        else 
        {
            printf("%c", text[i]);
        }
    }
    printf("\n");
}

int shift(char c)
{
    if (isupper(c))
    {
        shifted = (c - 'A');
        return shifted;
    }
    else if (islower(c))
    {
        shifted = (c - 'a');
        return shifted;
    }
    return 1;
}
