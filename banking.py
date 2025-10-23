from bank_app import BankApp


def main() -> None:
    """Entry point for the banking system."""
    app = BankApp()
    app.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
