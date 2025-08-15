#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <semaphore.h>

#define TOTAL_STD 10
#define CHAIR_CNT 3

int wait_std = 0;
int done_std = 0;
int curr_std = -1;
int in_consultation = 0;

sem_t st_ready;
sem_t std_ready;
sem_t consultation_lock;
pthread_mutex_t lock;

void* std_thread(void* arg);
void* st_thread(void* arg);

int main(){
    pthread_t stds[TOTAL_STD];
    pthread_t st;
    int std_ids[TOTAL_STD];

    sem_init(&st_ready, 0, 0);
    sem_init(&std_ready, 0, 0);
    sem_init(&consultation_lock, 0, 1);
    pthread_mutex_init(&lock, NULL);

    pthread_create(&st, NULL, st_thread, NULL);

    for(int i=0;i<TOTAL_STD;i++){
        std_ids[i] = i;
        pthread_create(&stds[i], NULL, std_thread, &std_ids[i]);
        usleep((rand() % 1500000) + 500000);
    }

    for(int i=0;i<TOTAL_STD;i++){
        pthread_join(stds[i], NULL);
    }

    pthread_cancel(st);
    pthread_join(st, NULL);

    sem_destroy(&st_ready);
    sem_destroy(&std_ready);
    sem_destroy(&consultation_lock);
    pthread_mutex_destroy(&lock);

    return 0;
}

void* std_thread(void* arg){
    int id = *((int*)arg);

    pthread_mutex_lock(&lock);
    if(wait_std < CHAIR_CNT){
        wait_std++;
        printf("Student %d started waiting for consultation\n", id);

        if(wait_std == 1 && !in_consultation){
            sem_post(&std_ready);
        }

        printf("Number of students now waiting: %d\n", wait_std);
        pthread_mutex_unlock(&lock);

        sem_wait(&st_ready);
        sem_wait(&consultation_lock);
        in_consultation = 1;

        pthread_mutex_lock(&lock);
        wait_std--;
        curr_std = id;
        printf("ST giving consultation\n");
        printf("Student %d is getting consultation\n", id);
        pthread_mutex_unlock(&lock);

        usleep((rand() % 2000000) + 1000000);

        pthread_mutex_lock(&lock);
        curr_std = -1;
        in_consultation = 0;
        done_std++;
        printf("Student %d finished getting consultation and left\n", id);
        printf("Number of served students: %d\n", done_std);
        
        sem_post(&consultation_lock);  // Release consultation room lock
        
        if(wait_std > 0){
            sem_post(&std_ready);
        }
        pthread_mutex_unlock(&lock);
    }
    else{
        printf("No chairs remaining in lobby. Student %d Leaving.....\n", id);
        done_std++;
        printf("Number of served students: %d\n", done_std);
        pthread_mutex_unlock(&lock);
    }

    pthread_exit(NULL);
}

void* st_thread(void* arg){
    while(1){
        sem_wait(&std_ready);

        pthread_mutex_lock(&lock);
        if(wait_std > 0 && !in_consultation){
            printf("A waiting student started getting consultation\n");
            sem_post(&st_ready);
        }
        pthread_mutex_unlock(&lock);
    }

    pthread_exit(NULL);
}
