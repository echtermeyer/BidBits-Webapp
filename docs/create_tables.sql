-- 1. Create User table
CREATE TABLE "User" (
    "Username" VARCHAR(255) PRIMARY KEY,
    "Email" VARCHAR(255) NOT NULL UNIQUE,
    "Password" VARCHAR(255) NOT NULL,
    "Name" VARCHAR(255) NOT NULL,
    "Address" TEXT NOT NULL,
    "Phone" VARCHAR(20) NOT NULL
);

-- 2. Create Category table
CREATE TABLE "Category" (
    "CategoryID" SERIAL PRIMARY KEY,
    "Name" VARCHAR(255) NOT NULL
);

-- 3. Create Item table
CREATE TABLE "Item" (
    "ItemID" SERIAL PRIMARY KEY,
    "Name" VARCHAR(255) NOT NULL,
    "Description" TEXT NOT NULL,
    "StartingPrice" NUMERIC NOT NULL,
    "CurrentBid" NUMERIC,
    "StartTime" TIMESTAMP NOT NULL,
    "EndTime" TIMESTAMP NOT NULL,
    "Seller" VARCHAR(255) REFERENCES "User"("Username") ON DELETE CASCADE,
    "Category" INTEGER REFERENCES "Category"("CategoryID") ON DELETE SET NULL
);

-- 4. Create Bid table
CREATE TABLE "Bid" (
    "BidID" SERIAL PRIMARY KEY,
    "Amount" NUMERIC NOT NULL,
    "BidTime" TIMESTAMP NOT NULL,
    "Bidder" VARCHAR(255) REFERENCES "User"("Username") ON DELETE CASCADE,
    "Item" INTEGER REFERENCES "Item"("ItemID") ON DELETE CASCADE
);

-- 5. Create Image table
CREATE TABLE "Image" (
    "ImageID" SERIAL PRIMARY KEY,
    "URL" TEXT NOT NULL,
    "Item" INTEGER REFERENCES "Item"("ItemID") ON DELETE CASCADE
);

-- 6. Create Watchlist table
CREATE TABLE "Watchlist" (
    "WatchlistID" SERIAL PRIMARY KEY,
    "User" VARCHAR(255) REFERENCES "User"("Username") ON DELETE CASCADE
);

-- 7. Create WatchlistItem (junction table for many-to-many relationship between User and Item)
CREATE TABLE "WatchlistItem" (
    "Watchlist" INTEGER REFERENCES "Watchlist"("WatchlistID") ON DELETE CASCADE,
    "Item" INTEGER REFERENCES "Item"("ItemID") ON DELETE CASCADE,
    PRIMARY KEY ("Watchlist", "Item")
);

-- 8. Create Feedback table
CREATE TABLE "Feedback" (
    "FeedbackID" SERIAL PRIMARY KEY,
    "Rating" INTEGER NOT NULL,
    "Comment" TEXT,
    "Buyer" VARCHAR(255) REFERENCES "User"("Username") ON DELETE CASCADE,
    "Seller" VARCHAR(255) REFERENCES "User"("Username") ON DELETE CASCADE
);

-- 9. Create Payment table
CREATE TABLE "Payment" (
    "PaymentID" SERIAL PRIMARY KEY,
    "PaymentAmount" NUMERIC NOT NULL,
    "PaymentDate" TIMESTAMP NOT NULL,
    "PaymentType" VARCHAR(255) NOT NULL,
    "Buyer" VARCHAR(255) REFERENCES "User"("Username") ON DELETE CASCADE,
    "Item" INTEGER REFERENCES "Item"("ItemID") ON DELETE CASCADE
);