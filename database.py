import sqlite3
from sqlite3 import Error




class Database:
    """All database connections and functionality"""
    def __init__(self, db_file):
        self.conn = self.create_connection(db_file)
        self.sql_create_users = """ CREATE TABLE IF NOT EXISTS users(
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    surname text NOT NULL,
                                    age integer NOT NULL,
                                    card_id integer NOT NULL,
                                    password text NOT NULL

                                );"""
        self.create_table(self.conn,self.sql_create_users)

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
        """Validate password to complete login"""

        cur = self.conn.cursor()

        cur.execute("SELECT * FROM users WHERE card_id = ?", (card_id,))
        row = cur.fetchone()

        if row[5] == password:
            return True
        return False

