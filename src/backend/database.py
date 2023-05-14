import json
import psycopg2
from datetime import datetime, timedelta

from pathlib import Path

# Datenbank 'bidbits' muss manuell angelegt werden bevor der dump durchgeführt werden kann.

class Database:
    def __init__(self):
        self.__conn = None
        self.__cur = None
        self.__current_user = None

    # ----- Utilities
    def __connect(self):
        path_file = Path(__file__)

        path_secrets = path_file.parent.parent / "secrets.json"
        with path_secrets.open() as f:
            secrets = json.load(f)

        self.__conn = psycopg2.connect(
            dbname=secrets["POSTGRES"]["DBNAME"],
            user=secrets["POSTGRES"]["USER"],
            password=secrets["POSTGRES"]["PASSWORD"],
            host=secrets["POSTGRES"]["HOST"],
            port=secrets["POSTGRES"]["PORT"]
        )

        self.__cur = self.__conn.cursor()

    def __disconnect(self):
        self.__conn.commit()
        self.__cur.close()
        self.__conn.close()

    def __connection_manager(func):  
        """Decorator function that takes car of everything concerning the database connection"""      
        def wrapper(self, *args, **kwargs):
            try:
                self.__connect()
                result = func(self, *args, **kwargs)
                self.__disconnect()
                return (True, "success") if result is None else result
            except Exception as e:
                print(e)
                Warning(f"\n!== Something went wrong. Might be a database error. Check datatypes ==!\n{e}")
                return (False, f"Database error. Check Data Types.{e}")
            
        return wrapper

    def __fetch_data_from_cursor(self):
        """Used to transform the data in the cursor to a format which is applicable to dash: [{col_name, cell_val},...]"""
        return [
            {
                self.__cur.description[col_num][0]: entry[col_num]
                for col_num in range(len(entry))
            }
            for entry in self.__cur.fetchall()
        ]

    @__connection_manager
    def database_dump(self):
        # Check if tables already exist
        self.__cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        table_names = self.__cur.fetchall()

        if table_names.__len__() != 0:
            # Delete current tables and domains
            for table in table_names:
                self.__cur.execute(f'DROP TABLE "{table[0]}" CASCADE;')
            self.__cur.execute("DROP DOMAIN IF EXISTS EMAIL")
            self.__cur.execute("DROP DOMAIN IF EXISTS PAYMENT_TYPE")

        # Creating tables & domains and fill them with data
        with open("./ddl.sql", "r") as sql_file:
            sql = sql_file.read()
            print(sql)
            self.__cur.execute(sql)
            
        self.__cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        print(f"\n == Successfully Created Tables == \n{[x[0] for x in self.__cur.fetchall()]}\n")
  
    # ---- Functions that correspond to button clicks
    @__connection_manager
    def register(self, username, email, first_name, last_name, address, phone, password, conf_password):
        # Check if passwords match
        if password != conf_password:
            return (False, "Passwords do not match")
        
        # Register User
        self.__cur.execute(
            f"INSERT INTO \"user\" (username, email, password, firstName, lastName, address, phone) VALUES\
            ('{username}', '{email}', '{password}', '{first_name}', '{last_name}', '{address}', '{phone}')")

    @__connection_manager
    def login(self, username, password):
        self.__cur.execute(f"SELECT * FROM \"user\" WHERE username = '{username}' AND password = '{password}'")
        if self.__cur.fetchall():
            self.__current_user = username
        else:
            return (False, "Incorrect username or password")
    
    # TODO: Error: Database error. Check Data Types.duplicate key value violates unique constraint "item_pkey" DETAIL: Key (id)=(1) already exists.
    @__connection_manager
    def create_item(self, title, description, category, start_price, auction_duration, image):
        self.__cur.execute(f"SELECT id from categorisation WHERE category = '{category.split(' - ')[0]}' AND subcategory = '{category.split(' - ')[1]}'")
        category_id, = self.__cur.fetchall()[0]
        self.__cur.execute(
            f"INSERT INTO Item (name, description, startingPrice, startTime, endTime, imageUrl, user_username, category_id) VALUES\
            ('{title}', '{description}', '{start_price}', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}', '{(datetime.now() + timedelta(days=auction_duration)).strftime('%Y-%m-%d %H:%M:%S')}', '{image}', '{self.__current_user}', '{category_id}')"
        )

    @__connection_manager
    def place_bid(self, amount, item_id):
        # Check if amount > highest bid
        # TODO: Use MAX to retrieve the highest bid
        self.__cur.execute(
            f"SELECT amount FROM bid WHERE item_id = 2 ORDER BY bidtime desc LIMIT 1;"
        )
        current_bid, = self.__cur.fetchall()[0]
        if amount < current_bid:
            return (False, "Your bid must exceed the highest bid")
        
        # Place Bid
        self.__cur.execute(
            f"INSERT INTO bid (amount, bidtime, user_username, item_id) VALUES\
            ('{amount}', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}', '{self.__current_user}', '{item_id}')"
        )

    @__connection_manager
    def add_to_watchlist(self, item_id):
        self.__cur.execute(
            f"INSERT INTO watchlist VALUES ('{self.__current_user}', '{item_id}')"
        )

    @__connection_manager
    def remove_from_watchlist(self, item_id):
        self.__cur.execute(
            f"DELETE FROM watchlist WHERE user_username = '{self.__current_user}' AND item_id = '{item_id}'")

    @__connection_manager
    def update_userdata(self, email, first_name, last_name, address, phone):
        self.__cur.execute(
            f"UPDATE \"user\" SET email = '{email}', firstname = '{first_name}', lastname = '{last_name}', address = '{address}', phone = '{phone}'\
            WHERE username = '{self.__current_user}';"
        )
        print(self.__current_user, email, first_name)

    # ---- Functions that return data for page rendering
    @__connection_manager
    def show_user(self):
        self.__cur.execute(
            f"SELECT * FROM \"user\" WHERE username = {self.__current_user};"
        )
        return self.__fetch_data_from_cursor()

    # ---- TBD
    @__connection_manager
    def show_all_listings(self):
        # self.__cur.execute(
        #     f"SELECT * FROM item WHERE endtime > CURRENT_TIMESTAMP;"
        # )
        # result = self.__fetch_data_from_cursor()
        pass

    @__connection_manager
    def show_my_watchlist(self):
        pass

# db = Database()
# db.database_dump()