#include <stdio.h>
#include <unistd.h>
#include <signal.h>

void sigint_handler(int sig) {
    printf("\nCaught SIGINT (CTRL+C), but continuing to sleep...\n");
}

int main() {
    signal(SIGINT, sigint_handler);

    printf("Sleeping for 10 seconds. Press CTRL+C to test signal handling...\n");
    sleep(10);

    printf("Sleep complete.\n");

    return 0;
}

