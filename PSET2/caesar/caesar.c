#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        return 1;
    }
    
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (!isdigit(argv[1][i]))
        {
            return 1;
        }
    }
    
    int key = atoi(argv[1]);
    int c;
    
    string text = get_string("plaintext: ");
    
    printf("ciphertext: ");
    
    for (int i = 0; i < strlen(text); i++)
    {
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
