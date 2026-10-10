# We are importing functions from other Python files so we can use them here.
from LoginPage import loud_users, loginpage
from main_menu import loud_overrides,main_menu_customer, main_menu_admin

# Load all users into a dictionary.
# Example result:
# {"omar": "12345678", "ahmed": "password123"}
users = loud_users()

# Run the login page.
# This returns TWO things:
# user_type = "customer" or "admin"
# username = customer username (or None if admin)
overrides = loud_overrides()

user_type, username = loginpage(users)
# If the user logged in as a customer, take them to the customer menu.
if user_type == "customer":
    customer = main_menu_customer(overrides, username)
# If the user logged in as an admin, take them to the admin menu.
elif user_type == "admin":
    admin = main_menu_admin(overrides)
