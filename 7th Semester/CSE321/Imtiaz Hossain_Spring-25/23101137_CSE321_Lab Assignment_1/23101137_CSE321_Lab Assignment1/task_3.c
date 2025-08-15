#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/mman.h>

int main(){
    int *counter = mmap(NULL, sizeof(int), PROT_READ | PROT_WRITE,
                        MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    *counter = 1;

    pid_t a, b, c, extra;
    pid_t pid = getpid();

    a = fork();
    if (a == 0){
        (*counter)++;
    }

    b = fork();
    if (b == 0){
        (*counter)++;
    }

    c = fork();
    if (c == 0){
        (*counter)++;
    }

    sleep(1);

    if (getpid() != pid){
        if (getpid() % 2 != 0){
            extra = fork();
            if (extra == 0){
                (*counter)++;
            } 
            else if (extra > 0){
                (*counter)++;
            }
        }
    }

    sleep(2);
    if (getpid() == pid){
        printf("Total processes created (including parent): %d\n", *counter);
    }

    munmap(counter, sizeof(int));
    return 0;
}
