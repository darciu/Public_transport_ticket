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
                print("Name has to be longer than two characters")


    def input_surname(self):
        while True:
            surname = input("Please provide your surname:\n")
            if len(surname) >2:
                return surname
            else:
                print("Surname has to be longer than two characters")

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
        password = input("Please establish your password:\n")
        while True:
            password_check = input("Repeat your password:\n")
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
                    3. List of all users
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
              2. Change personal data
              3. Buy a ticket
              4. Log out
              5. Exit Application""")
            option = input("")

            if option == "1":
                self.db.present_personal_data(self.card_id)
            elif option == "2":
                pass
            elif option == "3":
                pass
            elif option == "4":
                condition = False
            elif option == "5":
                print("Bye!")
                sys.exit()
            else:
                print("Please provide a correct option")








if __name__ == '__main__':
    Menu().account_menu()



