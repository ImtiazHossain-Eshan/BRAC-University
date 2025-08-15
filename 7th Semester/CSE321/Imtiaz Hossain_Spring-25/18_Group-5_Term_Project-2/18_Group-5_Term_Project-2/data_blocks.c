#include "data_blocks.h"
#include <stdlib.h>

void collect_blocks(FILE *img, const uint8_t *inode_data, uint32_t *blocks, int *count){
    (void)img;
    uint32_t direct = read_uint32_le(inode_data + 40);
    
    if (direct != 0 && *count < MAX_DATA_BLOCKS){
        if (direct >= FIRST_DATA_BLOCK && direct < TOTAL_BLOCKS){
            blocks[(*count)++] = direct;
        } else {
            printf("Invalid direct block: %u\n", direct);
        }
    }

    uint32_t single_indirect = read_uint32_le(inode_data + 44);
    
    if (single_indirect >= FIRST_DATA_BLOCK && single_indirect < TOTAL_BLOCKS){
        
        uint8_t indirect_block[BLOCK_SIZE];
        
        check_fseek(img, single_indirect * BLOCK_SIZE, SEEK_SET);
        check_fread(indirect_block, BLOCK_SIZE, img);
        
        for (int i = 0; i < BLOCK_SIZE / 4; i++){
            uint32_t block = read_uint32_le(indirect_block + i * 4);
            
            if (block != 0 && *count < MAX_DATA_BLOCKS){
                if (block >= FIRST_DATA_BLOCK && block < TOTAL_BLOCKS){
                    blocks[(*count)++] = block;
                } 
                
                else{
                    printf("Invalid indirect block: %u\n", block);
                }
                
            }
        }
        
        
    } 
    
    else if (single_indirect != 0){
        printf("Invalid single indirect block: %u\n", single_indirect);
    }
}

void check_data_blocks(FILE *img, const uint8_t *inode_bitmap, const uint8_t *data_bitmap, int total_inodes){
    bool data_bitmap_errors = false;
    bool bad_blocks = false;
    bool duplicates = false;
    
    uint32_t referenced_blocks[MAX_DATA_BLOCKS] = {0};
    int ref_count = 0;
    uint8_t block_ref_count[TOTAL_BLOCKS] = {0};

    for (int i = 0; i < total_inodes; i++){
        if (!is_inode_bit_set(inode_bitmap, i)) continue;

        uint8_t inode_data[INODE_SIZE];
        read_inode(img, i, inode_data);
        uint32_t links = read_uint32_le(inode_data + 32);
        uint32_t del_time = read_uint32_le(inode_data + 28);

        if (links == 0 || del_time != 0) continue;

        uint32_t blocks[MAX_DATA_BLOCKS];
        int block_count = 0;
        collect_blocks(img, inode_data, blocks, &block_count);

        for (int j = 0; j < block_count; j++){
            uint32_t blk = blocks[j];
            
            if (blk < FIRST_DATA_BLOCK || blk >= TOTAL_BLOCKS){
                printf("Inode %d references bad block %u\n", i, blk);
                bad_blocks = true;
                continue;
            }
            
            referenced_blocks[ref_count++] = blk;
            block_ref_count[blk]++;
            
            if (block_ref_count[blk] > 1){
                printf("Block %u referenced by multiple inodes\n", blk);
                duplicates = true;
            }

            int data_bit = blk - FIRST_DATA_BLOCK;
            int data_byte = data_bit / 8;
            int data_bit_position = data_bit % 8;
            
            if ((data_bitmap[data_byte] & (1 << data_bit_position)) == 0){
                printf("Block %u referenced but not marked in data bitmap\n", blk);
                data_bitmap_errors = true;
            }
        }
        
    }

    for (int i = 0; i < MAX_DATA_BLOCKS; i++){
    
        int block_byte = i / 8;
        int block_bit = i % 8;
        
        if ((data_bitmap[block_byte] & (1 << block_bit)) != 0){
            bool found = false;
            
            for (int j = 0; j < ref_count; j++) {
                if (referenced_blocks[j] == (uint32_t)(i + FIRST_DATA_BLOCK)){
                    found = true;
                    break;
                }
            }
            
            if (!found){
                printf("Data block %u marked but not referenced\n", i + FIRST_DATA_BLOCK);
                data_bitmap_errors = true;
            }
        }
    }

    if (!data_bitmap_errors && !bad_blocks && !duplicates){
        printf("Data blocks are consistent.\n");
    }
    
}
