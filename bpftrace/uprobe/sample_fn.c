#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int main() {
    int num1, num2, result;

    // Take two numbers as input
    printf("Enter first number: ");
    scanf("%d", &num1);
    printf("Enter second number: ");
    scanf("%d", &num2);

    // Call the add function
    result = add(num1, num2);

    // Print the result
    printf("Result: %d\n", result);

    return 0;
}
