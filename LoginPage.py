def loud_users():
    # This function loads all existing users from the file "Customer.txt"
    users = {} # Create an empty dictionary to store usernames and passwords
    try:
        with open("Customer.txt","r") as file:
            for x in file:
                if "," in x:
                    username, password = x.strip().split(",",1)
                    users[username] = password

    except FileNotFoundError:
        pass
    return users

def loginpage(users):
    # This function handles the login system for both customers and admins.
    # It returns:
    # ("customer", username) if a customer logs in
    # ("admin", None) if an admin logs in
    print("Weclome to the Bus Ticket App")
    admin_customer = input("\nPress 1 for customer\nPress 2 for Admin\n")
    while admin_customer != "1" and admin_customer != "2":
        print("Invalid input. Please try again.")
        admin_customer = input("\nPress 1 for customer\nPress 2 for Admin\n")
    if admin_customer == "1":
        new = input("\nAre you a new customer? y/n\n")
        while new != "y" and new != "n":
            print("Invalid input. Please try again.")
            new = input("\nAre you a new customer? y/n\n")
        if new == "y":
            new_username = input("\nCreat a new username\n")
            while new_username in users or new_username.strip() == "":
                print("Uersname cannot be empty\nUsername already exists. Please try again.")
                new_username = input("\nCreat a new username\n")
            new_password = input("\nCreat a new password\n")
            while len(new_password) < 8:
                print("Password must be at least 8 characters long")
                new_password = input("\nCreat a new password\n")


            with open("Customer.txt","a") as file:
                file.write(new_username + "," + new_password + "\n")

            users[new_username] = new_password
            return "customer",new_username

        elif new == "n":
            username = input("\nEnter your username\n")
            while username not in users:
                print("Invalid username. Please try again.")
                username = input("\nEnter your username\n")
            password = input("\nEnter your password\n")
            while password != users[username]:
                print("password is incorrect. Please try again.")
                password = input("\nEnter your password\n")

            return "customer",username






    elif admin_customer == "2":
        input("press enter to continue")
        return "admin", None
