import json

from pathlib import Path
from datetime import datetime, timedelta

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from sqlalchemy import text, create_engine


path_file = Path(__file__)
with open(path_file.parent.parent / "config.json") as f:
    config = json.load(f)


class Database:
    def __init__(self):
        self.__create_database(
            dbname=config["POSTGRES"]["DBNAME"],
            user=config["POSTGRES"]["USER"],
            password=config["POSTGRES"]["PASSWORD"],
            host=config["POSTGRES"]["HOST"],
            port=config["POSTGRES"]["PORT"]
        )
        self.__conn = None
        self.__cur = None
        self.__current_user = None

    def __create_database(self, dbname, user, password, host, port):
        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/')

        with engine.connect() as connection:
            connection.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            result = connection.execute(text(f"SELECT datname FROM pg_database WHERE datname = '{dbname}'")).fetchone()
            
            if result:
                print(f"Database {dbname} already exists!")
                print(f"Für Debugging: {result}")
            else:
                connection.execute(text(f"CREATE DATABASE {dbname}"))

                conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
                self.__fill_database(path_file.parent / "ddl.sql", conn)
                conn.close()

                print(f"Database {dbname} created successfully!")

        engine.dispose()

    def __fill_database(self, file_path, conn):
        cursor = conn.cursor()

        with open(file_path, 'r') as file:
            sql = file.read()

        sql_commands = sql.split(';')
        for command in sql_commands:
            try:
                if command.strip() != '':
                    cursor.execute(command)
                    print(f"SQL command executed successfully: {command}")
                    conn.commit()
            except Exception as e:
                print(f"An error occurred while executing the SQL command: {e}")

    # ----- Utilities
    def __connect(self):
        self.__conn = psycopg2.connect(
            dbname=config["POSTGRES"]["DBNAME"],
            user=config["POSTGRES"]["USER"],
            password=config["POSTGRES"]["PASSWORD"],
            host=config["POSTGRES"]["HOST"],
            port=config["POSTGRES"]["PORT"]
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

    # @__connection_manager
    # def database_dump(self):
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

    @__connection_manager
    def delete_userdata(self):
        self.__cur.execute(
            f"DELETE FROM \"user\"\
            WHERE username = '{self.__current_user}';"
        )

    # ---- Functions that return data for page rendering
    @__connection_manager
    def get_active_items(self):
        self.__cur.execute(
            f"""
                SELECT 
                    item_status.*,
	                CASE
                        WHEN filtered_watchlist.user_username is NUll THEN 0
                        ELSE 1
                    END is_watchlist
                FROM 
                    items_status 
                    LEFT JOIN (SELECT * FROM watchlist WHERE user_username = '{self.__current_user}') AS filtered_watchlist 
                        ON items_status.item_id = filtered_watchlist.item_id 
                WHERE time_left > 0;
            """
            )
        return self.__fetch_data_from_cursor()

    def get_watchlist_items(self):
        active_items = self.get_active_items()
        return [item for item in active_items if item["is_watchlist"]]
    
    @__connection_manager
    def get_personal_data(self):
        """For tab Personal Data under user profile"""
        self.__cur.execute(
            f"SELECT * FROM \"user\" WHERE username = {self.__current_user};"
        )
        return self.__fetch_data_from_cursor()
    
    @__connection_manager
    def get_user_stats(self):
        """For stats on top of tabs won_auctions, feedback and payment under user profile"""
        self.__cur.execute(
            f"REFRESH MATERIALIZED VIEW user_statistics;\
              SELECT * FROM user_statistics WHERE username = {self.__current_user};"
        )
        return self.__fetch_data_from_cursor()

    @__connection_manager
    def get_won_auctions(self):
        self.__cur.execute(f"""
        SELECT bid.item_id, title, description, image_path, amount
        FROM
            bid
            CROSS JOIN (SELECT * FROM items_status WHERE time_left < 0) AS past_auctions
        WHERE 
            bid.item_id = past_auctions.item_id AND 
            bid.amount = past_auctions.highest_bid 
            AND user_username = '{self.__current_user}'
        """)

        return self.__fetch_data_from_cursor()

    @__connection_manager
    def get_feedback(self):
        self.__cur.execute(f"SELECT * FROM feedback WHERE receiver = '{self.__current_user}';")
        
        return self.__fetch_data_from_cursor()

    @__connection_manager
    def get_payments(self):
        self.__cur.execute(f"""
        SELECT 
            item_id,
            item.user_username AS seller,
            payment.user_username AS buyer,
            date,
            type,
            amount,
            CASE 
                WHEN payment.user_username = '{self.__current_user}' THEN 'Purchase'
                ELSE 'Sale'
            END action
            
        FROM payment
        JOIN item ON item.id = payment.item_id
        WHERE payment.user_username = '{self.__current_user}' OR item.user_username = '{self.__current_user}'
        """)
        
        return self.__fetch_data_from_cursor()
        