import DatabaseConnection
from ussd_dial import ussd_dail


def bank_system_setup():
    qus = input("This operation will setup a database, and a customer table for your banking system.\n"
                "Please confirm you have your MySQL service running on your local PC or you are connected\n"
                "to a remote server. For remote server, please modify the login parameter on the "
                "DatabaseConnection.py module.\n"
                "Please confirm you have not already initiated this process.\n"
                "===================================================================================================\n"
                "Please confirm, do you have a database setup already? Yes or No\n")

    if qus.lower() == "no":
        print("setting up database...")
        print("===============================================\n")
        DatabaseConnection.sql_connect()
        try:
            DatabaseConnection.create_db()
        except Exception as ex:
            print("Failed to create database")
            print(ex)
        try:
            DatabaseConnection.create_table()
        except Exception as ex:
            print("Failed to create table")
            print(ex)
        try:
            DatabaseConnection.customer_dbconnect()
        except Exception as ex:
            print("Failed to connect to customer table")
            print(ex)
        print("=========================================================")
        print("Database and relevant customer table has been created,\n "
              "and connected successfully.\n"
              "You're all set!")
        print("=========================================================")
        ussd_dail()
    else:
        ussd_dail()


# ==========================Prompt Dial========================
def prompt_dail():
    print("====================================================")
    print("Welcome to XBZ Home Bank, your personal home banking system.\n"
          "Developed by Muhammad .A. Oyonumoh.\n"
          "====================================================\n"
          "This is a Simulator Bank project to demonstrate what happens \n"
          "at the back end with customer service when you walk\n"
          "into a bank for transaction.\n"
          "Hope you enjoy it.\n")
    print("====================================================")
    qus_operation = input("Please select an option of corresponding figure: \n"
                          "1: System Setup\n"
                          "2: Bank Operation\n")
    if qus_operation == "1":
        bank_system_setup()
    elif qus_operation == "2":
        ussd_dail()
    else:
        quit()


prompt_dail()
