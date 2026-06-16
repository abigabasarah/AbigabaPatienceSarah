# Menu-driven calculator using functions
def add(a, b):
    result = a + b
    print("Result:", a, "+", b, "=", result)


def subtract(a, b):
    result = a - b
    print("Result:", a, "-", b, "=", result)


def multiply(a, b):
    result = a * b
    print("Result:", a, "*", b, "=", result)


def divide(a, b):
    if b == 0:
        print("Error: Cannot divide by zero!")
    else:
        result = a / b
        print("Result:", a, "/", b, "=", result)


def show_menu():
    print("\n==============================")
    print("       CALCULATOR MENU        ")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Exit")


while True:
    show_menu()
    choice = input("Enter your choice (1-5): ")

    if choice == "5":
        print("Exiting....")
        break

    elif choice in ("1", "2", "3", "4"):
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))

        if choice == "1":
            add(a, b)
        elif choice == "2":
            subtract(a, b)
        elif choice == "3":
            multiply(a, b)
        elif choice == "4":
            divide(a, b)
    else:
        print("Invalid choice! Please enter a number between 1 and 5.")
