#include "lfs/lfs.h"
typedef lfs_file_t file_t;

int mount();
int unmount();
file_t* open_file(const char *path, const char *mode);
int close_file(file_t *file);
int read_file(file_t *file, void *buffer, size_t size);
int write_file(file_t *file, const void *buffer, size_t size);
int seek_file(file_t *file, int offset);
int seek_file_end(file_t *file);
int seek_file_rel(file_t *file, int offset);
int seek_file_begin(file_t *file);
int tell_file(file_t *file);
int remove_file(const char *path);
int rename_file(const char *old_path, const char *new_path);
int make_dir(const char *path);
int remove_dir(const char *path);
int read_dir(const char *path, char *buffer, size_t size);


