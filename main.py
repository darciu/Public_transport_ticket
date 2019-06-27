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
                    print("Card ID is exactly 4 digits!")
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
        card_id = self.input_card_id()
        if not self.db.check_card_id(card_id):
            print("Could not find Card ID: {0}".format(card_id))
            return False
        password = input("Please provide password:\n")
        if not self.db.check_password(card_id,password):
            print("Password is incorrect!")
            return False
        return True
    def list_of_accounts(self):
        pass

    def account_menu(self):
        condition = True
        self.db = Database("database.db")

        while condition:

            print("""Choose:
                    1. I am a new user
                    2. I already have an account
                    3. List of all users
                    4. Exit""")
            option = input("")
            if option == "1":
                self.new_user()


            elif option == "2":
                if self.login_account():
                    print("All right!")


            elif option == "3":
                pass
                condition = False

            elif option == "4":
                print("Bye!")
                sys.exit()
            else:

                print("Please provide a correct option")

    def run(self):
        pass

    def display_options(self):
        print("""Choose scenario:
                1. """)



if __name__ == '__main__':
    Menu().account_menu()



