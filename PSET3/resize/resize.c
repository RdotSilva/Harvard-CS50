// Resizes a bmp file by a value of n

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // Check if 4 arguments are provided to command line.
    if (argc != 4)
    {
        fprintf(stderr, "Usage: resize n infile outfile\n");
        return 1;
    }

    // Resize value entered by user as the 2nd argument.
    int n = atoi(argv[1]);

    // Check if resize value is between 1-100
    if (n < 0 || n > 100)
    {
        printf("Resize value must be between 1-100");
        return 1;
    }

    // Initialize file names
    char *infile = argv[2];
    char *outfile = argv[3];

    // Open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // Open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // Read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // Read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // Ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // Create outfile bf and bi
    BITMAPFILEHEADER out_bf = bf;
    BITMAPINFOHEADER out_bi = bi;

    // Set outfile height/width based on n.
    out_bi.biWidth *= n;
    out_bi.biHeight *= n;

    // Determine in and out padding.
    int in_padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int out_padding = (4 - (out_bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // Image size calculated using new padding (includes pixels and padding)
    out_bi.biSizeImage = ((sizeof(RGBTRIPLE) * out_bi.biWidth) + out_padding) * abs(out_bi.biHeight);

    // Total file size in bytes (including pixels, padding, and headers)
    out_bf.bfSize = (out_bi.biSizeImage + 54);

    // Write new outfile's BITMAPFILEHEADER
    fwrite(&out_bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // Write new outfile's BITMAPINFOHEADER
    fwrite(&out_bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // Iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        for (int j = 0; j < n; j++)
        {
            // Set pointer to the start of the line
            fseek(inptr, 54 + (bi.biWidth * 3 + in_padding) * i, SEEK_SET);

            // Iterate over the pixels in scanline
            for (int k = 0; k < bi.biWidth; k++)
            {
                // Temp storage
                RGBTRIPLE triple;

                // Read RGP triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                // Iterate each pixel n times
                for (int l = 0; l < n; l++)
                {
                    // Write RGB triple to outfile
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            // Add padding back to outfile
            for (int m = 0; m < out_padding; m++)
            {
                fputc(0x00, outptr);
            }
        }
    }
    // Close infile
    fclose(inptr);

    // Close outfile
    fclose(outptr);

    return 0;
}