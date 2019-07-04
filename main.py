import sys

from database import Database
class Menu:
    """Display and choose all possible scenarios"""

    def input_name(self):

        while True:
            name = input("Please provide your name:\n")
            if len(name) >2:
                name = name[0].upper() + name[1:]
                name = name.strip()
                return name
            else:
                print("Name has to be at least two characters")


    def input_surname(self):
        while True:
            surname = input("Please provide your surname:\n")
            if len(surname) >2:
                surname = surname[0].upper() + surname[1:]
                surname = surname.strip()
                return surname
            else:
                print("Surname has to be at least two characters")

    def input_age(self):
        while True:
            age = input("Please provide your age:\n")
            if age.isnumeric():
                if int(age) < 12:
                    print("You are too young to have a card")
                elif int(age) > 120:
                    print("You are too old to have a card")
                else:
                    return age
            else:
                print("Age is not valid. Please provide a number between 12 and 120.")

    def input_password(self):
        password = input("Please establish new password:\n")
        while True:
            password_check = input("Repeat the password:\n")
            if password == password_check:
                return password
            print("Wrong!")

    def input_card_id(self):
        while True:
            card_id = input("Please provide your own Card ID ((Q) to Quit):\n")
            if card_id.isnumeric():
                if len(card_id) == 4:
                    return card_id
                else:
                    print("Card ID has to be exactly 4 digits!")
            elif card_id.upper() == "Q":
                return None
            else:
                print("Card ID has to be a number!")




    def new_user(self):
        """Create new user if valid data"""
        name = self.input_name()
        surname = self.input_surname()
        age = self.input_age()
        password = self.input_password()
        self.db.insert_user(name,surname,age,password)

    def login_account(self):

        self.card_id = self.input_card_id()
        if self.card_id == None:
            return False
        if not self.db.check_card_id(self.card_id):
            print("Could not find Card ID: {0}".format(self.card_id))
            return False
        password = input("Please provide password:\n")
        if not self.db.check_password(self.card_id,password):
            print("Password is incorrect!")
            return False
        return True


    def account_menu(self):
        condition = True
        self.db = Database("database.db")

        while condition:

            print("""Choose:
                    1. I am a new user (CREATE ACCOUNT)
                    2. I already have an account (LOG IN)
                    3. List of recent accounts
                    4. Exit Application""")
            option = input("")
            if option == "1":
                self.new_user()

            elif option == "2":
                if self.login_account():
                    self.login_menu()

            elif option == "3":
                self.db.list_of_accounts()

            elif option == "4":
                print("Bye!")
                sys.exit()

            else:
                print("Please provide a correct option")

    def login_menu(self):
        """This menu appears when the user has successfully logged in"""
        print("\nWelcome {0}! You have successfull logged into your account".format(self.db.return_user_name(self.card_id)))

        self.display_active_tickets()



        condition = True
        while condition:

            print("""Choose:
              1. My personal data
              2. My active tickets
              3. Change password or personal data
              4. Buy a ticket
              5. Delete account
              6. Log out
              7. Exit Application""")
            option = input("")

            if option == "1":
                self.db.present_personal_data(self.card_id)
            elif option == "2":
                self.display_active_tickets()
                print("\n\n")
                n = input("Press Enter...")
            elif option == "3":
                self.change_personal_data_menu()
            elif option == "4":
                self.buy_ticket_menu()
            elif option == "5":
                if self.delete_account():
                    condition = False
            elif option == "6":
                condition = False
            elif option == "7":
                print("Bye!")
                sys.exit()
            else:
                print("Please provide a correct option")

    def delete_account(self):
        """Pernamently deletes user account with ticket references from database"""

        print("In order to delete your account, please provide Card ID and Password:\n")
        card_id = input("Card ID: ")
        if card_id == self.card_id:
            password = input("Password: ")
            if not self.db.check_password(self.card_id, password):
                print("Password is incorrect!")
                return False

            else:
                option = input("If you are sure to delete this account, put (Y): ")
                if option.upper() == "Y":
                    self.db.delete_account_from_db(self.card_id)
                    print("\nAccount has been deleted!")
                    return True
                else:
                    return False
        else:
            print("Card ID is incorrect!")
            return False
    def display_active_tickets(self):
        print("Active tickets:")
        condition = True
        for ticket_name in ['20 min','1 hour','Daily','Monthly']:
            if self.db.return_active_ticket(self.card_id,ticket_name):
                condition = False
                print("{0} is ticket active.".format(ticket_name))
        if condition:
            print("There are no active tickets\n")


    def change_personal_data_menu(self):
        condition = True
        while condition:
            print("""Choose:
            1. Change personal data
            2. Change password
            3. Back
            """)
            option = input("")

            if option == "1":
                self.change_name_and_surname()
            elif option == "2":
                self.change_password()
            elif option == "3":
                condition = False
            else:
                print("Please provide a correct option")

    def change_name_and_surname(self):
        """Change name and surname for logged user"""
        print("Your current name is {0}".format(self.db.get_user_record(self.card_id,1)))
        name = self.input_name()
        print("Your current surname is {0}".format(self.db.get_user_record(self.card_id,2)))
        surname = self.input_surname()
        self.db.update_name_and_surname(name,surname,self.card_id)

    def change_password(self):
        """Change password for logged user"""
        password = input("Please provide current password:\n")
        if not self.db.check_password(self.card_id, password):
            print("Password is incorrect!")
            return

        password = self.input_password()
        self.db.update_password(password,self.card_id)

    def buy_ticket_menu(self):
        condition = True
        while condition:
            print("""Choose:
                        1. 20 min ticket
                        2. 1 hour ticket
                        3. Daily Ticket
                        4. Monthly Ticket (30 days)
                        5. Back
                        """)
            option = input("")

            if option == "1":
                self.buy_ticket("20 min")
            elif option == "2":
                self.buy_ticket("1 hour")
            elif option == "3":
                self.buy_ticket("Daily")
            elif option == "4":
                self.buy_ticket("Monthly")
            elif option == "5":
                condition = False
            else:
                print("Please provide a correct option")

    def buy_ticket(self,ticket_name):
        if not self.db.return_active_ticket(self.card_id,ticket_name):
            ticket_prices = {'20 min':"2",'1 hour':'4','Daily':'10','Monthly':'150'}
            print("This ticket costs {0} units".format(ticket_prices[ticket_name]))
            answer = input("Put (Y) if you want to buy: ")

            if answer.upper() == "Y":
                self.db.buy_ticket(self.card_id,ticket_name)
                self.ticket_has_been_bought(ticket_name)

        else:
            print("This kind of ticket is already active. You cannot buy it unless it expires.\n")


    def ticket_has_been_bought(self, ticket_name):
        print("{0} ticket has been bought.\n\n\n".format(ticket_name))
        n = input("Press Enter to continue...")

if __name__ == '__main__':
    Menu().account_menu()

