#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

struct FIBODATA{
    int n;
    long long *result;
};

struct SearchData{
    int count_of_search;
    int *search_indices;
    long long *fib_sequence;
    int sequence_length;
    int *search_results;
};

void *fib_gen(void *arg){

    struct FIBODATA *data = (struct FIBODATA *)arg;
    
    int n = (*data).n;
    
    (*data).result = (long long *)malloc((n + 1) * sizeof(long long));
    
    if ((*data).result == NULL){
        fprintf(stderr, "Malloc Failed\n");
        pthread_exit(NULL);
    }
    
    if (n >= 0) (*data).result[0] = 0;
    if (n >= 1) (*data).result[1] = 1;
    
    for (int i = 2; i <= n; i++){
        (*data).result[i] = (*data).result[i - 1] + (*data).result[i - 2];
    }
    
    pthread_exit(NULL);
    
}


void *fib_search(void *arg){
    struct SearchData *data = (struct SearchData *)arg;
    
    for (int i = 0; i < (*data).count_of_search; i++){
    
        int index = (*data).search_indices[i];
        
        if (index >= 0 && index <= (*data).sequence_length){
            (*data).search_results[i] = (*data).fib_sequence[index];
        }
      	
      	else{
            (*data).search_results[i] = -1;
        }
    }
    
    pthread_exit(NULL);
}

int main(){
    int n, count_of_search;
    
    pthread_t fib_thread, search_thread;
    
    printf("Enter the term of fibonacci sequence:\n");
    scanf("%d", &n);
    
    if (n < 0 || n > 40){
        printf("Error: The term must be between 0 and 40\n");
        return 1;
    }
    
    struct FIBODATA fib_data;
    fib_data.n = n;
    
    if (pthread_create(&fib_thread, NULL, fib_gen, &fib_data) != 0){
        fprintf(stderr, "Error creating fibonacci thread\n");
        return 1;
    }
    
    pthread_join(fib_thread, NULL);
    
    for (int i = 0; i <= n; i++){
        printf("a[%d] = %lld\n", i, fib_data.result[i]);
    }
    
    printf("How many numbers you are willing to search?:\n");
    scanf("%d", &count_of_search);
    
    if (count_of_search <= 0){
        printf("Error: The number of searches must be greater than 0\n");
        free(fib_data.result);
        return 1;
    }
    
    int *search_indices = (int *)malloc(count_of_search * sizeof(int));
    int *search_results = (int *)malloc(count_of_search * sizeof(int));
    
    if (search_indices == NULL || search_results == NULL){
        fprintf(stderr, "Malloc failed\n");
        free(fib_data.result);
        if (search_indices) free(search_indices);
        if (search_results) free(search_results);
        
        return 1;
        
    }
    
    for (int i = 0; i < count_of_search; i++){
        printf("Enter search %d:\n", i + 1);
        scanf("%d", &search_indices[i]);
    }
    
    struct SearchData search_data;
    search_data.count_of_search = count_of_search;
    search_data.search_indices = search_indices;
    search_data.fib_sequence = fib_data.result;
    search_data.sequence_length = n;
    search_data.search_results = search_results;
    
    if (pthread_create(&search_thread, NULL, fib_search, &search_data) != 0){
        fprintf(stderr, "Error creating search thread\n");
        free(fib_data.result);
        free(search_indices);
        free(search_results);
        
        return 1;
        
    }
    
    pthread_join(search_thread, NULL);
    
    for (int i = 0; i < count_of_search; i++){
        printf("result of search #%d = %d\n", i + 1, search_results[i]);
    }
    
    free(fib_data.result);
    free(search_indices);
    free(search_results);
    
    return 0;
}
