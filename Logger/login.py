class BankAccount:
    def __init__(self,owner,balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance < amount:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        
    def get_balance(self):
        return self.balance   

calc = BankAccount("Ada",50000)

def display():
    while True:
        print(f"------ BANK ACCOUNT ------")
        option = ["Withdraw",
                  "Deposit",
                  "Check Balance",
                  "Log out",
                  ]
        for index, option in enumerate(option, start=1):
            print (f"{index}. {option}")

        try:
            user_input = int(input("Enter an option:"))
        except ValueError:
            print("Enter a valid option:")
            continue
        
        if user_input == 4:
            print("Loging out...")
            break
        
        if user_input == 1:
            amount = int(input("Enter Amount:"))
            print(amount)
            print (f"Withdraw Successful. {calc.withdraw(amount)}")
        elif user_input == 2:
                amount = int(input("Enter Amount:"))
                print(amount)
                print (f"Deposit Successful. {calc.deposit(amount)}")
        elif user_input == 3:
                print (f"Withdraw Successful. {calc.get_balance}")
        else:
             print("Invalid Input.  Try again") 
if  __name__ == "__main__":
    display()   
