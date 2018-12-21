static int r0, r1, r2, r3, r4, r5;

#include <stdio.h>

int main(int argc, char *argv[])
{
    r0 = r1 = r2 = r3 = r4 = r5 = 0;
    r0 = 975;
    for(;;r1++)
    switch (r1) {
    case 0: r4 = 123; break;
    case 1: r4 = r4 & 456; break;
    case 2: r4 = r4 == 72 ? 1 : 0; break;
    case 3: r1 = r4 + r1; break;
    case 4: r1 = 0; break;
    case 5: r4 = 0; break;
    case 6: r3 = r4 | 65536; break;
    case 7: r4 = 16098955; break;
    case 8: r5 = r3 & 255; break;
    case 9: r4 = r4 + r5; break;
    case 10: r4 = r4 & 16777215; break;
    case 11: r4 = r4 * 65899; break;
    case 12: r4 = r4 & 16777215; break;
    case 13: r5 = 256 > r3 ? 1 : 0; break;
    case 14: r1 = r5 + r1; break;
    case 15: r1 = r1 + 1; break;
    case 16: r1 = 27; break;
    case 17: r5 = 0; break;
    case 18: r2 = r5 + 1; break;
    case 19: r2 = r2 * 256; break;
    case 20: r2 = r2 > r3 ? 1 : 0; break;
    case 21: r1 = r2 + r1; break;
    case 22: r1 = r1 + 1; break;
    case 23: r1 = 25; break;
    case 24: r5 = r5 + 1; break;
    case 25: r1 = 17; break;
    case 26: r3 = r5; break;
    case 27: r1 = 7; break;
    case 28: r5 = r4 == r0 ? 1 : 0; break;
    case 29: r1 = r5 + r1; break;
    case 30: r1 = 5; break;
    default: printf("[%d,%d,%d,%d,%d,%d]\n", r0, r1, r2, r3, r4, r5); return 0;
    }
}
