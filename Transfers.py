from trigger_cursor import trigger
from trigger_cursor import trigger_handle
import locale
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from TransactionTime import tranx_date_time


locale.setlocale(locale.LC_MONETARY, 'en_NG')


def transfer():
    print("==============================")
    print("Funds Transfer initiated...")
    print("============================\n")

    sender_acc_input = input("Please enter your (sender's) account Number: \n")
    input_transfer_amount = input("Enter transfer amount: \n")
    try:
        transformed_transfer_amount = float(input_transfer_amount)
    except Exception as ex:
        print("Invalid entry-1!")
        print(ex)
        quit()
    transfer_amount = locale.currency(transformed_transfer_amount, grouping=True)
    receiver_acc_num = input("Enter receiver's account number: \n")
    description = input("Description: ")
    # ================================================================================
    # We fetch receivers' email addresses for the sender and receiver of funds.
    # ==================================================================================
    # 1) Senders Email fetch
    sender_email_fetch = "SELECT Email FROM Customers WHERE Account_Number = %s"
    sender_account_number = (str(sender_acc_input),)
    trigger_handle.execute(sender_email_fetch, sender_account_number)
    email_fetch_result = trigger_handle.fetchone()
    sender_email_0 = email_fetch_result[0]
    sender_email_1 = str(sender_email_0)

    # 2) Senders Name fetch
    sender_name_fetch = "SELECT Name FROM Customers WHERE Account_Number = %s"
    sender_account_number = (str(sender_acc_input),)
    trigger_handle.execute(sender_name_fetch, sender_account_number)
    name_fetch_result = trigger_handle.fetchone()
    sender_name_0 = name_fetch_result[0]
    sender_name_1 = str(sender_name_0)
    sender_account = sender_acc_input

    # 3) Receiver's Name fetch
    receiver_name_fetch = "SELECT Name FROM Customers WHERE Account_Number = %s"
    receiver_account_number_1 = (str(receiver_acc_num),)
    trigger_handle.execute(receiver_name_fetch, receiver_account_number_1)
    name_fetch_result_r = trigger_handle.fetchone()
    receiver_name_0 = name_fetch_result[0]
    receiver_name_1 = str(sender_name_0)

    # 4) Receivers Email fetch
    receiver_email_fetch_1 = "SELECT Email FROM Customers WHERE Account_Number = %s"
    receiver_account_number_1 = (str(receiver_acc_num),)
    trigger_handle.execute(receiver_email_fetch_1, receiver_account_number_1)
    email_fetch_result_2 = trigger_handle.fetchone()
    receiver_email_01 = email_fetch_result_2[0]
    receiver_email_1a = str(receiver_email_01)

    # ================================================================================
    # We verify receiver's account details
    try:
        verify_receiver = "SELECT Name FROM Customers WHERE Account_Number = %s"
        receiver_name_value = (str(receiver_acc_num),)
        trigger_handle.execute(verify_receiver, receiver_name_value)
        name_display_tpl = trigger_handle.fetchone()
        receiver_name = name_display_tpl[0]
        print(f"You are sending {transfer_amount} to {receiver_name} ({receiver_acc_num}). \n"
              f" Do you confirm this to be correct? Yes/No")
        verify_response = input("")
        if verify_response.lower() == "yes":
            # We debit sender's account
            # first, we get account balance of sender
            try:
                sender_balance_query = "SELECT Balance FROM Customers WHERE Account_Number = %s"
                sender_bal_value = (str(sender_acc_input),)  # convert the input to string
                trigger_handle.execute(sender_balance_query, sender_bal_value)
                sender_acc_bal_tpl = trigger_handle.fetchone()
                sender_acc_bal = sender_acc_bal_tpl[0]
            except Exception as ex:
                print("Invalid Entry-5! Operation terminated.")
                print(ex)
                quit()

            # 1. We convert the string tuple to float for calculation
            sender_old_bal = float(sender_acc_bal)
            sender_new_bal = sender_old_bal - transformed_transfer_amount
            if sender_new_bal < 1:
                print("Sorry, you do not have sufficient funds to carry out this transaction."
                      "Kindly fund your account and try again.")
                quit()
            else:
                # We update sender's record on database with new balance
                try:
                    update_query = "UPDATE Customers SET Balance = %s WHERE Account_Number = %s"
                    sender_new_bal_value = (str(sender_new_bal), str(sender_acc_input))  # convert the input to string
                    trigger_handle.execute(update_query, sender_new_bal_value)
                    trigger.commit()
                except Exception as ex:
                    print("Invalid Entry-6! Operation terminated.")
                    print(ex)
                    quit()

            # 2. We credit receiver's account with the imputed amount
            try:
                receiver_balance_query = "SELECT Balance FROM Customers WHERE Account_Number = %s"
                receiver_bal_value = (str(receiver_acc_num),)  # convert the input to string
                trigger_handle.execute(receiver_balance_query, receiver_bal_value)
                acc_bal_tpl = trigger_handle.fetchone()
                acc_bal = acc_bal_tpl[0]
            except Exception as ex:
                print("Invalid Entry-7! Operation terminated.")
                print(ex)
                quit()

            # 3. We convert the string tuple to float for calculation
            old_bal = float(acc_bal)
            new_bal = old_bal + transformed_transfer_amount

            # We update receiver's record on database with new balance
            try:
                update_query = "UPDATE Customers SET Balance = %s WHERE Account_Number = %s"
                new_bal_value = (str(new_bal), str(receiver_acc_num))  # convert the input to string
                trigger_handle.execute(update_query, new_bal_value)
                trigger.commit()
            except Exception as ex:
                print("Invalid Entry-8! Operation terminated.")
                print(ex)
                quit()

            print("Transaction successful!")

            print("===============================================\n")

        else:
            print("Transaction Cancelled.")


    except Exception as ex_note:
        print("Invalid Entry-9! Operation terminated.")
        print(ex_note)
        quit()

    # ==============Email Notification==================================================

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Function for sending to email notification to fund Sender
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    amount_received = transfer_amount

    def send_email(sender_email, sender_password, receiver_emails, subjects, messages):
        if len(receiver_emails) != len(subjects) or len(receiver_emails) != len(messages):
            raise ValueError("Number of recipients, subjects, and messages must be the same.")

        for receiver_email, subject, message in zip(receiver_emails, subjects, messages):
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
    receiver_emails = [f"{sender_email_1}", f"{receiver_email_1a}"]
    subjects = [f"Debit Alert [Transfer - {sender_account}]", f"Credit Alert [Transfer - {receiver_acc_num}]"]
    messages = [f"Dear {sender_name_1},\n"
                f"Your XBZ Bank has been debited.\n"
                f"You have transferred {transfer_amount} to {receiver_name}\n"
                f"Date: {tranx_date_time()}.\n"
                f"Description: {description}.\n"
                f"Your current account balance is now: {locale.currency(sender_new_bal, grouping=True)}\n"
                f"Thank you for banking with XBZ Bank Plc.",
                f"Dear {receiver_name},\n"
                f"Your account has been credited! \n"
                f"You have received {amount_received} from {sender_name_1}.\n"
                f"Date: {tranx_date_time()}.\n"
                f"Description: {description}.\n"
                f"Your current account balance is now: {locale.currency(new_bal, grouping=True)}.\n"
                f"Thank you for banking with XBZ Bank Plc."]

    # Send the emails
    send_email(sender_email, sender_password, receiver_emails, subjects, messages)
    print("Notification success.")
    print("===============================================\n")

