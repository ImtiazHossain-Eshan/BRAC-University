#include "shell.h"

void tokenize_input(char *input, char **tokens) {
    int idx = 0;
    tokens[idx] = strtok(input, " \t\r\n");
    while (tokens[idx] != NULL) {
        tokens[++idx] = strtok(NULL, " \t\r\n");
    }
    tokens[idx] = NULL;
}

int run_command(char *cmd) {
    char *args[MAX_TOKENS];
    tokenize_input(cmd, args);
    if (args[0] == NULL) return 1;

    if (strcmp(args[0], "history") == 0) {
        show_history();
        return 1;
    }

    if (strcmp(args[0], "cd") == 0) {
        if (args[1] == NULL) {
            fprintf(stderr, "cd: missing argument\n");
        } else {
            if (chdir(args[1]) != 0) {
                perror("cd failed");
                return 0;
            }
        }
        return 1;
    }

    pid_t pid = fork();
    if (pid == 0) {
        redirect_handler(args);
        execvp(args[0], args);
        perror("execvp");
        exit(1);
    } else {
        int status;
        waitpid(pid, &status, 0);
        return WIFEXITED(status) && WEXITSTATUS(status) == 0;
    }
}
