#include "inode_bitmap.h"
#include <stdlib.h>

void read_bitmap(FILE *img, uint32_t block_num, uint8_t *bitmap){
    check_fseek(img, block_num * BLOCK_SIZE, SEEK_SET);
    check_fread(bitmap, BLOCK_SIZE, img);
}

bool is_inode_bit_set(const uint8_t *bitmap, int inode_num){
    int byte = inode_num / 8;
    int bit = inode_num % 8;
    return (bitmap[byte] & (1 << bit)) != 0;
}

void read_inode(FILE *img, int inode_num, uint8_t *inode_data){
    
    int block_num = INODE_TABLE_START + (inode_num / INODES_PER_BLOCK);
    int offset = (inode_num % INODES_PER_BLOCK) * INODE_SIZE;
    
    check_fseek(img, block_num * BLOCK_SIZE + offset, SEEK_SET);
    check_fread(inode_data, INODE_SIZE, img);
}

void check_inode_bitmap(FILE *img, const uint8_t *inode_bitmap, int total_inodes){

    bool errors = false;
    
    for (int i = 0; i < total_inodes; i++){
        if (is_inode_bit_set(inode_bitmap, i)){
            uint8_t inode_data[INODE_SIZE];
            read_inode(img, i, inode_data);
            uint32_t links = read_uint32_le(inode_data + 32);
            uint32_t del_time = read_uint32_le(inode_data + 28);
            if (links == 0 || del_time != 0){
                printf("Inode %d marked used but invalid (links=%u, del_time=%u)\n", i, links, del_time);
                errors = true;
            }
        }
    }

    for (int i = 0; i < total_inodes; i++){
        uint8_t inode_data[INODE_SIZE];
        read_inode(img, i, inode_data);
        uint32_t links = read_uint32_le(inode_data + 32);
        uint32_t del_time = read_uint32_le(inode_data + 28);
        
        if (links > 0 && del_time == 0 && !is_inode_bit_set(inode_bitmap, i)){
            printf("Inode %d valid but not marked in bitmap\n", i);
            errors = true;
        }
    }

    if (!errors) {
        printf("Inode bitmap is consistent.\n");
    }
}
