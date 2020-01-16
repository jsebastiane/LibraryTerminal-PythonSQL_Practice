import Model
import View

Model.connect_database()
Model.create_tables()

librarian_menudict = {1: Model.librarian_sign_in, 2: Model.store_librarian}
librarian_actions = {1: Model.store_book, 2: Model.delete_book, 3: Model.view_all_books, 4: Model.update_book_author,
                     5: Model.update_book_title}
user_menudict = {1: Model.sign_in, 2: Model.store_user}
user_actions = {1: Model.rent_book, 2: Model.return_book, 3: Model.update_user_email, 4: Model.update_user_phone,
                5: Model.delete_user, 6: Model.view_all_books}


def main_librarian_activity():
    main_lib_key = True
    while main_lib_key:
        choice_librarian = View.librarian_menu()
        if choice_librarian == 3:
            main_lib_key = False
        elif choice_librarian == 1:
            librarian = librarian_menudict[choice_librarian]()
            if librarian[1]:
                librarian_activity()
            else:
                main_lib_key = False
        elif choice_librarian == 2:
            librarian_menudict[choice_librarian]()


def librarian_activity():
    lib_key = True
    while lib_key is True:
        lib_choice = View.librarian_action_menu()
        if lib_choice == 6:
            lib_key = False
        else:
            librarian_actions[lib_choice]()


def main_user_activity():
    main_user_key = True
    while main_user_key:
        choice_user = View.user_menu()
        if choice_user == 3:
            main_user_key = False
        elif choice_user == 1:
            user = user_menudict[choice_user]()
            if user[1]:
                user_activity(user[0])
            else:
                main_user_key = False
        elif choice_user == 2:
            user_menudict[choice_user]()


def user_activity(user):
    user_key = True
    while user_key is True:
        choice_user = View.user_details_menu()
        if choice_user == 7:
            user_key = False
        elif choice_user == 6:
            user_actions[choice_user]()
        else:
            user_actions[choice_user](user)


###################################################################################
#        RUNNING PROGRAM - RECOMMENDED TO START AS LIBRARIAN AND ADD BOOKS        #
###################################################################################

# OPTIONS FOR USER WHEN ON 'HOME' PAGE
home_menudict = {1: main_librarian_activity, 2: main_user_activity}

key = True

while key is True:
    choice = View.print_home_menu()
    if choice == 3:
        break
    else:
        home_menudict[choice]()
