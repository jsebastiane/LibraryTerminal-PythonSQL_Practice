#################################################
#      USER, ADMIN, AND LIBRARIAN MENUS         #
#################################################


# HOME MENU
def print_home_menu():
    print("Press 1 - Log in as Librarian \nPress 2 - Log in as User \nPress 3 - Quit")
    while True:
        try:
            choice = int(input("Enter option: "))
            # Stops user from entering value greater than available options
            if choice <= 4:
                break
            else:
                raise ValueError
        except ValueError:
            print("Your entry was invalid, please try again")
    return choice


# LIBRARIAN
def librarian_action_menu():
    print("Press 1 - Add book \nPress 2 - Delete book \nPress 3 - View all books \nPress 4 - Update book author "
          "\nPress 5 - Update book title \nPress 6 - Quit")
    while True:
        try:
            choice = int(input("Enter option: "))
            # Stops user from entering value greater than available options
            if choice <= 6:
                break
            else:
                raise ValueError
        except ValueError:
            print("Your entry was invalid, please try again")
    return choice


def librarian_menu():
    print("Press 1 - Sign in \nPress 2 - Register \nPress 3 - Quit")
    while True:
        try:
            choice = int(input("Enter option: "))
            # Stops user from entering value greater than available options
            if choice <= 3:
                break
            else:
                raise ValueError
        except ValueError:
            print("Your entry was invalid, please try again")
    return choice


# USER
def user_menu():
    print("Press 1 - Sign in \nPress 2 - Register \nPress 3 - Quit")
    while True:
        try:
            choice = int(input("Enter option: "))
            # Stops user from entering value greater than available options
            if choice <= 3:
                break
            else:
                raise ValueError
        except ValueError:
            print("Your entry was invalid, please try again")
    return choice


# USER DETAILS UPDATE AND BOOK RENTAL MENU
def user_details_menu():
    print("Press 1 - Check out book \nPress 2 - Return book \nPress 3 - Update email"
          "\nPress 4 - Update phone number \nPress 5 - Delete user \nPress 6 - View all books \nPress 7 - Quit")
    while True:
        try:
            choice = int(input("Enter option: "))
            # Stops user from entering value greater than available options
            if choice <= 7:
                break
            else:
                raise ValueError
        except ValueError:
            print("Your entry was invalid, please try again")
    return choice

################################################
#      USER, LIBRARIAN, AND BOOK INFO INPUT    #
################################################


# LIBRARIAN DETAILS FOR ADDING LIBRARIAN
def add_librarian():
    librarian_details = dict()
    librarian_details["name"] = input("Please enter full name: ")
    librarian_details["email"] = input("Please enter email address: ")
    librarian_details["pass_word"] = input("Please enter password: ")
    librarian_details["phone_num"] = input("Please enter phone number: ")
    return librarian_details


# USER DETAILS FOR ADDING USER
def add_user():
    user_details = dict()
    user_details["name"] = input("Please enter full name: ")
    user_details["email"] = input("Please enter email address: ")
    user_details["pass_word"] = input("Please enter password: ")
    user_details["phone_num"] = input("Please enter phone number: ")
    return user_details


# BOOK DETAILS FOR ADDING BOOK
def book_info():
    book_details = dict()
    book_details["title"] = input("Please enter book title: ")
    book_details["author"] = input("Please enter book author: ")
    book_details["public_comp"] = input("Please enter book publication company: ")
    return book_details


# For rental and returns
def retrieve_book():
    book_title = input("Enter book title: ")
    return book_title


def retrieve_author():
    author = input("Enter new author: ")
    return author

##############################################
#      LOGIN FOR USERS AND LIBRARIANS        #
##############################################


def user_login():
    email = input("Enter Email: ")
    password = input("Enter Password: ")
    user_login_info = [email, password]
    return user_login_info


def librarian_login():
    email = input("Enter Email: ")
    password = input("Enter Password: ")
    librarian_login_info = [email, password]
    return librarian_login_info

############################
#      UPDATE DETAILS      #
############################


def update_email():
    new_email = input("Please enter you new email: ")
    return new_email


def update_phone_number():
    new_number = input("Please enter new phone number: ")
    return new_number


def delete_info():
    print("Enter your password to delete the account")
    pass_word = input("Your password: ")
    return pass_word


