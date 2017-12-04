#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

static void do_cat(const char *path);
static void kill(const char *s);

int main(int argc, char *argv[]){
    int i;
    // printf("stderr: %d; STDERR_FILENO: %d\n", stderr, STDERR_FILENO);
    if (argc<2){
        fprintf(stderr, "%s: file name not given\n", argv[0]);
        exit(1);
    }
    for (i=1; i<argc; i++){
        do_cat(argv[i]);
    }
    exit(0);
}

# define BUFFER_SIZE 4096

static void do_cat(const char *path){
    int fd;
    int n;
    unsigned char buf[BUFFER_SIZE];
    // printf("sizeof buff: %d\n", sizeof buf);

    fd = open(path, O_RDONLY); // fd=fd of files, if success
    // printf("fd: %d", fd);
    // printf("O_RDONLY: %d\n", O_RDONLY);
    if (fd<0) kill(path);
    while(1){
        n = read(fd, buf, sizeof buf); // fd = 0 = stdin
        if(n<0) kill(path); // failed to read
        if(n==0) break; // read finished
        if(write(STDOUT_FILENO, buf, n) < 0) kill(path); // failed to write
    }
    if (close(fd)<0) kill(path); // failed to close stdin
}

static void kill(const char *s){
    perror(s);
    exit(1);
}
