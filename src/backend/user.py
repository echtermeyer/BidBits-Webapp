# Used for login
def login_user():
    pass


# Used for registration
def register_user():
    if __check_user_exists():
        return "Already exists"
    pass

def __check_user_exists():
    pass


# Used for displaying "update personal data" on users page
def retrieve_user_information():
    return {
        "username": "Maxus121", 
        "email": "max@mustermann.de",
        "firstname": "Max",
        "lastname": "Mustermann",
        "address": "Meerlachstr. 5, 68166 Mannheim",
        "phone": "015168188995"
    }


# Used for displaying "payment history" on users page
def retrieve_payment_information():
    return [
        {
            "item_id": "3",
            "title": "Goofy cat",
            "amount": "$500",
            "date": "05/12/2023",
            "method": "PayPal"
        },
        {
            "item_id": "8",
            "title": "Goofy cat, but different",
            "amount": "$1200",
            "date": "05/12/2023",
            "method": "Bitcoin"
        }, {
            "item_id": "12",
            "title": "Goofy cat",
            "amount": "$500",
            "date": "05/12/2023",
            "method": "PayPal"
        },
        {
            "item_id": "312",
            "title": "Goofy cat, but different",
            "amount": "$1200",
            "date": "05/12/2023",
            "method": "Bitcoin"
        }
    ]


# Used for displaying "won auctions" on users page
def retrieve_won_auctions():
    return  [
        {
            "item_id": "3",
            "seller": "tomym",
            "buyer": "maxmuster",
            "title": "Goofy cat",
            "description": "a very ugly cat",
            "price": "$500",
            "date": "05/12/2023",
            "image_path": "item1.jpg"
        },
        {
            "item_id": "44",
            "title": "Goofy cat 2",
            "seller": "tomym",
            "buyer": "maxmuster",
            "description": "a very ugly cat",
            "price": "$500",
            "date": "05/12/2023",
            "image_path": "item2.jpg"
        },
        {
            "item_id": "35",
            "seller": "tomym",
            "buyer": "maxmuster",
            "title": "Goofy cat 3",
            "description": "a very ugly cat",
            "price": "$500",
            "date": "05/12/2023",
            "image_path": "item1.jpg"
        },
    ]


# Used for displaying "feedback" users page
def retrieve_feedback():
    return  [
        {
            "sender": "tomyh",
            "rating": "4",
            "message": "Awesome seller. Everything like described",
            "date": "05/05/2023"
        },
        {
            "sender": "bboom",
            "rating": "2",
            "message": "Delivery was slow",
            "date": "05/12/2023"
        },
        {
            "sender": "tomyh",
            "rating": "4",
            "message": "Awesome seller. Everything like described",
            "date": "05/05/2023"
        },
        {
            "sender": "bboom",
            "rating": "2",
            "message": "Delivery was slow",
            "date": "05/12/2023"
        }
    ]