#include <cs50.h>
#include <stdio.h>

int get_height(string prompt);

void print_hash(void);
void print_space(void);
void print_newline(void);

int main(void)
{
    int height = get_height("Enter a number between 1 and 8: ");
    int x, y, z;

    for (x = 1; x <= height; x ++)
    {
        for (y = 0 ; y < height - x; y ++)
        {
            printf(" ");
        }
        for (z = 0; z < height - y; z ++)
        {
            printf("#");
        }
        printf("\n");
    }
}

int get_height(string prompt)
{
    int n;
    do
    {
        n = get_int("%s", prompt);
    }
    while (n < 1 || n > 8);
    return n;
}