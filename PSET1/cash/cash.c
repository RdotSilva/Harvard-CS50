#include <cs50.h>
#include <stdio.h>
#include <math.h>

#define QUARTER 25
#define DIME 10
#define NICKLE 5
#define PENNY 1

float get_change(string prompt);

int main(void)
{
    int coins = 0;
    
    float change = get_change("How much change: ");

    int rounded = round(change * 100);

    while (rounded / QUARTER > 0)
    {
        rounded = rounded - QUARTER;
        coins = coins + 1;
    }
    while (rounded / DIME > 0)
    {
        rounded = rounded - DIME;
        coins = coins + 1;
    }
    while (rounded / NICKLE > 0)
    {
        rounded = rounded - NICKLE;
        coins = coins + 1;
    }
    while (rounded / PENNY > 0)
    {
        rounded = rounded - PENNY;
        coins = coins + 1;
    }
    
    printf("%i\n", coins);
    
}

float get_change(string prompt)
{
    float f;
    do 
    {
        f = get_float("%s", prompt);
    }
    while (f < 0); 
    return f;
}