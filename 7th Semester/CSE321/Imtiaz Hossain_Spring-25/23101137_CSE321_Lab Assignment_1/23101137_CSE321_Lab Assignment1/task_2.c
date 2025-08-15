#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>


int main(){
		
	pid_t child_pid = fork();
	
	if (child_pid < 0){
		perror("Failed to fork child");
		return 1;
	}
	
	else if (child_pid == 0){
		pid_t grandchild_pid = fork();
		
		if (grandchild_pid < 0){
			perror("Failed to fork child");
			return 1;
		}
		
		else if (grandchild_pid == 0){
			printf("I am grandchild\n");		
		}
		
		else{
			wait(NULL);
			printf("I am child\n");
		}		
	}
	
	else{
		wait(NULL);
		printf("I am parent\n");
	}		
		
	return 0;
	
}
