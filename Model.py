import View
import sqlite3
import datetime as dt
from datetime import timedelta
import pandas as pd


# Create Library Database
def connect_database():
    global library
    library = sqlite3.connect('LibraryDatabase.db')
    global c
    c = library.cursor()


def create_tables():
    # Librarian Table
    c.execute("""CREATE TABLE IF NOT EXISTS Librarians(
                    Name varchar,
                    Email varchar,
                    Password varchar,
                    `Phone number` int)
                    """)

    # User Table
    c.execute("""CREATE TABLE IF NOT EXISTS Users(
                    Name varchar,
                    Email varchar,
                    Password varchar,
                    `Phone number` varchar,
                    `Book checked out` varchar,
                    `Due date` DATE,
                    `Fees owed` float)
                    """)

    # Books Table
    c.execute("""CREATE TABLE IF NOT EXISTS Books(
                    Title varchar,
                    Author varchar,
                    `Publication Company` varchar,
                    `Checked out` DATE,
                    `Availability` varchar)
                    """)


# Storing newly added book - Current user and Rented date are "None" by default
def store_book():
    book_details = View.book_info()
    c.execute("INSERT INTO Books VALUES (?, ?, ?, ?, ?)", (book_details["title"],
                                                           book_details["author"],
                                                           book_details["public_comp"], None, "Available"))
    library.commit()


def delete_book():
    book_to_delete = View.retrieve_book()
    c.execute("SELECT * FROM Books WHERE Title=? COLLATE NOCASE", (book_to_delete,))
    book = c.fetchone()
    try:
        if book[4].lower() == "unavailable":
            print("Can't delete when the book is checked out")
        else:
            c.execute("DELETE FROM Books WHERE Title=? COLLATE NOCASE", (book_to_delete,))
            print("{} deleted successfully".format(book_to_delete))
    except:
        print("Error: Title may not exist")
    library.commit()


# Storing new librarian
def store_librarian():
    librarian_info = View.add_librarian()
    c.execute("SELECT * FROM Librarians WHERE Email=?", (librarian_info["email"],))
    person = c.fetchone()
    if person is None:
        c.execute("INSERT INTO Librarians VALUES (?, ?, ?, ?)", (librarian_info["name"],
                                                                 librarian_info["email"],
                                                                 librarian_info["pass_word"],
                                                                 librarian_info["phone_num"]))
        print("Librarian added successfully")
    else:
        print("ERROR: Account name already exists")
    library.commit()


# Storing new user
def store_user():
    user_details = View.add_user()
    c.execute("SELECT * FROM Users WHERE Email=?", (user_details["email"],))
    person = c.fetchone()
    if person is None:
        c.execute("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?)", (user_details["name"],
                                                                     user_details["email"],
                                                                     user_details["pass_word"],
                                                                     user_details["phone_num"],
                                                                     None,
                                                                     None,
                                                                     0))
        print("User added successfully")
    else:
        print("ERROR: Account name already exists")
    library.commit()


def sign_in():
    details = View.user_login()
    try:
        c.execute("SELECT * FROM Users WHERE Email=?", (details[0],))
        user = c.fetchone()
        if user is None:
            print("Email does not match anyone in the system")
            key = False
        # Check if password matches
        elif details[1] == user[2]:
            # Print first name
            print("Welcome back {}".format(user[0]))
            print(pd.DataFrame(user))
            key = True
        else:
            raise ValueError
    except ValueError:
        print("Email or password is wrong")
        key = False
    # details[0], which is the email, is used for purposes related to checking out books
    return [details[0], key]


def librarian_sign_in():
    details = View.user_login()
    try:
        c.execute("SELECT * FROM Librarians WHERE Email=?", (details[0],))
        user = c.fetchone()
        if user is None:
            print("Email does not match anyone in the system")
        # Check if password matches
            key = False
        elif details[1] == user[2]:
            # Print first name
            print("Welcome back {}".format(user[0]))
            print(pd.DataFrame(user))
            key = True
        else:
            raise ValueError
    except ValueError:
        print("Email or password is wrong")
        key = False
    # details[0], which is the email, is used for purposes related to checking out books
    return [details[0], key]

#######################
#    USER ACTIVITY    #
#######################


def rent_book(user):
    book_title = View.retrieve_book()
    c.execute("SELECT * FROM Books WHERE Title=? COLLATE NOCASE", (book_title,))
    the_book = c.fetchone()
    if the_book is None:
        print("Book does not exist")
    elif the_book[4].lower() == "available":
        today = dt.datetime.now().date()
        due_date = today + timedelta(days=20)
        c.execute("UPDATE Books SET Availability=?  WHERE Title=? COLLATE NOCASE", ("Unavailable", book_title))
        c.execute("UPDATE Books SET `Checked out`=? WHERE Title=? COLLATE NOCASE", (today, book_title))
        c.execute("UPDATE Users SET `Book checked out`=? WHERE Email=?", (book_title, user))
        c.execute("UPDATE Users SET `Due date`=? WHERE Email=?", (due_date, user))
        print("Order successful")
    else:
        print("Book is unavailable")

    library.commit()


def return_book(user):
    book_title = View.retrieve_book()
    c.execute("SELECT * FROM Users WHERE Email=?", (user,))
    user_details = c.fetchone()
    if user_details[4].lower() == book_title.lower():
        # CALLING FEES FUNCTION BELOW
        fine = fees(book_title, user)
        c.execute("UPDATE Books SET Availability=?  WHERE Title=? COLLATE NOCASE", ("Available", book_title))
        c.execute("UPDATE Books SET `Checked out`=? WHERE Title=? COLLATE NOCASE", (None, book_title))
        c.execute("UPDATE Users SET `Book checked out`=? WHERE Email=?", (None, user))
        c.execute("UPDATE Users SET `Due date`=? WHERE Email=?", (None, user))
        print("Thank you for returning this book")
        print("You have $ {} worth of fines".format(float(fine)))

    else:
        print("You have not checked out this book")
    library.commit()


def fees(book_title, user):
    today = dt.datetime.today()
    c.execute("SELECT * FROM Books WHERE Title=? COLLATE NOCASE", (book_title,))
    book = c.fetchone()
    # tomorrow = dt.datetime(2019, 10, 29) <<< Test Variable
    date_checkedout = dt.datetime.strptime(book[3], "%Y-%m-%d")
    date_diff = (today - date_checkedout).days
    # date_diff = abs(tomorrow - date_checkedout).days <<< Test variable
    fine = 0
    if date_diff >= 20:
        fine += 20
        extra_days = date_diff - 20
        days_with_fine = extra_days // 5
        for i in range(0, days_with_fine):
            fine += 20 + (5 * i)
    c.execute("UPDATE Users SET `Fees owed`=? WHERE Email=?", (float(fine), user))
    return fine


def update_user_email(user):
    new_email = View.update_email()
    c.execute("UPDATE Users SET Email=? WHERE Email=?", (new_email, user))
    print("Account updated")
    print("*****PRESS QUIT AND SIGN BACK IN BEFORE CONTINUING*****")
    library.commit()


def update_user_phone(user):
    new_phone = View.update_phone_number()
    c.execute("UPDATE Users SET `Phone number`=? WHERE Email=?", (new_phone, user))
    print("Account updated")
    print("*****PRESS QUIT AND SIGN BACK IN BEFORE CONTINUING*****")
    library.commit()


def delete_user(user):
    pass_word = View.delete_info()
    try:
        c.execute("SELECT * FROM Users WHERE Email=?", (user,))
        user_info = c.fetchone()
        # Check if password matches
        if pass_word == user_info[2]:
            c.execute("DELETE FROM Users WHERE Email=?", (user,))
            print("User {} deleted".format(user))
        else:
            raise ValueError
    except ValueError:
        print("Password is wrong: Could not delete account")
    library.commit()
    # details[0], which is the email, is used for purposes related to checking out books


def update_book_author():
    try:
        book_title = View.retrieve_book()
        c.execute("SELECT * FROM Books WHERE Title=? COLLATE NOCASE", (book_title,))
        the_book = c.fetchone()
        if the_book[4].lower() == "unavailable":
            print("Can't edit when the book is checked out")
        else:
            print("Please enter book's new author")
            new_author = View.retrieve_author()
            c.execute("UPDATE Books SET Author=? WHERE Title=? COLLATE NOCASE", (new_author, book_title))
    except:
        print("Error with the book you are trying to change: Title may not exist")
    library.commit()


def update_book_title():
    try:
        book_title = View.retrieve_book()
        c.execute("SELECT * FROM Books WHERE Title=? COLLATE NOCASE", (book_title,))
        the_book = c.fetchone()
        if the_book[4].lower() == "unavailable":
            print("Can't edit when the book is checked out")
        else:
            print("Please enter books new title")
            new_title = View.retrieve_book()
            c.execute("UPDATE Books SET Title=? WHERE Title=? COLLATE NOCASE", (new_title, book_title))
    except:
        print("Error with the book you are trying to change: Title may not exist")
    library.commit()


def view_all_books():
    c.execute("SELECT * FROM Books")
    books = c.fetchall()
    print(pd.DataFrame(books))

