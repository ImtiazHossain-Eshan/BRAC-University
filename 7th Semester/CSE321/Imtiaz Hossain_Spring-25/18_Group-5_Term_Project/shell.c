#include "shell.h"

char *cmd_history[MAX_HISTORY];
int history_index = 0;

void handle_signal(int sig) {
    write(STDOUT_FILENO, "\nsh> ", 5);
    fflush(stdout);
}

void save_history(const char *input) {
    if (history_index < MAX_HISTORY) {
        cmd_history[history_index++] = strdup(input);
    }
}

void show_history() {
    for (int i = 0; i < history_index; ++i) {
        printf("%d: %s\n", i + 1, cmd_history[i]);
    }
}

void handle_sequential(char *input) {
    char *semicolon_cmd;
    char *semi_ptr;
    semicolon_cmd = strtok_r(input, ";", &semi_ptr);

    while (semicolon_cmd != NULL) {
        char *and_cmd;
        char *and_ptr;
        and_cmd = strtok_r(semicolon_cmd, "&&", &and_ptr);

        int exec_success = 1;
        while (and_cmd != NULL && exec_success) {
            if (strchr(and_cmd, '|')) {
                execute_pipeline(and_cmd);
            } else {
                exec_success = run_command(and_cmd);
            }
            and_cmd = strtok_r(NULL, "&&", &and_ptr);
        }
        semicolon_cmd = strtok_r(NULL, ";", &semi_ptr);
    }
}

int main() {
    char buffer[MAX_BUFFER];
    signal(SIGINT, handle_signal);

    while (1) {
        printf("sh> ");
        if (!fgets(buffer, MAX_BUFFER, stdin)) break;
        if (strlen(buffer) <= 1) continue;

        buffer[strcspn(buffer, "\n")] = '\0';

        if (strcmp(buffer, "exit") == 0) break;

        save_history(buffer);
        handle_sequential(buffer);
    }

    return 0;
}
