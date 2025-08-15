#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

int main (int count, char *args[]){

	pid_t pid1;
	
	int arr_size=5;
	
	printf("Enter 5 elements one by one\n");
	char* arr[arr_size];
	
	for (int i = 0; i < arr_size; i++){
		arr[i]=(char *) malloc(32*sizeof(char));
	} 
	
	for (int i = 0; i < arr_size; i++){
		printf("Enter an integer : ");
		scanf("%s", arr[i]);
	}
	
	pid1 = fork();
	
	if (pid1 < 0) {
		printf("Fork Failed");
	}
	
	else if (pid1 == 0) {
		printf("--> Child process running... \n");
		execl("/home/imtiaz/CSE321_LAB_Assignment_1/sort","will_sort", arr[0], arr[1], arr[2], arr[3], arr[4], NULL);
		printf("Error\n");
	}
	
	else {
		wait(NULL);
		printf("----> Parent process running...\n");
		execl("/home/imtiaz/CSE321_LAB_Assignment_1/oddeven","do_oddeven", arr[0], arr[1], arr[2], arr[3], arr[4], NULL);
		printf("Error\n");
	}
}
