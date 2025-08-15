#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <string.h>
#include <sys/wait.h>


struct shared{
	char sel[100];
	int b;
};

int main(){

	key_t key = ftok("shmfile", 213045);
	int shmid = shmget(key, sizeof(struct shared), 0666|IPC_CREAT);
	struct shared *ptr = (struct shared*) shmat(shmid, NULL, 0);


	int pipefd[2];
	pipe(pipefd);
	
	printf("Provide Your Input From Given Options:\n");
	printf("1. Type a to Add Money\n");
	printf("2. Type w to Withdraw Money\n");
	printf("3. Type c to Check Balance.\n\n");
	
	char input;
	
	scanf(" %c", &input);
	(*ptr).b = 1000;
	(*ptr).sel[0] = input;
	(*ptr).sel[1] = '\0';
	
	printf("Your selection: %c\n\n", input);
	
	pid_t pid = fork();
	
	if (pid == 0){
		if (input == 'a'){
			int amount;
			printf("Enter amount to be added:\n");
			scanf("%d", &amount);
			
			if (amount > 0){
				(*ptr).b += amount;
				printf("Balance added successfully\n");
				printf("Updated balance after addition: %d\n", (*ptr).b);
			}
			
			else{
				printf("Adding failed, Invalid amount\n");
			}
		}
		
		else if (input == 'w'){
			int amount;
			printf("Enter amount to be withdrawn:\n");
			scanf("%d", &amount);
			if (amount > 0 && amount < (*ptr).b){
				(*ptr).b -= amount;
				printf("Balance withdrawn successfully\n");
				printf("Updated balance after withdrawal: %d\n", (*ptr).b);
			}
			
			else{
				printf("Withdrawal failed, Invalid amount\n");
			}
		}
		
		else if (input == 'c'){
			printf("Your current balance is %d\n", (*ptr).b);
		}
		
		else{
			printf("Invalid selection\n");
		}
		
		char msg[] = "Thank you for using\n";
		
		write(pipefd[1], msg, strlen(msg) + 1);
		exit(0);
	}
	
	else{
		wait(NULL);
		char buffer[100];
		read(pipefd[0], buffer, sizeof(buffer));
		printf("%s\n", buffer);
		shmdt(ptr);
		shmctl(shmid, IPC_RMID, NULL);
	}
	return 0;	
}


