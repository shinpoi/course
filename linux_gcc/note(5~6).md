## 5.ストリームに関わるシステムコール

### 5-1.
fd: file descriptor（int, カーネルからプロセスに提供したストリームの番号）

### 5-3.
標準入出力：  
0　STDIN_FILENO　  
1　STDOUT_FILENO　  
2　STDERR_FILENO　  

### 5-4.
```c
ssize_t read(int fd, void *buf, size_t bufsize);
// success: return number of bytes be read
// error: -1

// size_t は int や long
// ssize_t = signed size_t

ssize_t write(int fd, const void *buf, size_t bufsize);
// success: return number of bytes be written
// error: -1
```

### 5-5.

```c
int open(const char *path, int flags);
int open(const char *path, int flags, mode_t mode);
// success: return fd
// flags: O_RDONLY, O_WRONLY, O_RDWR
// mode(if write, 複数可): O_CREAT, O_EXCL, O_TRUNC, O_APPEND

int close(int fd);
```

### 5-6. errno
一般的に、システムコールが失敗した時は失敗した原因を表す定数がグローバル変数errnoにセットされます。

### 5-7.
```c
// fdにはファイルオフセットがあります
off_t lseek(int fd, off_t offset, int whence);
// whence: SEEK_SET, SEEK_CUR, SEEK_END
// lseek = long seek, off_t = long int

int dup(int oldfd);
int dup2(int oldfd, int newfd);

int ioctl(int fd, unsigned log request, ...);
// 「...」は可変長引数

int fcntl(int fd, int cmd, ...);
```

## 6.ストリームに関わるライブラリ関数

### 6-1.
stdio: standard I/O library

stdioレベルの変数型: FILE（buffer内蔵）

fd　正式名　stdio変数  
0　STDIN_FILENO　stdin  
1　STDOUT_FILENO　stdout  
2　STDERR_FILENO　stderr  

```c
FILE *fopen(const char *path, const char *mode);
// mode: r, w, a, r+(rw), w+, a+

int fclose(FILE *stream);
```

### 6-2.
```c
int fgetc(FILE *stream);
int fputc(int c, FILE *stream);
// getc = fgetc
// putc = fputc

int getchar();
int putchar(int c);
// get from stdin / put to stdout

int ungetc(int c, FILE *stream);
```

### 6-4.
```c
char *fgets(char *buf, int size, FILE *stream);
// read one line (read until '\n, \0' or full of buffer)

char *gets(char *buf);
// overflowの恐れがあり、勧めしない

fputs(const char *buf, FILE *stream);
int puts(const char *buf);

int printf(const char *fmt, ...);
int fprintf(FILE *stream, const char *fmt, ...);
// 可能な問題：
// fgets(buf, sizeof buf, stdin);
// printf(buf);
// もしbufに「%」を含まれていましたなら、致命的な問題が起こるかもしれない

// scanfもoverflowの原因で勧めしない
```

### 6-6.
stdioレベルのファイルオフセット操作：

```c
int fseek(FILE *stream, long offset, int whence);
int fseek(FILE *stream, off_t offset, int whence);
// x86: long: 32bit, off_t 64bit
// x64: long, off_t: 64bit

long ftell(FILE *stream);
off_t ftello(FILE *stream);
// return offset

void rewind(FILE *stream);
// set offset -> 0
```

### 6-7.

```c
int fileno(FILE *stream);
// return fd

FILE *fdopen(int fd, const char *mode);
// return wrapped fd
```

### 6-8.

```c
int fflush(FILE *stream);

int setvbuf(FILE *stream, char *buf, int mode, size_t size);
```
