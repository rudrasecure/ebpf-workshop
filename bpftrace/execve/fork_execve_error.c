#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main(void)
{
    int pid = fork();
    int rc = 0;

    if (pid ==0) {
        printf("I am the child\n");
        char *margs[] = {"/bin/nonexistentfile", NULL, NULL, NULL, NULL };
        rc = execve(margs[0], margs, NULL);
        printf("We should not see this %d\n", rc);
    } else {
        printf("I am the parent\n");
        }
    return rc;
}
