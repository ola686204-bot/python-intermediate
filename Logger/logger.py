class Calculator:
    def add(self, num1 , num2):
        return num1 + num2
    
    def subtract(self, num1 , num2):
        return num1 - num2

    def multiply(self, num1 , num2):
        return num1 * num2

    def divide(self, num1 , num2):
        if num2 == 0:
            return f"Error: Cannot divide by zero."
        return num1 / num2

    def floor_divide(self, num1 , num2):
        if num2 == 0:
            return f"Error: Cannot divide by zero."
        return num1 // num2

    def modulus(self, num1 , num2):
        if num2 == 0:
            return f"Error: Cannot mod by zero."
        return num1 % num2

    def power(self, num1, num2):
        return num1 ** num2

def get_number():
    while True:
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            return num1,num2
        except ValueError:
            print("Invalid Number! Try again.")


calc = Calculator()

while True:
    print("\n======== Menu Calculator ========")
    print()
    operation = ["Addition",
                 "Subtraction",
                 "Multiplication",
                 "Division",
                 "Floor Division",
                 "Modulus",
                 "Power",
                 "Exit"
    ]
    for index, operation in enumerate(operation, start=1):
        print(f"{index}. {operation}")

    try:
        choice = int(input("Enter a choice between (1-8): "))
    except ValueError:
        print("Choice must be a valid number .")
        continue
    

    if choice == 8:
        print("Exiting Program, Bye! ")
        break

    num1, num2 = get_number()

    if choice == 1:
        print(f"Result: {num1} + {num2} = {calc.add(num1, num2)}")
    elif choice == 2:
        print(f"Result: {num1} - {num2} = {calc.subtract(num1, num2)}")
    elif choice == 3:
        print(f"Result: {num1} * {num2} = {calc.multiply(num1, num2)}")
    elif choice == 4:
        print(f"Result: {num1} / {num2} = {calc.divide(num1, num2)}")
    elif choice == 5:
        print(f"Result: {num1} // {num2} = {calc.floor_divide(num1, num2)}")
    elif choice == 6:
        print(f"Result: {num1} % {num2} = {calc.modulus(num1, num2)}")
    elif choice == 7:
        print(f"Result: {num1} ** {num2} = {calc.power(num1, num2)}")
    else:
        print(f"Invalid choice. Try again.")
    
if __name__ == "__main__":
    get_number()
