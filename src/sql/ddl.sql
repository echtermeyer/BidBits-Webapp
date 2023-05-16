-- Create Datatypes
CREATE DOMAIN EMAIL AS VARCHAR
    CHECK (VALUE LIKE '%@%.%');

CREATE DOMAIN PAYMENT_TYPE AS VARCHAR
    CHECK (value IN ('Paypal', 'Credit Card', 'Cash'));


-- Create Category table
CREATE TABLE Categorisation (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50) NOT NULL
);

-- Create User table
CREATE TABLE "user" (
    username VARCHAR(255) PRIMARY KEY,
    email EMAIL NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    name VARCHAR(100) GENERATED ALWAYS AS (firstName || ' ' ||lastName) STORED,
    address TEXT NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE
);

-- Create Item table
CREATE TABLE Item (
    id SERIAL KEY PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    startingPrice NUMERIC DEFAULT 0,
    startTime TIMESTAMP NOT NULL,
    endTime TIMESTAMP NOT NULL,
    imageUrl TEXT NOT NULL,
    user_username VARCHAR(50) REFERENCES "user"(username) 
        ON DELETE SET NULL,
    category_id INTEGER REFERENCES Categorisation(id) 
);

-- Create Bid table
CREATE TABLE Bid (
    id SERIAL PRIMARY KEY,
    amount NUMERIC NOT NULL,
    bidTime TIMESTAMP NOT NULL,
    user_username VARCHAR(50) REFERENCES "user"(username) 
        ON DELETE SET NULL,
    item_id INTEGER REFERENCES Item(id) 
);

-- Create Watchlist table
CREATE TABLE Watchlist (
    user_username VARCHAR(50) REFERENCES "user"(username) 
        ON DELETE CASCADE,
    item_id SERIAL REFERENCES Item(id), 
    CONSTRAINT unique_watchlist_entry UNIQUE (user_username, item_id)
);

-- Create Feedback table
CREATE TABLE Feedback (
    feedbackID SERIAL PRIMARY KEY,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 0 AND 10),
    comment TEXT,
    sender VARCHAR(50) REFERENCES "user"(username) 
        ON DELETE SET NULL,
    receiver VARCHAR(50) REFERENCES "user"(username) 
        ON DELETE SET NULL
);

-- Create Payment table
CREATE TABLE Payment (
    amount NUMERIC NOT NULL,
    date TIMESTAMP NOT NULL,
    type PAYMENT_TYPE NOT NULL,
    user_username VARCHAR(50) REFERENCES "user"(username)
        ON DELETE SET NULL,
    item_id INTEGER REFERENCES Item(id) 
);

-- Create items_status View
CREATE VIEW items_status AS
	SELECT 
		item.name AS title, 
		item.id AS item_id, 
		item.description, 
		item.imageUrl AS image_path,  
		EXTRACT(DAY FROM AGE(item.endtime, CURRENT_TIMESTAMP)) AS time_left,
		max_bids.highest_bid,
		bid.user_username AS highest_bidder,
		item.user_username AS seller
		
	FROM item 
	JOIN (SELECT item_id, MAX(amount) AS highest_bid FROM bid GROUP BY item_id) AS max_bids 
		ON item.id = max_bids.item_id
	JOIN bid
		ON bid.item_id = max_bids.item_id
		AND bid.amount = max_bids.highest_bid;

-- Create user_statistics materialized view (needs to be refreshed manually)
CREATE MATERIALIZED VIEW user_statistics AS
    SELECT 
        u.username,
        COALESCE(participated_auctions.participated_auctions, 0) AS participated_auctions,
        COALESCE(won_auctions.won_auctions, 0) AS won_auctions,
        COALESCE(CAST(average_feedback.average_rating AS INTEGER), 0) AS average_rating,
        COALESCE(total_expenses.total_expenses, 0) AS total_expenses,
        COALESCE(total_income.total_income, 0) AS total_income
    FROM "user" u
    LEFT JOIN (
        SELECT user_username, COUNT(DISTINCT item_id) AS participated_auctions
        FROM bid
        GROUP BY user_username
    ) AS participated_auctions ON u.username = participated_auctions.user_username
    LEFT JOIN (
        SELECT user_username, COUNT(DISTINCT bid.item_id) AS won_auctions
        FROM bid
        JOIN items_status ON bid.item_id = items_status.item_id AND bid.amount = items_status.highest_bid
        WHERE items_status.time_left < 0
        GROUP BY user_username
    ) AS won_auctions ON u.username = won_auctions.user_username
    LEFT JOIN (
        SELECT receiver, AVG(rating) AS average_rating
        FROM feedback
        GROUP BY receiver
    ) AS average_feedback ON u.username = average_feedback.receiver
    LEFT JOIN (
        SELECT user_username AS buyer, SUM(amount) AS total_expenses
        FROM payment
        GROUP BY user_username
    ) AS total_expenses ON u.username = total_expenses.buyer
    LEFT JOIN (
        SELECT item.user_username AS seller, SUM(amount) AS total_income
        FROM payment
        JOIN item ON item.id = payment.item_id
        GROUP BY item.user_username
    ) AS total_income ON u.username = total_income.seller;




INSERT INTO Categorisation VALUES
(1, 'Animals', 'Mammals'),
(2, 'Animals', 'Amphibians'),
(3, 'Antiquities', 'Boring old stuff'),
(4, 'Antiquities', 'Cool old stuff');

INSERT INTO "user" (username, email, password, firstName, lastName, address, phone) VALUES
('Karen', 'karen@astrology.com', 'godblessamerica', 'Karen', 'Nonyabis', '68161 Mannheim A1 14', '015789445571'),
('Alfie', 'alfie@burminghambakery.com', 'nevergivepowertothebigman', 'Alfonso', 'Solomons', '24220 Burmingham Kensington Road 11', '01578331212'),
('John', 'John.watson@gmail.com', 'thegameisafoot', 'John', 'Watson', '27615 London Baker Street 221b', '02295001922');



INSERT INTO Item VALUES
(1, 'Cat with large ears', 'This cat is a great listener. Buy it now!', 20, '2023-05-14 12:11:08', '2023-06-02 11:11:01', 'kitten.jpg', 'Karen', 1),
(2, 'The Amber Room', 'Look what I found under my bed. It is golden, it is good.', 1200420123, '2023-05-13 06:07:08', '2023-05-30 06:07:08', 'amber_room.jpg', 'Alfie', 4),
(3, 'A red bar stool', 'Good Chair, nice and comfy. Does not wobble.', 15, '2020-01-01 19:12:22', '2020-01-02 13:02:22', 'red_chair.jpg', 'Karen', 3);


INSERT INTO Bid (amount, bidTime, user_username, item_id) VALUES
(1200420124, '2023-05-13 09:10:11', 'Karen', 2),
(1300000000, '2023-05-13 12:13:14', 'John', 2),
(24, '1999-01-10 09:11:21', 'Alfie', 1),
(16, '2020-01-05 19:11:22', 'John', 3),
(18, '2020-01-09 20:12:52', 'Alfie', 3),
(19, '2020-01-11 21:00:00', 'John', 3);

INSERT INTO Watchlist VALUES
('Karen', 2),
('John', 2),
('Alfie', 1);

INSERT INTO Feedback VALUES
(1, 1, 'Karen sold me a wobbly chair, I am furious.', 'John', 'Karen'),
(2, 10, 'The small gentleman bought my crooked bar stool. What a good lad.', 'Karen', 'John');



INSERT INTO Payment VALUES
(42, '2020-01-02 13:02:22', 'Credit Card', 'John', 3);
