import csv # This lets us read CSV files (spreadsheet-like files)

# This is the name of the text file where the admin’s price changes are saved
override_file = "price_overrides.txt"
# PRICE OVERRIDES (ADMIN CHANGES)
def loud_overrides():
    overrides = {}  # empty dictionary where we store overrides
    try:
        # Try to open the file. If it doesn't exist, the program will not crash.
        with open(override_file,"r") as f:
            for line in f:
                category,title,price = line.strip().split("|")
                # We store it in a dictionary using a pair (category, title) as the key
                overrides[(category,title)] = int(float(price) * 100)
    except FileNotFoundError:
        # If file does not exist, do nothing (no overrides saved yet)
        pass
    return overrides # return the dictionary of overrides

def save_overrides(overrides):
        #This function saves the admin’s changed prices to the text file.
        #It overwrites the file each time so it always stays up-to-date.
    with open(override_file,"w") as f:
        for (category,title),price in overrides.items():
            price_pounds = price/100
            f.write(f"{category}|{title}|{price_pounds:.2f}\n")

class Categorys:
    # A Category is like a box that holds information about a ticket category.
    # Example: "Single Tickets - City Zone" with its description.
    def __init__(self,code,title,description):
        self.title = title
        self.description = description
        self.code = code
    def __str__(self):
        # This controls what is shown when you print a Category object
        return f"{self.code} : {self.title} - {self.description}"

class TopUps:
    #  A TopUp is one ticket/top-up item.
    # This stores all details about a ticket.
    def __init__(self,code,topup_title,topup_description,topup_passenger,topup_passenger_name,topup_startdate,topup_enddate,topup_price_pence):
        self.code = code
        self.topup_title = topup_title
        self.topup_description = topup_description
        self.topup_passenger = topup_passenger
        self.topup_passenger_name = topup_passenger_name
        self.topup_startdate = topup_startdate
        self.topup_enddate = topup_enddate
        # The CSV stores price in pence, but you want pounds (£)
        # So we divide by 100.
        self.topup_price_pence = topup_price_pence/100
    def __str__(self):
        # This controls how a ticket prints on screen
        return (
                f"{self.topup_title}\n"
                f" {self.topup_description}\n"
                f" {self.topup_passenger}x{self.topup_passenger_name}\n"
                f"{self.topup_startdate} - {self.topup_enddate}\n"
                f"£{self.topup_price_pence:.2f}\n")

    #LOAD DATA FROM CSV

def load_categories():
    # This function reads the CSV file and returns a list of categories.
    # It avoids duplicates by using a set called 'seen'.

    categories = [] # list of category tuples like (code, title, description)
    seen = set() # set keeps track of titles we already added
    code = 1 # category number shown to the user

    with open("mobile_products.csv","r") as file:
        reader = csv.DictReader(file)
        for x in reader:
            title = x["category_title"]
            description = x["category_description"]

            # If we have not seen this category title before, add it
            if title not in seen:
                seen.add(title)
                categories.append((code,title,description))
                code = code + 1
    return categories

def loadtopups(overrides):
    # This reads the CSV and groups all tickets by category.
    # It also applies admin price overrides if they exist.
    topup_by_category = {}
    with open("mobile_products.csv","r") as file:
        reader = csv.DictReader(file)
        for x in reader:
            title = x["category_title"].strip()
            topup_title = x["topup_title"].strip()
            price_pence= int(x["topup_price_in_pence"])

            if (title,topup_title) in overrides:
                price_pence = overrides[(title,topup_title)]




            topup = TopUps(
            code = None,
            topup_title = x["topup_title"],
            topup_description = x["topup_description"],
            topup_passenger = x["topup_passenger_class_quantity"],
            topup_passenger_name = x["topup_passenger_class_name"],
            topup_startdate = x["topup_entitlement_start_date"],
            topup_enddate = x["topup_entitlement_end_date"],
            topup_price_pence = price_pence
            )

            if title not in topup_by_category:
                topup_by_category[title] = []
            topup_by_category[title].append(topup)
    return topup_by_category




cart = []
def main_menu_customer(overrides, username):
    customer_options = ["Purchase a ticket",
                        "View cart"]
    # Show menu options
    while True:
        for x,z in enumerate(customer_options,start=1):
            print(x,"",z.title())
        # Try reading the menu choice
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("\nPlease enter a valid choice.\n")
            continue

        # OPTION 1: PURCHASE
        if choice == 1:
            categories = load_categories()
            print("\n Here are the available categories:\n")
            for code,title,description in categories:
                print(f"{code}: {title} - {description}","\n")


            user_input = input("\nEnter your choice: ")
            # Repeat until valid number
            while not user_input.isdigit() or int(user_input) < 1 or int(user_input) > len(categories):
                print("\nPlease enter a valid category.\n")
                user_input = (input("Enter your choice: "))

            category_choice = int(user_input)
            # Find the chosen category title
            selcated_category = categories[category_choice-1][1].strip()

            # Load tickets grouped by category
            topups = loadtopups(overrides)

            if selcated_category not in topups:
                print("\nPlease enter a valid choice.\n")
                continue
            # Show tickets in that category
            print(f"\nHere are the available {selcated_category}:\n")
            for x,z in enumerate(topups[selcated_category],start=1):
                print(f"{x}.{z}")
            # Let user pick a ticket
            while True:
                user_input2 = input("\nEnter your choice: ")
                while not user_input2.isdigit() or int(user_input2) < 1 or int(user_input2) > len(topups):
                    print("\nPlease enter a valid choice.\n")
                    user_input2 = input("Enter your choice: ")

                ticket_choice = int(user_input2)
                selcated_ticket = topups[selcated_category][ticket_choice-1]

                print(f"\nYou have selected {selcated_ticket}")
                comfirm = input("\nWould you like to add the ticket to the cart? (y/n): ").strip().lower()
                while comfirm not in ("y", "n"):
                    print("\nPlease enter y or n.\n")
                    comfirm = input("Would you like to add the ticket to the cart? (y/n): ").strip().lower()

                if comfirm == "y":
                    cart.append(selcated_ticket)
                    print("\n Added.\n")
                    break
                else:
                    print("\n")
                    for x, z in enumerate(topups[selcated_category], start=1):
                        print(f"{x}.{z}")
        # OPTION 2: VIEW CART
        elif choice == 2:
            print("\nYour cart:\n")
            # If cart is empty, return to menu
            if len(cart) == 0:
                print("Your cart is empty\n")
                input("Press enter to continue")
                continue
            # Calculate total
            total = 0
            for x,item in enumerate(cart,start=1):
                print(f"{x}.{item.topup_title}\n{item.topup_description}\n""\n")
                total += item.topup_price_pence
            print(f"Your total is: £{total}\n")
            print("press (1) for  checkout")
            print("press (2) for main menu")
            cart_choice = input("\nEnter your choice: ")
            while cart_choice not in ("1", "2"):
                print("\nPlease enter 1 or 2.\n")
                cart_choice = input("Enter your choice: ")
            # Checkout
            if cart_choice == "1":
                confirm_checkout = input("Are you sure you would like to check out?\npress 1 to continue\npress 2 to cancel")
                while confirm_checkout not in ("1", "2"):
                    print("\nPlease enter 1 or 2.\n")
                    confirm_checkout = input("Are you sure you would like to check out?\npress 1 to continue\npress 2 to cancel")
                if confirm_checkout == "1":
                    save_checkout(username) # save purchase history
                    cart.clear()            # empty cart after checkout
                    print("\nCheckout complete.")
                    print("Thank you for using the buss ticket app.\n")
                    break
                else:
                    print("\nCheckout cancelled.\n")
                    continue

# 5) ADMIN MENU (CHANGE PRICE)

def admin_change_price(overrides):
    while True:
        categories = load_categories()
        for code,title,desc in categories:
            print(f"{code}: {title}")
        cat = input("Choose your category: ").strip()
        while not cat.isdigit() or int(cat) < 1 or int(cat) > len(categories):
            cat = input("Choose your category: ").strip()

        selcated_category = categories[int(cat) - 1][1].strip()

        # Load tickets with any overrides applied
        topups = loadtopups(overrides)
        tickets = topups[selcated_category]

        for x,i in enumerate(tickets,start=1):
            print(f"{x}: {i.topup_title}- £{i.topup_price_pence:.2f}")
        tic = input("\nChoose a ticket number: ").strip()
        while not tic.isdigit() or int(tic) < 1 or int(tic) > len(tickets):
            tic = input("\nChoose a ticket number: ").strip()
        selacted_ticket = tickets[int(tic) - 1]

        # Enter new price
        new_price =input("\nEnter the new price: ").strip()

        # Keep asking until a valid positive number is entered
        while True:
            try:
                new_price_float = float(new_price)
                if new_price_float <= 0:
                    print("\nPlease enter a price grater than 0.\n")
                    new_price = input("Enter the new price: ").strip()
                    continue
                break
            except ValueError:
                print("\nPlease enter a valid number.\n")
                new_price = input("Enter the new price: ").strip()
        # Convert pounds to pence
        new_price_pence = int(new_price_float*100)

        # Save override (category + ticket title)
        overrides[(selcated_category, selacted_ticket.topup_title)] = new_price_pence
        save_overrides(overrides)
        print("price has been updated and saved.\n")

        # Ask if admin wants to change another ticket
        again = input("\nDo you want to continue? (y/n): ").strip().lower()
        while again not in ("y", "n"):
            again = input("\nPlease enter y or n.\n")
        if again == "n":
            print("Logging out as admin...")
            break

def main_menu_admin(overrides):
    print("Welcome Administrator\n")
    print("please choose from the following options:\n")
    admins_options = input("press (1) to change tickets prices\nPress (2) to exit\n")
    while admins_options not in ("1", "2"):
        print("\nPlease enter 1 or 2.\n")
        print("please choose from the following options:\n")
        admins_options = input("press (1) to change tickets prices\nPress (2) to exit")
    if admins_options == "1":
        admin_change_price(overrides)
    elif admins_options == "2":
        pass

# 6) SAVE PURCHASE HISTORY
def save_checkout(username):
    with open ("purchase_history.txt", "a") as f:
        f.write("Checkout history for " + username + "\n")

        total = 0.0
        for x in cart:
            f.write(f"item: {x.topup_title} - {x.topup_price_pence:.2f}\n")
            total = total + x.topup_price_pence
        f.write(f"total: {total:.2f}\n\n")
