#include <cs50.h>
#include <stdio.h>
#include <math.h>

float get_change(string prompt);

int main(void)
{
    int coins, quarter, dime, nickle, penny;
    coins = 0;
    quarter = 25;
    dime = 10;
    nickle = 5;
    penny = 1;
    
    float change = get_change("How much change: ");

    int rounded = round(change * 100);

    while (rounded / quarter > 0)
    {
        rounded = rounded - quarter;
        coins = coins + 1;
    }
    while (rounded / dime > 0)
    {
        rounded = rounded - dime;
        coins = coins + 1;
    }
    while (rounded / nickle > 0)
    {
        rounded = rounded - nickle;
        coins = coins + 1;
    }
    while (rounded / penny > 0)
    {
        rounded = rounded - penny;
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