#include "superblock.h"
#include <stdlib.h>

void check_fread(void *ptr, size_t size, FILE *stream){
    if (fread(ptr, size, 1, stream) != 1){
        perror("fread failed");
        exit(EXIT_FAILURE);
    }
}

void check_fseek(FILE *stream, long offset, int origin){
    if (fseek(stream, offset, origin) != 0){
        perror("fseek failed");
        exit(EXIT_FAILURE);
    }
}

uint16_t read_uint16_le(const uint8_t *p){
    return p[0] | (p[1] << 8);
}

uint32_t read_uint32_le(const uint8_t *p){
    return p[0] | (p[1] << 8) | (p[2] << 16) | (p[3] << 24);
}

bool read_superblock(FILE *img, Superblock *sb){
    uint8_t block[BLOCK_SIZE];
    check_fread(block, BLOCK_SIZE, img);

    sb->magic = read_uint16_le(block + MAGIC_OFFSET);
    sb->block_size = read_uint32_le(block + BLOCK_SIZE_OFFSET);
    sb->total_blocks = read_uint32_le(block + TOTAL_BLOCKS_OFFSET);
    sb->inode_bitmap_block = read_uint32_le(block + INODE_BITMAP_BLOCK_OFFSET);
    sb->data_bitmap_block = read_uint32_le(block + DATA_BITMAP_BLOCK_OFFSET);
    sb->inode_table_start = read_uint32_le(block + INODE_TABLE_START_OFFSET);
    sb->first_data_block = read_uint32_le(block + FIRST_DATA_BLOCK_OFFSET);
    sb->inode_size = read_uint32_le(block + INODE_SIZE_OFFSET);
    sb->inode_count = read_uint32_le(block + INODE_COUNT_OFFSET);

    return true;
}

void validate_superblock(const Superblock *sb){

    bool valid = true;
    
    if (sb->magic != 0xD34D){
        printf("Invalid magic number: 0x%04X\n", sb->magic);
        valid = false;
    }
    
    if (sb->block_size != 4096){
        printf("Invalid block size: %u\n", sb->block_size);
        valid = false;
    }
    
    if (sb->total_blocks != 64){
        printf("Invalid total blocks: %u\n", sb->total_blocks);
        valid = false;
    }
    
    if (sb->inode_bitmap_block != 1){
        printf("Invalid inode bitmap block: %u\n", sb->inode_bitmap_block);
        valid = false;
    }
    
    if (sb->data_bitmap_block != 2){
        printf("Invalid data bitmap block: %u\n", sb->data_bitmap_block);
        valid = false;
    }
    
    if (sb->inode_table_start != 3){
        printf("Invalid inode table start block: %u\n", sb->inode_table_start);
        valid = false;
    }
    
    if (sb->first_data_block != 8){
        printf("Invalid first data block: %u\n", sb->first_data_block);
        valid = false;
    }
    
    if (sb->inode_size != 256){
        printf("Invalid inode size: %u\n", sb->inode_size);
        valid = false;
    }
    
    uint32_t expected_inode_count = (5 * BLOCK_SIZE) / sb->inode_size;
    
    if (sb->inode_count != expected_inode_count){
        printf("Invalid inode count: %u (expected %u)\n", sb->inode_count, expected_inode_count);
        valid = false;
    }
    
    if (valid){
        printf("Superblock is valid.\n");
    } 
    
    else{
        printf("Superblock has errors.\n");
    }
}
