#include <stdio.h>
#include <stdlib.h>


void sort(int count, int* arr);

int main(int count, char *args[]){

	int arr[count-1];
	
	for (int i=0; i < count-1; i++){
		arr[i] = atoi(args[i+1]);
	}
	
	sort(count-1, arr);

}

void sort(int count, int* arr){

	int n_arr[count];

	for (int i = 0; i < count; i++){
		n_arr[i] = arr[i];
	}
	
	for (int i = 0; i < count; i++){
		for (int j = i; j > 0; j--){
			if (n_arr[j] > n_arr[j-1]){
				int temp = n_arr[j];
				n_arr[j] = n_arr[j-1];
				n_arr[j-1] = temp;	
			}
		}
	}
	
	printf("Sorted array in descending order: ");
	
	for (int i = 0; i < count; i++){
		printf("%d ", n_arr[i]);
	}
	
	printf("\n");
	
}
