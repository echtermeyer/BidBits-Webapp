import dash_bootstrap_components as dbc
from dash import html


def retrieve_all_items():
    return  [
        {
            "item_id": "10",
            "title": "Item 1",
            "description": "Some detailed description",
            "highest_bid": "500",
            "time_left": "2",
            "image_path": "item1.jpg",
            "is_watchlist": False
        },
        {
            "item_id": "3",
            "title": "Item 2",
            "description": "Some detailed description",
            "highest_bid": "500",
            "time_left": "2",
            "image_path": "item2.jpg",
            "is_watchlist": True
        },
        {
            "item_id": "1",
            "title": "Item 3",
            "description": "Some detailed description",
            "highest_bid": "500",
            "time_left": "2",
            "image_path": "item1.jpg",
            "is_watchlist": False
        },
        {
            "item_id": "2",
            "title": "Item 4",
            "description": "Some detailed description",
            "highest_bid": "500",
            "time_left": "2",
            "image_path": "item1.jpg",
            "is_watchlist": True
        }
    ]

def retrieve_watchlist():
    return  [
        {
            "item_id": "2",
            "title": "Item 2",
            "description": "Some detailed description",
            "highest_bid": "500",
            "time_left": "2",
            "image_path": "item2.jpg",
            "is_watchlist": True
        },
        {
            "item_id": "4",
            "title": "Item 4",
            "description": "Some detailed description",
            "highest_bid": "500",
            "time_left": "2",
            "image_path": "item1.jpg",
            "is_watchlist": True
        }
    ]


def add_bid_to_wishlist():
    pass


def remove_bid_from_whishlist():
    pass
