#ifndef SUPERBLOCK_H
#define SUPERBLOCK_H

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#define BLOCK_SIZE 4096
#define TOTAL_BLOCKS 64
#define INODE_BITMAP_BLOCK 1
#define DATA_BITMAP_BLOCK 2
#define INODE_TABLE_START 3
#define FIRST_DATA_BLOCK 8
#define INODE_SIZE 256

#define MAGIC_OFFSET 0
#define BLOCK_SIZE_OFFSET 2
#define TOTAL_BLOCKS_OFFSET 6
#define INODE_BITMAP_BLOCK_OFFSET 0xA
#define DATA_BITMAP_BLOCK_OFFSET 0xE
#define INODE_TABLE_START_OFFSET 0x12
#define FIRST_DATA_BLOCK_OFFSET 0x16
#define INODE_SIZE_OFFSET 0x1A
#define INODE_COUNT_OFFSET 0x1E

typedef struct{
    uint16_t magic;
    uint32_t block_size;
    uint32_t total_blocks;
    uint32_t inode_bitmap_block;
    uint32_t data_bitmap_block;
    uint32_t inode_table_start;
    uint32_t first_data_block;
    uint32_t inode_size;
    uint32_t inode_count;
} Superblock;

uint16_t read_uint16_le(const uint8_t *p);
uint32_t read_uint32_le(const uint8_t *p);

void check_fread(void *ptr, size_t size, FILE *stream);
void check_fseek(FILE *stream, long offset, int origin);

bool read_superblock(FILE *img, Superblock *sb);
void validate_superblock(const Superblock *sb);

#endif
