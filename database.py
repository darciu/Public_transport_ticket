import sqlite3
from sqlite3 import Error
from datetime import datetime, timedelta




class Database:
    """All database connections and functionality"""
    def __init__(self, db_file):
        self.conn = self.create_connection(db_file)
        self.conn.execute('PRAGMA foreign_keys = ON')
        sql_create_users = """ CREATE TABLE IF NOT EXISTS users(
                                    users_id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    surname text NOT NULL,
                                    age integer NOT NULL,
                                    card_id integer NOT NULL,
                                    password text NOT NULL

                                );"""

        sql_create_tickets = """CREATE TABLE IF NOT EXISTS tickets(
                                tickets_id integer PRIMARY KEY,
                                users_id integer NOT NULL,
                                ticket_name text NOT NULL,
                                ticket_start text NOT NULL,
                                ticket_end text NOT NULL,
                                FOREIGN KEY (users_id) REFERENCES users(users_id) ON DELETE CASCADE
                                )"""

#FOREIGN KEY users_id REFERENCES users(card_id) ON DELETE CASCADE
        self.create_table(self.conn, sql_create_users)

        self.create_table(self.conn , sql_create_tickets)

    def create_connection(self, db_file):
        """Returns connection object with database"""
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

    def insert_user(self,name,surname,age,password):

        sql = "INSERT INTO users(name,surname,age,card_id,password) VALUES(?,?,?,?,?)"
        cur = self.conn.cursor()

        cur.execute("SELECT count(*) as total FROM users")
        num = cur.fetchone()
        card_id = num[0] + 1501
        user_data = (name, surname, age,card_id,password)
        cur.execute(sql,user_data)
        self.conn.commit()
        print("Account has been successfully created.\nName {0}\nSurname {1}\nAge {2}\nCard ID {3}\n"
              "Please keep Card ID as it will be used to login to the system.".format(name,surname,age,card_id))

    def create_table(self,conn,sql_statement):
        """"""
        try:
            cur = conn.cursor()
            cur.execute(sql_statement)
        except Error as e:
            print(e)

    def check_card_id(self,card_id):
        """Check if card id exists in database"""

        cur = self.conn.cursor()

        cur.execute("SELECT * FROM users WHERE card_id = ?",(card_id,))
        row = cur.fetchone()

        if row == None:
            return False
        return True
    def check_password(self,card_id,password):
        """Validate password"""

        cur = self.conn.cursor()

        cur.execute("SELECT * FROM users WHERE card_id = ?", (card_id,))
        row = cur.fetchone()

        if row[5] == password:
            return True
        return False

    def list_of_accounts(self):

        cur = self.conn.cursor()

        cur.execute("SELECT * FROM users ORDER BY users_id DESC LIMIT 5")

        rows = cur.fetchall()

        if len(rows) == 0:
            print("There are no users!\n\n\n\n")
            n = input("Press Enter...")
        else:
            print("Most recent accounts:")
            for row in rows:

                print(row[1], row[2][0] + ". ID: " + str(row[4]))
            print("\n")

    def present_personal_data(self, card_id):

        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users WHERE card_id = ?",(card_id,))
        row = cur.fetchone()
        print("Name ", row[1])
        print("Surname ", row[2])
        print("Age ", row[3])
        print("Card ID", row[4])
        n = input("\n\n\nPress Enter to continue...")

    def get_user_record(self,card_id,column):
        """Returns column value for given card ID"""

        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users WHERE card_id = ?",(card_id,))
        row = cur.fetchone()
        return row[column]


    def update_name_and_surname(self,name,surname, card_id):
        try:
            cur = self.conn.cursor()
            sql = "UPDATE users SET name = ?, surname = ? WHERE card_id = ?"
            cur.execute(sql,(name,surname,card_id))
            self.conn.commit()
            print("User name and surname has been successfully updated")
        except:
            print("An error occured. Database could not be updated!")


    def update_password(self,password,card_id):
        try:
            cur = self.conn.cursor()
            sql = "UPDATE users SET password = ? WHERE card_id = ?"
            cur.execute(sql,(password,card_id))
            self.conn.commit()
            print("Password has been successfully updated")
        except:
            print("An error occured. Database could not be updated!")


    def buy_ticket(self,card_id,ticket_name):

        card_id = str(int(card_id) - 1500)
        cur = self.conn.cursor()
        sql = "INSERT INTO tickets(users_id, ticket_name, ticket_start, ticket_end) VALUES (?,?,?,?)"
        ticket_stat = str(datetime.now())
        ticket_end = self.ticket_end_date(ticket_name)
        ticket_data = (card_id,ticket_name,ticket_stat,ticket_end)
        cur.execute(sql,ticket_data)
        self.conn.commit()


    def ticket_end_date(self, ticket_name):
        """Returns ticket expiration time according to ticket type"""
        if ticket_name == "20 min":
            ticket_end = datetime.now() + timedelta(minutes=20)
            return ticket_end
        elif ticket_name == "1 hour":
            ticket_end = datetime.now() + timedelta(hours=1)
            return ticket_end
        elif ticket_name == "Daily":
            ticket_end = datetime.now() + timedelta(days=1)
            return ticket_end
        elif ticket_name == "Monthly":
            ticket_end = datetime.now() + timedelta(days=30)
            return ticket_end

    def return_user_name(self,card_id):

        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users WHERE card_id = ?", (card_id,))
        row = cur.fetchone()
        return row[1]

    def return_active_ticket(self,card_id,ticket_name):
        """Returns end date if particular ticket is active"""
        card_id = str(int(card_id) - 1500)
        n = datetime.now()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tickets WHERE users_id = ? AND ticket_name = ? AND ticket_end > ?",(card_id,ticket_name,str(n)))
        row = cur.fetchall()
        if len(row) > 0:
            return True
        return False

    def delete_account_from_db(self,card_id):

        cur = self.conn.cursor()
        cur.execute("DELETE FROM users WHERE card_id = ?",(card_id,))
        self.conn.commit()


