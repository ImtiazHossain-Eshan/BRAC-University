#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <unistd.h>
#include <sys/wait.h>

struct msg{
    long int type;
    char txt[6];
};

int main(){
    key_t key = ftok("msgqueue", 213045);
    int msgid = msgget(key, 0666 | IPC_CREAT);
    struct msg message;

    char workspace[20];
    printf("Please enter the workspace name:\n");
    scanf("%s", workspace);

    if (strcmp(workspace, "cse321") != 0){
        printf("Invalid workspace name\n");
        msgctl(msgid, IPC_RMID, NULL);
        return 0;
    }

    message.type = 1;
    strcpy(message.txt, "cse321");
    msgsnd(msgid, &message, sizeof(message.txt), 0);
    printf("Workspace name sent to otp generator from log in: %s\n", message.txt);

    pid_t otp_pid = fork();
    
    if (otp_pid == 0){
        msgrcv(msgid, &message, sizeof(message.txt), 1, 0);
        printf("OTP generator received workspace name from log in: %s\n", message.txt);

        pid_t otp = getpid();
        snprintf(message.txt, sizeof(message.txt), "%d", otp);

        message.type = 2;
        msgsnd(msgid, &message, sizeof(message.txt), 0);
        printf("OTP sent to log in from OTP generator: %s\n", message.txt);

        message.type = 3;
        msgsnd(msgid, &message, sizeof(message.txt), 0);
        printf("OTP sent to mail from OTP generator: %s\n", message.txt);

        pid_t mail_pid = fork();
        
        if (mail_pid == 0){
            msgrcv(msgid, &message, sizeof(message.txt), 3, 0);
            printf("Mail received OTP from OTP generator: %s\n", message.txt);

            message.type = 4;
            msgsnd(msgid, &message, sizeof(message.txt), 0);
            printf("OTP sent to log in from mail: %s\n", message.txt);
            exit(0);
        }
        
        else{
            wait(NULL);
            exit(0);
        }
    }
    
    else{
        wait(NULL);
        struct msg r1, r2;

        msgrcv(msgid, &r1, sizeof(r1.txt), 2, 0);
        printf("Log in received OTP from OTP generator: %s\n", r1.txt);

        msgrcv(msgid, &r2, sizeof(r2.txt), 4, 0);
        printf("Log in received OTP from mail: %s\n", r2.txt);

        if (strcmp(r1.txt, r2.txt) == 0){
            printf("OTP Verified\n");
        }
        
        else {
            printf("OTP Incorrect\n");
        }

        msgctl(msgid, IPC_RMID, NULL);
    }

    return 0;
}

