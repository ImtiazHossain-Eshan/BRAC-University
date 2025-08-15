#ifndef SHELL_H
#define SHELL_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <signal.h>

#define MAX_BUFFER 1024
#define MAX_TOKENS 100
#define MAX_HISTORY 100

extern char *cmd_history[MAX_HISTORY];
extern int history_index;

void handle_signal(int sig);
void save_history(const char *input);
void show_history();
void tokenize_input(char *input, char **tokens);

int redirect_handler(char **tokens);
int run_command(char *cmd);
void execute_pipeline(char *line);
void handle_sequential(char *input);

#endif
