#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>
#include <time.h>

#define BREAD 0
#define CHEESE 1
#define LETTUCE 2

sem_t table_empty;          // Signals--> empty table
sem_t table_ready;          // Signals--> ingredients are ready
sem_t maker_finished;       // Signals--> maker finishes

pthread_mutex_t table_mutex = PTHREAD_MUTEX_INITIALIZER;

int table_ingredient1 = -1;
int table_ingredient2 = -1;
int sandwich_count = 0;
int total_sandwiches = 0;


const char* get_ingredient_name(int ingredient) 
{
    switch(ingredient) 
    {
        case BREAD: return "Bread";
        case CHEESE: return "Cheese";
        case LETTUCE: return "Lettuce";
        default: return "Unknown";
    }
}

char get_maker_for_ingredients(int ing1, int ing2) 
{
    int ingredients_present = (1 << ing1) | (1 << ing2);
    
    switch(ingredients_present) 
    
    {
        case (1 << BREAD) | (1 << CHEESE):
            return 'C';
        case (1 << BREAD) | (1 << LETTUCE):
            return 'B';
        case (1 << CHEESE) | (1 << LETTUCE):
            return 'A';
        default:
            return '?';
    }
}


void* supplier(void* arg) 
{
    int n = *((int*)arg);
    
    for (int i = 0; i < n; i++) 
    {
        sem_wait(&table_empty);
        
        pthread_mutex_lock(&table_mutex);
        

        do 
        
        {
            table_ingredient1 = rand() % 3;
            table_ingredient2 = rand() % 3;
            
        } while (table_ingredient1 == table_ingredient2);
        
        printf("Supplier places: %s and %s\n", 
               get_ingredient_name(table_ingredient1),
               get_ingredient_name(table_ingredient2));
        
        pthread_mutex_unlock(&table_mutex);
        

        sem_post(&table_ready);
        

        sem_wait(&maker_finished);
    }
    
    pthread_exit(NULL);
}


void* sandwich_maker(void* arg) 

{
    char maker_id = *((char*)arg);
    int my_ingredient;
    
    switch(maker_id) 
    
    {
        case 'A': my_ingredient = BREAD; break;
        case 'B': my_ingredient = CHEESE; break;
        case 'C': my_ingredient = LETTUCE; break;
        default: pthread_exit(NULL);
    }
    
    while (1) 
    
    {
        sem_wait(&table_ready);
        
        pthread_mutex_lock(&table_mutex);
        
        char required_maker = get_maker_for_ingredients(table_ingredient1, table_ingredient2);
        
        if (required_maker == maker_id) 
        
        {
            printf("Maker %c picks up %s and %s\n", 
                   maker_id,
                   get_ingredient_name(table_ingredient1),
                   get_ingredient_name(table_ingredient2));
            
            printf("Maker %c is making the sandwich...\n", maker_id);
            

            usleep(100000); //--> 100ms
            
            printf("Maker %c finished making the sandwich and eats it\n", maker_id);
            printf("Maker %c signals Supplier\n\n", maker_id);
            
            table_ingredient1 = -1;
            table_ingredient2 = -1;
            
            sandwich_count++;
            
            pthread_mutex_unlock(&table_mutex);

            sem_post(&maker_finished);

            sem_post(&table_empty);
        } 
        
        else 
        
        {

            pthread_mutex_unlock(&table_mutex);
            sem_post(&table_ready);
        }
        
        if (sandwich_count >= total_sandwiches) 
        
        {
            break;
        }
    }
    
    pthread_exit(NULL);
}

int main(int argc, char* argv[]) 

{
    if (argc != 2) 
    
    {
        printf("Usage: %s <number_of_sandwiches>\n", argv[0]);
        return 1;
    }
    
    total_sandwiches = atoi(argv[1]);
    
    if (total_sandwiches <= 0) 
    {
        printf("Number of sandwiches must be positive\n");
        return 1;
    }
    
    srand(time(NULL));
    
    sem_init(&table_empty, 0, 1);
    sem_init(&table_ready, 0, 0);
    sem_init(&maker_finished, 0, 0);
    
    pthread_t supplier_thread;
    pthread_t maker_threads[3];
    char maker_ids[3] = {'A', 'B', 'C'};
    
    pthread_create(&supplier_thread, NULL, supplier, &total_sandwiches);
    
    for (int i = 0; i < 3; i++) 
    {
        pthread_create(&maker_threads[i], NULL, sandwich_maker, &maker_ids[i]);
    }
    
    pthread_join(supplier_thread, NULL);
    
    sleep(3);
    
    sem_destroy(&table_empty);
    sem_destroy(&table_ready);
    sem_destroy(&maker_finished);
    pthread_mutex_destroy(&table_mutex);
    
    return 0;
}
