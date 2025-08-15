#ifndef INODE_BITMAP_H
#define INODE_BITMAP_H

#include "superblock.h"

#define INODES_PER_BLOCK (BLOCK_SIZE / INODE_SIZE)

void read_bitmap(FILE *img, uint32_t block_num, uint8_t *bitmap);
bool is_inode_bit_set(const uint8_t *bitmap, int inode_num);
void read_inode(FILE *img, int inode_num, uint8_t *inode_data);
void check_inode_bitmap(FILE *img, const uint8_t *inode_bitmap, int total_inodes);

#endif
