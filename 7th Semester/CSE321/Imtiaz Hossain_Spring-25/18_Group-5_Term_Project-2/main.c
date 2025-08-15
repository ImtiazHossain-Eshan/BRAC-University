#include "superblock.h"
#include "inode_bitmap.h"
#include "data_blocks.h"

int main(int argc, char *argv[]){
    if (argc != 2){
        fprintf(stderr, "Usage: %s <vsfs.img>\n", argv[0]);
        return 1;
    }

    FILE *img = fopen(argv[1], "rb");
    
    if (!img){
        perror("Failed to open image file");
        return 1;
    }

    Superblock sb;
    
    if (!read_superblock(img, &sb)){
        fclose(img);
        return 1;
    }
    
    validate_superblock(&sb);

    uint8_t inode_bitmap[BLOCK_SIZE];
    read_bitmap(img, INODE_BITMAP_BLOCK, inode_bitmap);
    check_inode_bitmap(img, inode_bitmap, sb.inode_count);

    uint8_t data_bitmap[BLOCK_SIZE];
    read_bitmap(img, DATA_BITMAP_BLOCK, data_bitmap);
    check_data_blocks(img, inode_bitmap, data_bitmap, sb.inode_count);

    fclose(img);
    return 0;
    
    
}
