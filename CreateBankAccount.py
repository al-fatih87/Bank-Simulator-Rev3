from trigger_cursor import trigger_handle
from trigger_cursor import trigger
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from TransactionTime import tranx_date_time


def create_account():  # Function to create bank account
    print("==============================")
    print("Account creation initiated...")
    print("============================\n")
    full_name = input("Enter Full Name: \n")
    email = input("Enter email: \n")
    phone_number = input("Enter Phone Number: \n")
    account_number = random.randint(1234567890, 9999999999)
    account_balance = 0

    acc_field = "INSERT INTO customers (Phone, Email, Name, Account_Number, Balance) VALUES (%s, %s, %s, %s, %s)"
    # Now, we convert values to string to pass into database
    acc_details = (str(phone_number), str(email), str(full_name), str(account_number), str(account_balance))
    try:
        trigger_handle.execute(acc_field, acc_details)
        trigger.commit()
        print(trigger_handle.rowcount, "Process completed!")
        print("===============================================")
        print("Congratulations! Your account was successfully created.")
        print(f"Your account number is: {account_number} \n"
              f"Your account name is: {full_name} \n"
              f"And your account balance is: {account_balance} \n"
              f"Do well to fund your account. Thanks for choosing XBZ Bank.")
    except Exception as ex:
        print("Account creation failed")
        print(ex)

    # ==============Email Notification=====================

    def send_email_creation(sender_email, sender_password, receiver_email, subject, message):
        # Create a multipart message object
        email_message = MIMEMultipart()
        email_message["From"] = formataddr((sender_name, sender_email))
        email_message["To"] = receiver_email
        email_message["Subject"] = subject

        # Add the message body
        email_message.attach(MIMEText(message, "plain"))

        # Create a secure connection to the SMTP server
        with smtplib.SMTP_SSL("mail.scupanet.com", 465) as server:
            # Login to the sender's email account
            server.login(sender_email, sender_password)

            # Send the email
            server.send_message(email_message)

    # Provide the necessary information
    sender_name = "XBZ Bank Plc"
    sender_email = "xbzbank@scupanet.com"
    sender_password = "Rasheedah.com*87"
    receiver_email = f"{email}"
    subject = "New Account with XBZ Bank"
    message = f"Dear {full_name},\n"\
              f"Thank you for creating an account with XBZ Bank. \n" \
              f"You account number is.{account_number}.\n" \
              f"Date: {tranx_date_time()}"

    # Send email notification
    send_email_creation(sender_email, sender_password, receiver_email, subject, message)
    print("===============================================\n")
    print("Notification success.")
    print("===============================================\n")