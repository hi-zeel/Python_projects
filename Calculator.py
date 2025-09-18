# Simple Calculator Program

# Ask the user to enter the first number and validate input
def get_float_input(prompt):
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Invalid input. Please enter a valid number.")

a = get_float_input("Enter the first number: ")

# Ask the user to enter the second number and validate input
def get_float_input(prompt):
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Invalid input. Please enter a valid number.")

b = get_float_input("Enter the second number: ")

# Ask the user to enter the operation they want to perform and validate input
while True:
    operation = input("Enter the operation (+, -, *, /): ")
    if operation == '+':
        print("The value of", a, "+", b, "is:", a + b)
    elif operation == '-':
        print("The value of", a, "-", b, "is:", a - b)
        break
    elif operation == '*':
        print("The value of", a, "*", b, "is:", a * b)
        break
    elif operation == '/':
        while b == 0:
            print("Error: Division by zero is not allowed.")
            b = get_float_input("Please enter a non-zero value for the second number: ")
        print("The value of", a, "/", b, "is:", a / b)
        break
    else:
        print("Invalid operation. Please enter one of +, -, *, /.")
print("Thanks for using this calculator! 😊")
