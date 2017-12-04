# include <stdio.h>
# include <stdlib.h>
# include <errno.h>


/*
// original (IO by byte)
int main(int argc, char *argv[]){
    int i;
    for(i=1; i<argc; i++){
        FILE *f;
        int c;

        f = fopen(argv[i], "r"); // failed: NULL
        if(!f){
            perror(argv[i]);
            exit(1);
        }
        while((c=fgetc(f)) != EOF){
            if (putchar(c) < 0) exit(1);
        }
        fclose(f);
    }
    exit(0);
}
*/


// by buffer
int main(int argc, char *argv[]){
    int i;
    for(i=1; i<argc; i++){
        FILE *f;
        char buf[1024];

        f = fopen(argv[i], "r"); // failed: NULL
        if(!f){
            perror(argv[i]);
            exit(1);
        }
        while(fgets(buf, sizeof buf, f)){
            // puts("read line! \n");
            // printf("struct of f: fd:%d, flags:%d\n", (*f)._fileno, (*f)._flags);
            if (fputs(buf, stdout) == EOF){ // success: >0; failed: EOF;
                perror("fputs() error!");
                exit(1);
            }
        }
        // printf("[break] struct of f: fd:%d, flags:%d\n", (*f)._fileno, (*f)._flags);
        // printf("break-feof(): %d\n", feof(f));
        fclose(f);
    }
    exit(0);
}
