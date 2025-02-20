#include <stdio.h>
#include <unistd.h>

int main(void)
{
    char *margs[] = {"/bin/id", NULL };
    int rc = execve(margs[0], margs, NULL);
    printf("If all goes well, we don't see this %d\n", rc);

    return rc;
}
