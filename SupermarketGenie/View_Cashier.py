import customtkinter as ctk
import Engine
from PIL import Image
import os
from tkinter import messagebox

class CashierFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        self.cart = [] # {id, name, price, qty_in_cart}
        
        self.grid_columnconfigure(0, weight=7) 
        self.grid_columnconfigure(1, weight=5) 
        self.grid_rowconfigure(0, weight=1)

        # ================= LEFT: LIVE CATALOG =================
        self.shop_zone = ctk.CTkFrame(self, fg_color="#181825", corner_radius=20)
        self.shop_zone.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.search_entry = ctk.CTkEntry(self.shop_zone, placeholder_text="🔍 Scan or Search...", height=50, font=("Consolas", 14))
        self.search_entry.pack(fill="x", padx=25, pady=20)
        self.search_entry.bind("<KeyRelease>", self.update_catalog)

        self.catalog_scroll = ctk.CTkScrollableFrame(self.shop_zone, fg_color="#11111b", corner_radius=15)
        self.catalog_scroll.pack(fill="both", expand=True, padx=25, pady=(0, 25))

        # ================= RIGHT: INTERACTIVE RECEIPT =================
        self.checkout_zone = ctk.CTkFrame(self, fg_color="#1e1e2e", corner_radius=20, border_width=1, border_color="#313244")
        self.checkout_zone.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")

        ctk.CTkLabel(self.checkout_zone, text="LIVE CART", font=("Segoe UI", 16, "bold"), text_color="#fab387").pack(pady=15)

        self.cart_scroll = ctk.CTkScrollableFrame(self.checkout_zone, fg_color="#11111b")
        self.cart_scroll.pack(fill="both", expand=True, padx=20)

        self.summary_f = ctk.CTkFrame(self.checkout_zone, fg_color="transparent")
        self.summary_f.pack(fill="x", padx=20, pady=20)

        self.total_label = ctk.CTkLabel(self.summary_f, text="TOTAL: $0.00", font=("Consolas", 32, "bold"), text_color="#a6e3a1")
        self.total_label.pack(pady=10)

        self.btn_pay = ctk.CTkButton(self.summary_f, text="💳 PROCESS TRANSACTION", height=60, fg_color="#a6e3a1", text_color="#11111b", font=("Segoe UI", 16, "bold"), command=self.show_confirm_window)
        self.btn_pay.pack(fill="x", pady=5)

        self.update_catalog()

    def update_catalog(self, event=None):
        for w in self.catalog_scroll.winfo_children(): w.destroy()
        query = self.search_entry.get().lower()
        # Using the new engine search function
        data = Engine.search_products(query)

        for item in data:
            card = ctk.CTkFrame(self.catalog_scroll, fg_color="#313244", height=70, corner_radius=10)
            card.pack(fill="x", pady=4, padx=5)
            card.pack_propagate(False)

            ctk.CTkLabel(card, text=item['name'], font=("Segoe UI", 13, "bold")).pack(side="left", padx=15)
            ctk.CTkLabel(card, text=f"${item['ps']:.2f}", font=("Consolas", 12), text_color="#94e2d5").pack(side="left", padx=20)
            
            if item['qty'] > 0:
                ctk.CTkButton(card, text="ADD TO CART", width=100, height=35, fg_color="#89b4fa", text_color="#11111b", command=lambda i=item: self.add_to_cart(i)).pack(side="right", padx=10)
            else:
                ctk.CTkLabel(card, text="OUT OF STOCK", text_color="#f38ba8", font=("Segoe UI", 10, "bold")).pack(side="right", padx=10)

    def add_to_cart(self, item):
        for cart_item in self.cart:
            if cart_item['id'] == item['id']:
                if cart_item['qty_in_cart'] < item['qty']:
                    cart_item['qty_in_cart'] += 1
                    self.refresh_cart_display()
                return
        self.cart.append({'id': item['id'], 'name': item['name'], 'price': item['ps'], 'qty_in_cart': 1, 'max': item['qty']})
        self.refresh_cart_display()

    def update_qty(self, p_id, delta):
        for item in self.cart:
            if item['id'] == p_id:
                new_qty = item['qty_in_cart'] + delta
                if 0 < new_qty <= item['max']:
                    item['qty_in_cart'] = new_qty
                elif new_qty <= 0:
                    self.cart.remove(item)
                break
        self.refresh_cart_display()

    def refresh_cart_display(self):
        for w in self.cart_scroll.winfo_children(): w.destroy()
        total = 0
        for item in self.cart:
            row = ctk.CTkFrame(self.cart_scroll, fg_color="#1e1e2e", height=50)
            row.pack(fill="x", pady=3, padx=5)
            
            ctk.CTkLabel(row, text=item['name'], font=("Segoe UI", 12, "bold"), width=120, anchor="w").pack(side="left", padx=10)
            
            # Controls: [-] QTY [+]
            ctk.CTkButton(row, text="-", width=25, height=25, fg_color="#45475a", command=lambda p=item['id']: self.update_qty(p, -1)).pack(side="left", padx=2)
            ctk.CTkLabel(row, text=str(item['qty_in_cart']), font=("Consolas", 12, "bold"), width=30).pack(side="left")
            ctk.CTkButton(row, text="+", width=25, height=25, fg_color="#45475a", command=lambda p=item['id']: self.update_qty(p, 1)).pack(side="left", padx=2)

            sub = item['price'] * item['qty_in_cart']
            total += sub
            ctk.CTkLabel(row, text=f"${sub:.2f}", font=("Consolas", 12), text_color="#a6e3a1", width=70).pack(side="right", padx=10)
            
            # Trash Icon
            ctk.CTkButton(row, text="🗑️", width=30, height=30, fg_color="transparent", text_color="#f38ba8", hover_color="#313244", command=lambda p=item['id']: self.update_qty(p, -999)).pack(side="right")

        self.total_label.configure(text=f"TOTAL: ${total:,.2f}")

    def show_confirm_window(self):
        if not self.cart: return
        
        # Priority Window
        pop = ctk.CTkToplevel(self)
        pop.title("CONFIRM SALE")
        pop.geometry("400x550")
        pop.attributes("-topmost", True)
        pop.grab_set() # Block interaction with main window
        
        ctk.CTkLabel(pop, text="ARE YOU SURE YOU SOLD THIS?", font=("Segoe UI", 16, "bold"), text_color="#f9e2af").pack(pady=20)
        
        # Review Area
        review_f = ctk.CTkScrollableFrame(pop, fg_color="#11111b", height=300)
        review_f.pack(fill="both", expand=True, padx=20)
        
        total = 0
        for item in self.cart:
            sub = item['price'] * item['qty_in_cart']
            total += sub
            lbl = ctk.CTkLabel(review_f, text=f"• {item['qty_in_cart']}x {item['name']} (${sub:.2f})", font=("Consolas", 12), justify="left")
            lbl.pack(anchor="w", pady=2)

        ctk.CTkLabel(pop, text=f"FINAL TOTAL: ${total:.2f}", font=("Segoe UI", 20, "bold"), text_color="#a6e3a1").pack(pady=20)

        btn_f = ctk.CTkFrame(pop, fg_color="transparent")
        btn_f.pack(fill="x", pady=20)
        
        ctk.CTkButton(btn_f, text="YES, CONFIRM", fg_color="#a6e3a1", text_color="#11111b", font=("Segoe UI", 14, "bold"), height=45, command=lambda: self.final_execute(pop)).pack(side="left", padx=20, expand=True, fill="x")
        ctk.CTkButton(btn_f, text="NO, GO BACK", fg_color="#f38ba8", text_color="#11111b", font=("Segoe UI", 14, "bold"), height=45, command=pop.destroy).pack(side="left", padx=20, expand=True, fill="x")

    def final_execute(self, window):
        for item in self.cart:
            for _ in range(item['qty_in_cart']):
                Engine.process_sale(item['id'])
        
        window.destroy()
        self.cart = []
        self.refresh_cart_display()
        self.update_catalog()
        messagebox.showinfo("Success", "Transaction finalized and stock updated!")