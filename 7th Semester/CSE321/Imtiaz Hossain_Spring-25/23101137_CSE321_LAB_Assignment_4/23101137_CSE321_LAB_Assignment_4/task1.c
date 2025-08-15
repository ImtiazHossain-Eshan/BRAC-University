#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_USERS 5
#define MAX_RESOURCES 5
#define MAX_NAME_LEN 20

typedef enum{
    READ = 1,
    WRITE = 2,
    EXECUTE = 4
} Permission;

typedef struct{
    char name[MAX_NAME_LEN];
} User;

typedef struct{
    char name[MAX_NAME_LEN];
} Resource;

typedef struct{
    char username[MAX_NAME_LEN];
    int permissions;
} ACLEntry;

typedef struct{
    Resource resource;
    ACLEntry entries[MAX_USERS];
    int acl_count;
} ACLControlledResource;

typedef struct{
    char resource_name[MAX_NAME_LEN];
    int permissions;
} Capability;

typedef struct{
    User user;
    Capability capabilities[MAX_RESOURCES];
    int capability_count;
} CapabilityUser;

void printPermissions(int perm){
    int isFirst = 1;
    if (perm & READ){
        printf("READ");
        isFirst = 0;
    }
    if (perm & WRITE){
        if (!isFirst) printf(", ");
        printf("WRITE");
        isFirst = 0;
    }
    if (perm & EXECUTE){
        if (!isFirst) printf(", ");
        printf("EXECUTE");
        isFirst = 0;
    }
    if (isFirst){
        printf("None");
    }
}

int hasPermission(int userPerm, int requiredPerm){
    return (userPerm & requiredPerm) ? 1 : 0;
}

void checkACLAccess(ACLControlledResource *res, const char *userName, int perm){
    for (int i = 0; i < res->acl_count; i++){
        if (strcmp(res->entries[i].username, userName) == 0){
            if (hasPermission(res->entries[i].permissions, perm)){
                printf("ACL Check: User %s requests ", userName);
                printPermissions(perm);
                printf(" on %s: Access GRANTED\n", res->resource.name);
            }
            
            else{
                printf("ACL Check: User %s requests ", userName);
                printPermissions(perm);
                printf(" on %s: Access DENIED\n", res->resource.name);
            }
            return;
        }
    }
    printf("ACL Check: User %s has NO entry for resource %s: Access DENIED\n", userName, res->resource.name);
}

void checkCapabilityAccess(CapabilityUser *user, const char *resourceName, int perm){
    for (int i = 0; i < user->capability_count; i++){
        if (strcmp(user->capabilities[i].resource_name, resourceName) == 0){
            if (hasPermission(user->capabilities[i].permissions, perm)){
                printf("Capability Check: User %s requests ", user->user.name);
                printPermissions(perm);
                printf(" on %s: Access GRANTED\n", resourceName);
            }
            
            else{
                printf("Capability Check: User %s requests ", user->user.name);
                printPermissions(perm);
                printf(" on %s: Access DENIED\n", resourceName);
            }
            return;
        }
    }
    printf("Capability Check: User %s has NO capability for %s: Access DENIED\n", user->user.name, resourceName);
}

int main(){
    User users[MAX_USERS] = {{"Alice"}, {"Bob"}, {"Charlie"}, {"Imtiaz"}, {"Eshan"}};
    Resource resources[MAX_RESOURCES] = {{"File1"}, {"File2"}, {"File3"}, {"File4"}, {"File5"}};

    ACLControlledResource aclResources[MAX_RESOURCES];
    
    aclResources[0].resource = resources[0];
    aclResources[0].acl_count = 2;
    strcpy(aclResources[0].entries[0].username, "Alice");
    aclResources[0].entries[0].permissions = READ;
    strcpy(aclResources[0].entries[1].username, "Bob");
    aclResources[0].entries[1].permissions = EXECUTE;


    aclResources[1].resource = resources[1];
    aclResources[1].acl_count = 0;

    aclResources[2].resource = resources[2];
    aclResources[2].acl_count = 0;

    aclResources[3].resource = resources[3];
    aclResources[3].acl_count = 1;
    strcpy(aclResources[3].entries[0].username, "Eshan");
    aclResources[3].entries[0].permissions = READ | WRITE;

    aclResources[4].resource = resources[4];
    aclResources[4].acl_count = 1;
    strcpy(aclResources[4].entries[0].username, "Imtiaz");
    aclResources[4].entries[0].permissions = EXECUTE;

    CapabilityUser capabilityUsers[MAX_USERS];
    capabilityUsers[0].user = users[0];
    capabilityUsers[0].capability_count = 1;
    strcpy(capabilityUsers[0].capabilities[0].resource_name, "File1");
    capabilityUsers[0].capabilities[0].permissions = WRITE;

    capabilityUsers[1].user = users[1];
    capabilityUsers[1].capability_count = 0;

    capabilityUsers[2].user = users[2];
    capabilityUsers[2].capability_count = 0;

    capabilityUsers[3].user = users[3];
    capabilityUsers[3].capability_count = 1;

    strcpy(capabilityUsers[3].capabilities[0].resource_name, "File5");
    capabilityUsers[3].capabilities[0].permissions = EXECUTE;

    capabilityUsers[4].user = users[4];
    capabilityUsers[4].capability_count = 1;
    strcpy(capabilityUsers[4].capabilities[0].resource_name, "File4");
    capabilityUsers[4].capabilities[0].permissions = READ | WRITE;

    checkACLAccess(&aclResources[0], "Alice", READ);
    checkACLAccess(&aclResources[0], "Bob", WRITE);
    checkACLAccess(&aclResources[0], "Charlie", READ);
    checkACLAccess(&aclResources[3], "Eshan", WRITE);
    checkACLAccess(&aclResources[4], "Imtiaz", EXECUTE);
    checkACLAccess(&aclResources[3], "Imtiaz", READ);


    checkCapabilityAccess(&capabilityUsers[0], "File1", WRITE);
    checkCapabilityAccess(&capabilityUsers[1], "File1", WRITE);
    checkCapabilityAccess(&capabilityUsers[2], "File2", READ);
    checkCapabilityAccess(&capabilityUsers[3], "File5", EXECUTE);
    checkCapabilityAccess(&capabilityUsers[4], "File4", WRITE);
    checkCapabilityAccess(&capabilityUsers[4], "File5", READ);    

    return 0;
    
}
