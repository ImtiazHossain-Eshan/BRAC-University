#include <stdio.h>
#include <stdlib.h>

int main(int count, char *args[]){

	int temp;
	
	for (int i = 1; i < count; i++){
		temp = atoi(args[i]);
		
		if ((temp % 2) == 0){
			printf("%d : Even\n", temp);
		}
		else{
			printf("%d : Odd\n", temp);
		}
		
	}
	
}
