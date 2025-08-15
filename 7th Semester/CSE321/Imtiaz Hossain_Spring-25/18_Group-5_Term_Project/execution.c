#include "shell.h"

int redirect_handler(char **tokens) {
    for (int i = 0; tokens[i]; ++i) {
        if (strcmp(tokens[i], ">") == 0) {
            int fd = open(tokens[i + 1], O_WRONLY | O_CREAT | O_TRUNC, 0644);
            dup2(fd, STDOUT_FILENO);
            close(fd);
            tokens[i] = NULL;
        } else if (strcmp(tokens[i], ">>") == 0) {
            int fd = open(tokens[i + 1], O_WRONLY | O_CREAT | O_APPEND, 0644);
            dup2(fd, STDOUT_FILENO);
            close(fd);
            tokens[i] = NULL;
        } else if (strcmp(tokens[i], "<") == 0) {
            int fd = open(tokens[i + 1], O_RDONLY);
            dup2(fd, STDIN_FILENO);
            close(fd);
            tokens[i] = NULL;
        }
    }
    return 0;
}

void execute_pipeline(char *line) {
    char *cmds[20];
    int count = 0;
    cmds[count++] = strtok(line, "|");

    while ((cmds[count++] = strtok(NULL, "|")) != NULL);

    int fd[2], in_fd = 0;

    for (int i = 0; i < count - 1; ++i) {
        pipe(fd);
        if (fork() == 0) {
            dup2(in_fd, 0);
            if (i != count - 2) dup2(fd[1], 1);
            close(fd[0]);

            char *args[MAX_TOKENS];
            tokenize_input(cmds[i], args);
            redirect_handler(args);
            execvp(args[0], args);
            perror("execvp");
            exit(1);
        } else {
            wait(NULL);
            close(fd[1]);
            in_fd = fd[0];
        }
    }
}
