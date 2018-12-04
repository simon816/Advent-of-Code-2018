/**
 *  Solution using the Minecraft Command Block Assembly project: https://github.com/simon816/Command-Block-Assembly
 */
#include <stdio.h>
#include <mclib.h>

// pretty much copy+paste from hdd_driver.c
int mar;
int mbr;

int __hdd_addr;
int __hdd_mul;

#define MEM_SIZE_X 64
#define MEM_SIZE_Z 64

#define WORD_SIZE 8

#define MEM_LOCATION 0 65 0

void memory_seek() {
    while (__hdd_addr--) {
        CMD(execute as @e[tag=mem_ptr] at @s run tp @s ~1 ~ ~);
    }

    __hdd_addr = mar;
    __hdd_addr %= MEM_SIZE_Z;

    while (__hdd_addr--) {
        CMD(execute as @e[tag=mem_ptr] at @s run tp @s ~ ~ ~1);
    }
}

void read_mem() {
    CMD(summon armor_stand MEM_LOCATION {Tags:["mem_ptr"], NoGravity:1b, Marker: 1b});
    __hdd_addr = mar;
    mbr = 0;
    __hdd_addr /= MEM_SIZE_X;
    memory_seek();
    __hdd_addr = WORD_SIZE;
    __hdd_mul = 1;

    while (__hdd_addr--) {
        if(TEST_CMD(execute at @e[tag=mem_ptr] if block ~ ~ ~ stone)) {
            mbr += __hdd_mul;
        }
        __hdd_mul *= 2;
        CMD(execute as @e[tag=mem_ptr] at @s run tp @s ~ ~1 ~);
    }
    CMD(kill @e[tag=mem_ptr]);
}

int number;

void read_number()
{
    static int inval;
    number = 0;
    while (1) {
        read_mem();
        mar++;
        if (mbr == 10) break;
        inval = mbr - 48;
        number *= 10;
        number += inval;
    }
    // printf("Read %d", number);
}

#define PLUS 43

#define READ_SIGN 0
#define ADD_VALUE 1
#define SUB_VALUE 2

void main()
{
    static int value = 0;
    static int state = READ_SIGN;
    static int nobreak = 1;
    mar = 0;
    while (nobreak) {
        switch (state) {
            case READ_SIGN:
                read_mem();
                mar++;
                if (mbr == 0) {
                    nobreak = 0; // no support for break to label
                    break;
                }
                if (mbr == PLUS) state = ADD_VALUE;
                else state = SUB_VALUE;
                break;
            case ADD_VALUE:
                read_number();
                value += number;
                state = READ_SIGN;
                break;
            case SUB_VALUE:
                read_number();
                value -= number;
                state = READ_SIGN;
                break;
        }
    }
    printf("Result = %d", value);
}
