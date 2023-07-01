import DatabaseConnection

trigger = DatabaseConnection.sql.connect(host=DatabaseConnection.host, user=DatabaseConnection.user,
                                         password=DatabaseConnection.password, database="Customers")
trigger_handle = trigger.cursor()