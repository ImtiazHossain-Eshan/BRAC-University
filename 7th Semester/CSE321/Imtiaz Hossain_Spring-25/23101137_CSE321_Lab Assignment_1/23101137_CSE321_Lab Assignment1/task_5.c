#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(){
    pid_t parent_pid, child_pid, grandchild_pid1, grandchild_pid2, grandchild_pid3;
    
    int status;
    
    parent_pid = getpid();
    
    printf("1. Parent process ID: %d\n", parent_pid);
    
    child_pid = fork();
    
    if (child_pid == 0){
      
        printf("2. Child process ID: %d\n", getpid());
        
        grandchild_pid1 = fork();
        
        if (grandchild_pid1 == 0){          
            printf("3. Grand Child process ID: %d\n", getpid());
            exit(0);
        } 
        
        else{
            grandchild_pid2 = fork();
            
            if (grandchild_pid2 == 0){
                printf("4. Grand Child process ID: %d\n", getpid());
                exit(0);
            } 
            
            else{
                grandchild_pid3 = fork();
                
                if (grandchild_pid3 == 0){
                    printf("5. Grand Child process ID: %d\n", getpid());
                    exit(0);
                } 
                
                else{                 
                    while (wait(NULL) > 0);
                }
            }
        }
    } 
    
    else{
        waitpid(child_pid, &status, 0);
    }
    
    return 0;
    
}
