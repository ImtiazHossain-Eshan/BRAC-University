#ifndef DATA_BLOCKS_H
#define DATA_BLOCKS_H

#include "inode_bitmap.h"

#define MAX_DATA_BLOCKS 56

void collect_blocks(FILE *img, const uint8_t *inode_data, uint32_t *blocks, int *count);
void check_data_blocks(FILE *img, const uint8_t *inode_bitmap, const uint8_t *data_bitmap, int total_inodes);

#endif
