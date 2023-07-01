import trigger_cursor
from trigger_cursor import trigger_handle
import locale
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from TransactionTime import tranx_date_time

def cash_deposit():
    print("==============================")
    print("Cash deposit initiated...")
    print("============================\n")
    cus_input = input("Enter account Number: \n")
    deposit = input("Enter deposit amount: \n")
    try:
        deposit_amount = float(deposit)
        # we select account balance from the user input
    except Exception as ex:
        print("Invalid entry!")
        print(ex)
        quit()
    try:
        acc_balance = "SELECT Balance FROM Customers WHERE Account_Number = %s"
        bal_value = (str(cus_input),)  # convert the input to string
        trigger_handle.execute(acc_balance, bal_value)
        acc_bal_tpl = trigger_handle.fetchone()
        acc_bal = acc_bal_tpl[0]
    except Exception as ex:
        print("Failed to carry out operation")
        if ex:
            print("Account number not found!")
            print(ex)
            quit()
    # We convert the string tuple to float/int for calculation
    old_bal = float(acc_bal)
    new_bal = old_bal + deposit_amount

    # We update record on database
    try:
        acc_balance = "UPDATE Customers SET Balance = %s WHERE Account_Number = %s"
        bal_value = (str(new_bal), str(cus_input))  # convert the input to string
        trigger_handle.execute(acc_balance, bal_value)
        trigger_cursor.trigger.commit()
    except Exception as ex:
        if ex:
            print("Invalid entry.")
            print(ex)
            quit()

    # ==============Email Notification=====================

    # 1) Senders Email fetch
    cus_email_fetch = "SELECT Email FROM Customers WHERE Account_Number = %s"
    cus_account_number = (str(cus_input),)
    trigger_handle.execute(cus_email_fetch, cus_account_number)
    cus_email_fetch_result = trigger_handle.fetchone()
    cus_email_0 = cus_email_fetch_result[0]
    cus_email = str(cus_email_0)
    # 2) Senders Email fetch
    cus_name_fetch = "SELECT Name FROM Customers WHERE Account_Number = %s"
    cus_account_number = (str(cus_input),)
    trigger_handle.execute(cus_name_fetch, cus_account_number)
    cus_name_fetch_result = trigger_handle.fetchone()
    cus_name_0 = cus_name_fetch_result[0]
    cus_name_1 = str(cus_name_0)

    def send_email_deposit(sender_email, sender_password, receiver_email, subject, message):
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
            try:
                server.login(sender_email, sender_password)
            except Exception as ex_note:
                print(ex_note)

            # Send the email
            try:
                server.send_message(email_message)
            except Exception as ex_note:
                print(ex_note)

    # Provide the necessary information
    sender_name = "XBZ Bank Plc"
    sender_email = "xbzbank@scupanet.com"
    sender_password = "Rasheedah.com*87"
    receiver_email = f"{cus_email}"
    subject = "Credit Alert"
    message = f"Dear {cus_name_1},\n" \
              f"You have credited your XBZ Bank account via direct bank deposit " \
              f"with the sum of: {locale.currency(deposit_amount, grouping=True)}. \n" \
              f"Transaction date: {tranx_date_time()}.\n" \
              f"Your current account balance is now: {locale.currency(new_bal, grouping=True)}"

    print("Cash deposit successful! Account balance has been updated.")
    # Send email-notification
    send_email_deposit(sender_email, sender_password, receiver_email, subject, message)
    print("===============================================")
    print("Email notification successful.")
    print("===============================================\n")
