

#include "pico/stdlib.h"
#include "pico/binary_info.h"

#include "hardware/flash.h"
#include "hardware/sync.h"

#include "lfs/lfs.h"

#include "file_system.hpp"
// Define the flash sizes
// This is setup to read a block of the flash from the end 
#define BLOCK_SIZE_BYTES (FLASH_SECTOR_SIZE)
#define HW_FLASH_STORAGE_BYTES  (1408 * 1024)
#define HW_FLASH_STORAGE_BASE   (PICO_FLASH_SIZE_BYTES - HW_FLASH_STORAGE_BYTES) // 655360

int pico_read(const struct lfs_config *c, lfs_block_t block, lfs_off_t off, void *buffer, lfs_size_t size)
{
    uint32_t fs_start = XIP_BASE + HW_FLASH_STORAGE_BASE;
    uint32_t addr = fs_start + (block * c->block_size) + off;
    
    // printf("[FS] READ: %p, %d\n", addr, size);
    
    memcpy(buffer, (unsigned char *)addr, size);
    return 0;
}

int pico_prog(const struct lfs_config *c, lfs_block_t block, lfs_off_t off, const void *buffer, lfs_size_t size)
{
    uint32_t fs_start = HW_FLASH_STORAGE_BASE;
    uint32_t addr = fs_start + (block * c->block_size) + off;
    
    // printf("[FS] WRITE: %p, %d\n", addr, size);
        
    uint32_t ints = save_and_disable_interrupts();
    flash_range_program(addr, (const uint8_t *)buffer, size);
    restore_interrupts(ints);
    
    return 0;
}

int pico_erase(const struct lfs_config *c, lfs_block_t block)
{           
    uint32_t fs_start = HW_FLASH_STORAGE_BASE;
    uint32_t offset = fs_start + (block * c->block_size);
    
    // printf("[FS] ERASE: %p, %d\n", offset, block);
        
    uint32_t ints = save_and_disable_interrupts();   
    flash_range_erase(offset, c->block_size);  
    restore_interrupts(ints);
    
    return 0;
}

int pico_sync(const struct lfs_config *c)
{
    return 0;
}

// configuration of the filesystem is provided by this struct
const struct lfs_config PICO_FLASH_CFG = {
    // block device operations
    .read  = &pico_read,
    .prog  = &pico_prog,
    .erase = &pico_erase,
    .sync  = &pico_sync,

    // block device configuration
    .read_size = FLASH_PAGE_SIZE, // 256
    .prog_size = FLASH_PAGE_SIZE, // 256
    
    .block_size = BLOCK_SIZE_BYTES, // 4096
    .block_count = HW_FLASH_STORAGE_BYTES / BLOCK_SIZE_BYTES, // 352
    .block_cycles = 500, // 500
    
    .cache_size = FLASH_PAGE_SIZE, // 256
    .lookahead_size = FLASH_PAGE_SIZE,   // 256    
};

// littlefs instance
lfs_t lfs;

int mount() {
    // mount the filesystem
    int err = lfs_mount(&lfs, &PICO_FLASH_CFG);
    if (err) {
        // reformat if we can't mount the filesystem
        // this should only happen on the first boot
        lfs_format(&lfs, &PICO_FLASH_CFG);
        err = lfs_mount(&lfs, &PICO_FLASH_CFG);
    }
    return err;
}

int unmount() {
    // unmount to release any resources we were using
    return lfs_unmount(&lfs);
}

int mode_to_flags(const char *mode) {
    int flags = LFS_O_CREAT;
    if(mode[0] == 'r') {
        flags |= LFS_O_RDONLY;
    } else if(mode[0] == 'w') {
        flags |= LFS_O_WRONLY;
    } else if(mode[0] == 'a') {
        flags |= LFS_O_WRONLY | LFS_O_APPEND;
    }
    if(mode[1] == '+') {
        flags |= LFS_O_RDWR;
    }
    return flags;
}

file_t* open_file(const char *path, const char *mode) {
    file_t *file = (file_t *)malloc(sizeof(file_t));
    int err = lfs_file_open(&lfs, file, path, mode_to_flags(mode));
    if(err < 0) {
        free(file);
        return nullptr;
    } 
    return file;
}

int close_file(file_t *file) {
    int result = lfs_file_close(&lfs, file);
    free(file);
    return result;
}

int read_file(file_t *file, void *buffer, size_t size) {
    return lfs_file_read(&lfs, file, buffer, size);
}

int write_file(file_t *file, const void *buffer, size_t size) {
    return lfs_file_write(&lfs, file, buffer, size);
}

int seek_file(file_t *file, int offset) {
    return lfs_file_seek(&lfs, file, offset, LFS_SEEK_SET);
}

int seek_file_end(file_t *file) {
    return lfs_file_seek(&lfs, file, 0, LFS_SEEK_END);
}

int seek_file_rel(file_t *file, int offset) {
    return lfs_file_seek(&lfs, file, offset, LFS_SEEK_CUR);
}

int seek_file_begin(file_t *file) {
    return lfs_file_seek(&lfs, file, 0, LFS_SEEK_SET);
}

int tell_file(file_t *file) {
    return lfs_file_tell(&lfs, file);
}

int remove_file(const char *path) {
    return lfs_remove(&lfs, path);
}

int rename_file(const char *old_path, const char *new_path) {
    return lfs_rename(&lfs, old_path, new_path);
}

int make_dir(const char *path) {
    return lfs_mkdir(&lfs, path);
}

int remove_dir(const char *path) {
    return lfs_remove(&lfs, path);
}

int read_dir(const char *path, char *buffer, size_t size) {
    lfs_dir_t dir;
    int err = lfs_dir_open(&lfs, &dir, path);
    if(err < 0) {
        return err;
    }
    int count = 0;
    while(true) {
        struct lfs_info info;
        err = lfs_dir_read(&lfs, &dir, &info);
        if(err < 0) {
            return err;
        }
        if(!err) {
            break;
        }
        if(count + strlen(info.name) + 1 > size) {
            return -1;
        }
        strcpy(buffer + count, info.name);
        count += strlen(info.name);
        buffer[count] = '\n';
        count++;
    }
    return count;
}
