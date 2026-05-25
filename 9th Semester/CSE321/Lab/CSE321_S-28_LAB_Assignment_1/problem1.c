#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>


typedef struct 
{
    int n;
    long long* fibonacci_seq;
    int search_index;
    long long search_result;
} thread_data_t;


pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond_fib_done = PTHREAD_COND_INITIALIZER;

int fib_completed = 0;
long long* global_fib_seq = NULL;
int global_n = 0;


void* compute_fibonacci(void* arg) {
    thread_data_t* data = (thread_data_t*)arg;
    int n = (*data).n;
    long long* fibonacci_seq;
    
    fibonacci_seq = (long long*)malloc((n + 1) * sizeof(long long));
    
    if (fibonacci_seq == NULL) 
    
    {
        printf("Memory allocation failed!\n");
        pthread_exit(NULL);
    }

    if (n >= 0) 
    
    {
        fibonacci_seq[0] = 0;
    }
    
    if (n >= 1) 
    
    {
        fibonacci_seq[1] = 1;
    }
    
    for (int i = 2; i <= n; i++) 
    
    {
        fibonacci_seq[i] = fibonacci_seq[i - 1] + fibonacci_seq[i - 2];
    }
    

    (*data).fibonacci_seq = fibonacci_seq;
    global_fib_seq = fibonacci_seq;
    global_n = n;
    
    pthread_mutex_lock(&mutex);
    fib_completed = 1;
    pthread_cond_broadcast(&cond_fib_done);
    pthread_mutex_unlock(&mutex);
    
    pthread_exit(NULL);
}


void* search_fibonacci(void* arg) 

{
    thread_data_t* data = (thread_data_t*)arg;
    int search_index = (*data).search_index;
    long long result;
    

    pthread_mutex_lock(&mutex);
    
    while (!fib_completed) 
    
    {
        pthread_cond_wait(&cond_fib_done, &mutex);
    }
    
    pthread_mutex_unlock(&mutex);
    

    if (search_index >= 0 && search_index <= global_n) 
    
    {
        result = global_fib_seq[search_index];
    } 
    
    else 
    
    {
        result = -1;
    }
    
    (*data).search_result = result;
    
    pthread_exit(NULL);
}

int main() 

{
    int n, num_searches;
    
    printf("Enter the term of fibonacci sequence:\n");
    scanf("%d", &n);
    
    if (n < 0 || n > 40) 
    
    {
        printf("Error: n must be between 0 and 40\n");
        return 1;
    }
    
    printf("How many numbers you are willing to search?:\n");
    scanf("%d", &num_searches);
    
    if (num_searches <= 0) 
    
    {
        printf("Error: number of searches must be greater than 0\n");
        return 1;
    }
    
    thread_data_t fib_data;
    fib_data.n = n;
    fib_data.fibonacci_seq = NULL;
    

    pthread_t fib_thread;
    
    if (pthread_create(&fib_thread, NULL, compute_fibonacci, &fib_data) != 0) 
    
    {
        printf("Error creating Fibonacci thread\n");
        return 1;
    }
    
    pthread_join(fib_thread, NULL);
    
    for (int i = 0; i <= n; i++) 
    {
        printf("a[%d] = %lld\n", i, fib_data.fibonacci_seq[i]);
    }
    
    pthread_t search_threads[num_searches];
    thread_data_t search_data[num_searches];
    
    int search_indices[num_searches];
    
    for (int i = 0; i < num_searches; i++) 
    
    {
        printf("Enter search %d:\n", i + 1);
        scanf("%d", &search_indices[i]);
    }
    
    for (int i = 0; i < num_searches; i++) 
    
    {
        search_data[i].n = n;
        search_data[i].fibonacci_seq = fib_data.fibonacci_seq;
        search_data[i].search_index = search_indices[i];
        
        if (pthread_create(&search_threads[i], NULL, search_fibonacci, &search_data[i]) != 0) 
        
        {
            printf("Error creating search thread %d\n", i + 1);
            return 1;
        }
    }
    
    for (int i = 0; i < num_searches; i++) 
    
    {
        pthread_join(search_threads[i], NULL);
    }
    
    for (int i = 0; i < num_searches; i++) 
    
    {
        printf("result of search #%d = %lld\n", i + 1, search_data[i].search_result);
    }
    
    free(fib_data.fibonacci_seq);
    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&cond_fib_done);
    
    return 0;
}
