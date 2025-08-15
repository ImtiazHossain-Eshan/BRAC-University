#include <stdio.h>
#include <stdlib.h>
#include <string.h>


#define MAX_LENGTH 1024

int main(int argc, char *argv[]){
	if (argc < 2){
		printf("File name not given\n");
		return 1;
	}
	
	FILE *my_file = fopen(argv[1], "a");

	if (my_file == NULL){
		perror("Error opening file");
		return 1;
	}

	char input[MAX_LENGTH];

	printf("Enter strings to write to the file (ENTER \"-1\" to stop):\n");

	while (1){
		printf("> ");
		
		if (fgets(input, MAX_LENGTH, stdin) == NULL){
			printf("Input Error.\n");
			break;
		}
		
		input[strcspn(input, "\n")] = '\0'; //null terminator
		
		if (strcmp(input, "-1") == 0){
			break;
		}
		
		fprintf(my_file, "%s\n", input);


	}

	fclose(my_file);

	printf("Data written to %s successfully.\n", argv[1]);

	return 0;

}
