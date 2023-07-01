from AccountBalance import account_bal_retrieval
from CashDeposit import cash_deposit
from CreateBankAccount import create_account
from Transfers import transfer


def ussd_dail():
    user_action = input("Please select option (corresponding figure: \n"
                        "1: Check Account Balance\n"
                        "2: Deposit\n"
                        "3: Transfer\n"
                        "4: Create Account\n"
                        "5: Quit\n")

    if user_action == "1":
        account_bal_retrieval()
    elif user_action == "2":
        cash_deposit()
    elif user_action == "3":
        transfer()
    elif user_action == "4":
        create_account()
    elif user_action == "5":
        print("Thank you for banking with us.")
        quit()
    else:
        print("That input was not recognised. Please try again later")
        quit()
