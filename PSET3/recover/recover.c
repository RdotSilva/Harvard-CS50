#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>

int main(int argc, char *argv[])
{
    // Check if 2 arguments are provided to command line.
    if (argc != 2)
    {
        fprintf(stderr, "Enter file name to recover");
        return 1;
    }

    // Remember infile name for memory card file.
    char *infile = argv[1];

    // Open memory card file.
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // Initialize image file.
    FILE *img = NULL;

    // Initialize jpeg found to false to start.
    bool jpeg_found = false;

    // Filename array
    char filename[8];

    // Count the number of jpegs found.
    int file_counter = 0;

    // Array for buffer 512 bytes.
    unsigned char buffer[512];

    // Repeat this until end of the memory card.
    while ((fread(buffer, 512, 1, inptr) == 1))
    {
        // Check if block is a JPEG or not by first 4.
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // Check if we have already found a JPEG.
            if (jpeg_found)
            {
                fclose(img);
                sprintf(filename, "%03i.jpg", file_counter);
                img = fopen(filename, "w");
                file_counter++;
                fwrite(buffer, 512, 1, img);

            }
            else
                // Jpeg not already found
            {
                jpeg_found = true;
                sprintf(filename, "%03i.jpg", file_counter);
                img = fopen(filename, "w");
                fwrite(&buffer, 512, 1, img);
                file_counter++;
            }
        }
        else
        {
            if (jpeg_found)
            {
                fwrite(&buffer, 512, 1, img);
            }
        }
    }
    fclose(img);
    fclose(inptr);
}