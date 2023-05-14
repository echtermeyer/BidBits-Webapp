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

INSERT INTO Categorisation VALUES
(1, 'Animals', 'Mammals'),
(2, 'Animals', 'Amphibians'),
(3, 'Antiquities', 'Boring old stuff'),
(4, 'Antiquities', 'Cool old stuff');


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

INSERT INTO "user" (username, email, password, firstName, lastName, address, phone) VALUES
('Karen', 'karen@astrology.com', 'godblessamerica', 'Karen', 'Nonyabis', '68161 Mannheim A1 14', '015789445571'),
('Alfie', 'alfie@burminghambakery.com', 'nevergivepowertothebigman', 'Alfonso', 'Solomons', '24220 Burmingham Kensington Road 11', '01578331212'),
('John', 'John.watson@gmail.com', 'thegameisafoot', 'John', 'Watson', '27615 London Baker Street 221b', '02295001922');


-- Create Item table
CREATE TABLE Item (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    startingPrice NUMERIC DEFAULT 0,
    startTime TIMESTAMP NOT NULL,
    endTime TIMESTAMP NOT NULL,
    imageUrl TEXT NOT NULL,
    user_username VARCHAR(50) REFERENCES "user"(username) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    category_id INTEGER REFERENCES Categorisation(id) 
        ON DELETE SET NULL
);

INSERT INTO Item VALUES
(1, 'A cat with large ears', 'This cat is a great listener. Buy it now!', 20, '2023-05-14 12:11:08', '2023-06-02 11:11:01', 'https://en.wikipedia.org/wiki/Cat#/media/File:Kittyply_edit1.jpg', 'Karen', 1),
(2, 'The Amber Room', 'Look what I found under my bed. It is golden, it is good.', 1200420123, '2023-05-13 06:07:08', '2023-05-30 06:07:08', 'https://de.wikipedia.org/wiki/Bernsteinzimmer#/media/Datei:Andrey_Zeest_-_Amber_Room_2_(autochrome).jpg', 'Alfie', 4),
(3, 'A red bar stool', 'Good Chair, nice and comfy. Does not wobble.', 15, '2020-01-01 19:12:22', '2020-01-02 13:02:22', 'https://cdn.eichholtz.com/media/catalog/product/cache/62a0001ba384dd559aac2c6dd8434b29/1/1/114878_0_1_1.jpg', 'Karen', 3);


-- Create Bid table
CREATE TABLE Bid (
    id SERIAL PRIMARY KEY,
    amount NUMERIC NOT NULL,
    bidTime TIMESTAMP NOT NULL,
    user_username VARCHAR(50) REFERENCES "user"(username) 
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    item_id INTEGER REFERENCES Item(id) 
        ON DELETE CASCADE
);

INSERT INTO Bid (amount, bidTime, user_username, item_id) VALUES
(1200420124, '2023-05-13 09:10:11', 'Karen', 2),
(1300000000, '2023-05-13 12:13:14', 'John', 2),
(24, '1999-01-10 09:11:21', 'Alfie', 1);


-- Create Watchlist table
CREATE TABLE Watchlist (
    user_username VARCHAR(50) REFERENCES "user"(username) 
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    item_id SERIAL REFERENCES Item(id) 
        ON DELETE CASCADE,
    CONSTRAINT unique_watchlist_entry UNIQUE (user_username, item_id)
);

INSERT INTO Watchlist VALUES
('Karen', 2),
('John', 2),
('Alfie', 1);


-- Create Feedback table
CREATE TABLE Feedback (
    feedbackID SERIAL PRIMARY KEY,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 0 AND 10),
    comment TEXT,
    sender VARCHAR(50) REFERENCES "user"(username) 
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    receiver VARCHAR(50) REFERENCES "user"(username) 
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT INTO Feedback VALUES
(1, 1, 'Karen sold me a wobbly chair, I am furious.', 'John', 'Karen'),
(2, 10, 'The small gentleman bought my crooked bar stool. What a good lad.', 'Karen', 'John');


-- Create Payment table
CREATE TABLE Payment (
    amount NUMERIC NOT NULL,
    date TIMESTAMP NOT NULL,
    type PAYMENT_TYPE NOT NULL,
    user_username VARCHAR(50) REFERENCES "user"(username)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    item INTEGER REFERENCES Item(id) 
        ON DELETE CASCADE
);

INSERT INTO Payment VALUES
(42, '2020-01-02 13:02:22', 'Credit Card', 'John', 3);