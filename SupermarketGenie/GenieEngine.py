# GenieEngine.py
products = [
    {"id": "101", "name": "Energy Drink", "pb": 10.0, "ps": 15.0, "qty": 20},
    {"id": "102", "name": "Organic Flour", "pb": 5.0, "ps": 8.5, "qty": 50}
]

def check_credentials(password):
    # Simple logic: 1234 is the master key for this prototype
    return password == "1234"

def get_stats():
    inv = sum(i['pb'] * i['qty'] for i in products)
    rev = sum(i['ps'] * i['qty'] for i in products)
    return {"inv": inv, "profit": rev - inv, "count": len(products)}