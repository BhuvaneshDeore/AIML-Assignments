# Day 5 — Bank Account Management System

## Project Flow

Code
class BankAccount:

    # Initialize account owner and starting balance
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    # Add the given amount to the account balance
    def deposit(self, amount):
        self.balance += amount

    # Withdraw amount only if sufficient balance is available
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            print("insufficient balance") # if balance < amount then it will print #insufficient balance

    # Display the current account balance
    def show_balance(self):
        print(f"Balance:{self.balance}")

# Create a bank account for Gaurav with balance 5000
acc = BankAccount("Gaurav", 5000)

# Deposit ₹1500 
acc.deposit(1500)

# Withdraw ₹2000 
acc.withdraw(2000)

# Display the final account balance
acc.show_balance()

Output
Balance:4500

Project Result

operations:

Initial Balance  → ₹5000
Deposit          → ₹1500
Withdrawal       → ₹2000
Final Balance    → ₹4500