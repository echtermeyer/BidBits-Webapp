import os
import json

from pathlib import Path
from datetime import datetime, timedelta

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from sqlalchemy import text, create_engine


class Database:
    def __init__(self):
        self.__conn = None
        self.__cur = None
        self.__current_user = None

    # ----- Utilities
    def __connect(self):
        self.__conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT")
        )

        self.__cur = self.__conn.cursor()

    def __disconnect(self):
        self.__conn.commit()
        self.__cur.close()
        self.__conn.close()

    def __connection_manager(func):
        """
        Decorator function that handles database connection using psycopg2. 
        It also checks if an auction has ended. If thats the case: document payment. 
        """

        def wrapper(self, *args, **kwargs):
            try:
                self.__connect()
                # Check if an auction has endet with a bid that does not has a payment yet
                self.__cur.execute(
                    f"""
                    SELECT 
                        highest_bid AS amount, 
                        item.endtime AS date,
                        CASE FLOOR(RANDOM() * 3)
                            WHEN 0 THEN 'Cash'
                            WHEN 1 THEN 'Credit Card'
                            WHEN 2 THEN 'Paypal'
                        END AS type,	
                        items_status.highest_bidder AS user_username,
                        items_status.item_id
                        
                    FROM items_status
                    LEFT JOIN payment ON items_status.item_id = payment.item_id
                    JOIN item ON items_status.item_id = item.id
                    WHERE time_left <= 0 AND payment.amount IS NULL AND highest_bid > 0
                    """
                )
                # Document Payment for all auctions that ran out
                for auction in self.__fetch_data_from_cursor():
                    print(auction)
                    self.__cur.execute(
                    f"""INSERT INTO payment VALUES ({auction["amount"]}, '{auction["date"]}', '{auction["type"]}', '{auction["user_username"]}', {auction["item_id"]})"""
                    )

                # Execute db query
                result = func(self, *args, **kwargs)
                self.__disconnect()
                return (True, "success") if result is None else result
            except Exception as e:
                print(e)
                Warning(
                    f"\n!== Something went wrong. Might be a database error. Check datatypes ==!\n{e}")
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
        self.__cur.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
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

        self.__cur.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        print(
            f"\n == Successfully Created Tables == \n{[x[0] for x in self.__cur.fetchall()]}\n")

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
        self.__cur.execute(
            f"SELECT * FROM \"user\" WHERE username = '{username}' AND password = '{password}'")
        if self.__cur.fetchall():
            self.__current_user = username
        else:
            return (False, "Incorrect username or password")

    # TODO: Error: Database error. Check Data Types.duplicate key value violates unique constraint "item_pkey" DETAIL: Key (id)=(1) already exists.
    @__connection_manager
    def create_item(self, title, description, category, start_price, auction_duration, image):
        if auction_duration <= 1:
            return (False, "Minimum auction duration is 2 days")
        
        self.__cur.execute(
            f"SELECT id from categorisation WHERE category = '{category.split(' - ')[0]}' AND subcategory = '{category.split(' - ')[1]}'")
        category_id, = self.__cur.fetchall()[0]
        self.__cur.execute(
            f"INSERT INTO Item (name, description, startingPrice, startTime, endTime, imageUrl, user_username, category_id) VALUES\
            ('{title}', '{description}', '{start_price}', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}', '{(datetime.now() + timedelta(days=auction_duration)).strftime('%Y-%m-%d %H:%M:%S')}', '{image.name}', '{self.__current_user}', '{category_id}')"
        )

    @__connection_manager
    def place_bid(self, amount, item_id):
        print(0)
        self.__cur.execute(
            f"SELECT highest_bid, highest_bidder, seller FROM items_status WHERE item_id = {item_id}"
        )
        data = self.__fetch_data_from_cursor()
        print(data)
        if data[0]["seller"] == self.__current_user:
            return (False, "You can't buy your own stuff")
        if data[0]["highest_bidder"] == self.__current_user:
            return (False, "You can't outbid yourself")
        print(2)
        if data[0]["highest_bid"] > int(amount):
            print(22)
            return (False, "Your bid must exceed the highest bid")

        # Place Bid
        self.__cur.execute(
            f"INSERT INTO bid (amount, bidtime, user_username, item_id) VALUES\
            ('{amount}', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}', '{self.__current_user}', '{item_id}')"
        )

    @__connection_manager
    def give_feedback(self, item_id, rating, comment):
        self.__cur.execute(
            f"""
                SELECT 
                    CASE 
                        WHEN buyer = {self.__current_user} THEN seller
                        ELSE buyer
                    END receiver
                FROM items_status 
                WHERE item_id = {item_id};
            """
        )
        receiver = self.__fetch_data_from_cursor()[0]["receiver"]
        self.__cur.execute(
            f"INSERT INTO feedback (rating, comment, sender, receiver) VALUES ({rating}, '{comment}', {self.__current_user}, {receiver})"
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
        print(email, first_name, last_name, address, phone)
        all_inputs = {"email": email, "firstname": first_name,
                      "lastname": last_name, "address": address, "phone": phone}
        filled_inputs = ", ".join(
            [f"{key} = '{value}'" for key, value in all_inputs.items() if value is not None])
        print(filled_inputs)
        self.__cur.execute(
            f"UPDATE \"user\" SET {filled_inputs} WHERE username = '{self.__current_user}';"
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
    def get_categories(self):
        self.__cur.execute(
            f"SELECT category || ' - ' || subcategory AS category FROM categorisation"
        )
        return [x["category"] for x in self.__fetch_data_from_cursor()]

    @__connection_manager
    def get_active_items(self):
        self.__cur.execute(
            f"""
                SELECT 
                    items_status.*,
                    CASE
                        WHEN filtered_watchlist.user_username is NUll THEN 0
                        ELSE 1
                    END as is_watchlist
                FROM 
                    items_status 
                    LEFT JOIN (SELECT * FROM watchlist WHERE user_username = '{self.__current_user}') AS filtered_watchlist 
                        ON items_status.item_id = filtered_watchlist.item_id 
                WHERE items_status.time_left > 0;
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
            f"SELECT * FROM \"user\" WHERE username = '{self.__current_user}';"
        )
        return self.__fetch_data_from_cursor()

    @__connection_manager
    def get_user_stats(self):
        """For stats on top of tabs won_auctions, feedback and payment under user profile"""
        self.__cur.execute(
            f"REFRESH MATERIALIZED VIEW user_statistics;\
              SELECT * FROM user_statistics WHERE username = '{self.__current_user}';"
        )
        return self.__fetch_data_from_cursor()

    @__connection_manager
    def get_my_auctions(self):
        self.__cur.execute(f"""
		SELECT item_id, title, description, image_path, highest_bid AS amount, 
			CASE 
				WHEN highest_bidder = '{self.__current_user}' THEN 'buyer'
				WHEN seller = '{self.__current_user}' THEN 'seller'
			END AS role
		FROM items_status 
		WHERE time_left < 0
		AND highest_bidder = '{self.__current_user}' OR seller = '{self.__current_user}';
        """)

        return self.__fetch_data_from_cursor()

    @__connection_manager
    def get_feedback(self):
        self.__cur.execute(
            f"SELECT * FROM feedback WHERE receiver = '{self.__current_user}';")

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
            END AS action
            
        FROM payment
        JOIN item ON item.id = payment.item_id
        WHERE payment.user_username = '{self.__current_user}' OR item.user_username = '{self.__current_user}'
        """)

        return self.__fetch_data_from_cursor()
