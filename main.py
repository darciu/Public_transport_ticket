import sys

from database import Database
class Menu:
    """Display and choose all possible scenarios"""

    def input_name(self):

        while True:
            name = input("Please provide your name:\n")
            if len(name) >2:
                return name
            else:
                print("Name has to be at least two characters")


    def input_surname(self):
        while True:
            surname = input("Please provide your surname:\n")
            if len(surname) >2:
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
            card_id = input("Please provide your own Card ID:\n")
            if card_id.isnumeric():
                if len(card_id) == 4:
                    return card_id
                else:
                    print("Card ID has to be exactly 4 digits!")
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
                    3. List of recent users
                    4. Exit Application""")
            option = input("")
            if option == "1":
                self.new_user()

            elif option == "2":
                if self.login_account():
                    print("You have successfull logged into your account!")
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
        condition = True
        while condition:

            print("""Choose:
              1. My personal data
              2. Change password or personal data
              3. Buy a ticket
              4. Log out
              5. Exit Application""")
            option = input("")

            if option == "1":
                self.db.present_personal_data(self.card_id)
            elif option == "2":
                self.change_personal_data_menu()
            elif option == "3":
                self.buy_ticket_menu()
            elif option == "4":
                condition = False
            elif option == "5":
                print("Bye!")
                sys.exit()
            else:
                print("Please provide a correct option")

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
                        4. Monthly Ticket
                        5. Back
                        """)
            option = input("")

            if option == "1":
                self.buy_ticket_20_min()
            elif option == "2":
                pass
            elif option == "3":
                pass
            elif option == "4":
                pass
            elif option == "5":
                condition = False
            else:
                print("Please provide a correct option")

    def buy_ticket_20_min(self):
        print("This ticket costs 2 units")
        answer = input("Put (Y) if you want to buy: ")
        if answer == "Y":
            self.db.buy_ticket(self.card_id,"20 min")

    def buy_ticket_hour(self):
        print("This ticket costs 4 units")
        answer = input("Put (Y) if you want to buy: ")
        if answer == "Y":
            self.db.buy_ticket(self.card_id,"1 hour")

    def buy_ticket_daily(self):
        print("This ticket costs 10 units")
        answer = input("Put (Y) if you want to buy: ")
        if answer == "Y":
            self.db.buy_ticket(self.card_id,"daily")

    def buy_ticket_monthly(self):
        print("This ticket costs 150 units")
        answer = input("Put (Y) if you want to buy: ")
        if answer == "Y":
            self.db.buy_ticket(self.card_id,"monthly")



if __name__ == '__main__':
    Menu().account_menu()



#przy zalogowaniu powiatanie + imię + ilość aktywnych biletów