#include <cstdio>
#include <set>

static int r0, r1, r2, r3, r4, r5;

int main(int argc, char *argv[]) {
    r0 = r1 = r2 = r3 = r4 = r5 = 0;
    
    std::set<int> seen;
    int prev = 0;

    start:
    r4 = 0;

    loop:
    r3 = r4 | 65536;
    r4 = 16098955;
    for(;;r3 /= 256) {
        r4 = (((r4 + (r3 & 255)) & 0xffffff) * 65899) & 0xffffff;
        if (r3 < 256) {
            if (seen.find(r4) != seen.end()) {
                printf("Prev=%d, r4=%d", prev, r4);
                return 0;
            }
            seen.insert(r4);
            prev = r4;
            if (r4 == r0) break;
            else goto loop;
        }
    }
    printf("[%d,%d,%d,%d,%d,%d]\n", r0, r1, r2, r3, r4, r5);
    return 0;
}
