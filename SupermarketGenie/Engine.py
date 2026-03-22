import customtkinter as ctk
from PIL import Image 
import os
from datetime import datetime

# --- GLOBAL IN-MEMORY DATABASE ---
inventory = []

def load_data():
    """Returns the live inventory list from RAM."""
    return inventory

def save_data(new_list):
    """Updates the global inventory with a new list."""
    global inventory
    inventory = new_list

def add_or_update_product(p_id, name, pb, ps, qty, image_path=""):
    global inventory
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    for item in inventory:
        if item["id"] == p_id:
            item.update({
                "name": name,
                "pb": float(pb),
                "ps": float(ps),
                "qty": int(qty),
                "image": image_path
            })
            return

    new_product = {
        "id": p_id,
        "name": name,
        "pb": float(pb),
        "ps": float(ps),
        "qty": int(qty),
        "image": image_path,
        "added_at": now
    }
    inventory.append(new_product)

def get_product_by_id(p_id):
    for item in inventory:
        if item["id"] == p_id:
            return item
    return None

def remove_product(p_id):
    global inventory
    initial_count = len(inventory)
    inventory = [item for item in inventory if item["id"] != p_id]
    return len(inventory) < initial_count

def process_sale(p_id):
    """Subtacts 1 from quantity if stock > 0."""
    for item in inventory:
        if item["id"] == p_id:
            if int(item["qty"]) > 0:
                item["qty"] -= 1
                return True
    return False

def get_total_stats():
    """Calculates business health metrics for Admin."""
    total_qty = sum(item["qty"] for item in inventory)
    total_investment = sum(item["pb"] * item["qty"] for item in inventory)
    total_revenue = sum(item["ps"] * item["qty"] for item in inventory)
    total_profit = total_revenue - total_investment
    
    return {
        "items_count": len(inventory),
        "total_stock": total_qty,
        "investment": round(total_investment, 2),
        "potential_profit": round(total_profit, 2)
    }

def bulk_update_stock(update_list):
    success_count = 0
    for p_id, additional_qty in update_list:
        item = get_product_by_id(p_id)
        if item:
            item["qty"] += int(additional_qty)
            success_count += 1
    return success_count

# ================= NEW POWER FUNCTIONS (Added for Cashier & Admin) =================

def search_products(query):
    """
    NEW: Returns a list of products matching ID or Name.
    Used by the Cashier's Live Search.
    """
    query = query.lower()
    return [i for i in inventory if query in i['id'].lower() or query in i['name'].lower()]

def get_low_stock_items(threshold=20):
    """
    NEW: Returns a list of items that need restocking.
    Used by the Admin AI Tips.
    """
    return [i for i in inventory if i['qty'] < threshold]

def get_best_sellers():
    """
    NEW: Placeholder for sales tracking.
    In the future, we could track which items are sold most often!
    """
    # For now, let's just return items with high margins
    return [i for i in inventory if i['ps'] > (i['pb'] * 1.5)]