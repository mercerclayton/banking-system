import random
import string
from bank_database import BankDatabase


class BankApp:
    """Main banking application handling user flow and actions."""

    def __init__(self) -> None:
        """Initialize the app and its database interface."""
        self.db = BankDatabase()
        self.running = True

    # -------------------------- Main Menu --------------------------

    def run(self) -> None:
        """Start the main loop."""
        while self.running:
            self.main_menu()
        print("Bye!")

    def main_menu(self) -> None:
        """Display the main menu and process user input."""
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
        choice = input("> ")

        if choice == "1":
            self.create_account()
        elif choice == "2":
            self.login_menu()
        elif choice == "0":
            self.running = False
        else:
            print("Invalid selection.\n")

    # -------------------------- Account Actions --------------------------

    def create_account(self) -> None:
        """Generate a valid account and save it to the database."""
        account_num = self._generate_account()
        pin = self._generate_pin()
        self.db.insert_account(account_num, pin)
        print("\nYour card has been created")
        print(f"Your card number:\n{account_num}")
        print(f"Your card PIN:\n{pin}\n")

    def login_menu(self) -> None:
        """Handle user login."""
        number = input("\nEnter your card number:\n> ")
        pin = input("Enter your PIN:\n> ")

        stored_pin = self.db.get_pin(number)
        if stored_pin == pin:
            print("\nYou have successfully logged in!\n")
            self.account_menu(number)
        else:
            print("\nWrong card number or PIN!\n")

    def account_menu(self, number: str) -> None:
        """Show actions available after login."""
        while True:
            print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
            choice = input("> ")

            if choice == "1":
                balance = self.db.get_balance(number)
                print(f"\nBalance: {balance}\n")

            elif choice == "2":
                try:
                    income = int(input("\nEnter income:\n> "))
                    self.db.update_balance(number, income)
                    print("Income was added!\n")
                except ValueError:
                    print("Invalid amount.\n")

            elif choice == "3":
                self._transfer(number)

            elif choice == "4":
                self.db.delete_account(number)
                print("The account has been closed!\n")
                break

            elif choice == "5":
                print("You have successfully logged out!\n")
                break

            elif choice == "0":
                self.running = False
                return

            else:
                print("Invalid selection.\n")

    # -------------------------- Transfer & Utility --------------------------

    def _transfer(self, sender: str) -> None:
        """Process money transfer to another account."""
        receiver = input("\nEnter card number:\n> ")
        if receiver == sender:
            print("You can't transfer money to the same account!\n")
            return
        if not self._luhn_check(receiver):
            print("Probably you made a mistake in the card number. Please try again!\n")
            return
        if not self.db.account_exists(receiver):
            print("Such a card does not exist.\n")
            return

        try:
            amount = int(input("Enter how much money you want to transfer:\n> "))
        except ValueError:
            print("Invalid amount.\n")
            return

        success = self.db.transfer(sender, receiver, amount)
        if success:
            print("Success!\n")
        else:
            print("Not enough money!\n")

    # -------------------------- Generators & Validators --------------------------

    @staticmethod
    def _generate_pin() -> str:
        """Generate a 4-digit PIN."""
        return "".join(random.choices(string.digits, k=4))

    @staticmethod
    def _generate_account() -> str:
        """Generate a valid account number using the Luhn algorithm."""
        base = "400000" + "".join(random.choices(string.digits, k=9))
        checksum = BankApp._luhn_sum(base)
        check_digit = (10 - checksum % 10) % 10
        return base + str(check_digit)

    @staticmethod
    def _luhn_sum(number: str) -> int:
        """Calculate the Luhn checksum for a number string."""
        digits = [int(d) for d in number]
        for i in range(0, len(digits), 2):
            digits[i] = digits[i] * 2 - 9 if digits[i] * 2 > 9 else digits[i] * 2
        return sum(digits)

    @staticmethod
    def _luhn_check(number: str) -> bool:
        """Verify if a number satisfies the Luhn algorithm."""
        return BankApp._luhn_sum(number) % 10 == 0
