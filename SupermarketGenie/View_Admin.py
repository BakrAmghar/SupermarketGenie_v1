import customtkinter as ctk
import Engine

class AdminFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # --- 1. THE COMMAND CENTER (Top Metrics) ---
        self.metrics_container = ctk.CTkFrame(self, fg_color="transparent")
        self.metrics_container.pack(fill="x", padx=20, pady=20)
        self.metrics_container.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.card_items = self.create_metric_card(0, "📁 UNIQUE PRODUCTS", "#cba6f7")
        self.card_stock = self.create_metric_card(1, "📦 TOTAL STOCK", "#89b4fa")
        self.card_invest = self.create_metric_card(2, "💰 TOTAL INVESTMENT", "#f9e2af")
        self.card_profit = self.create_metric_card(3, "📈 POTENTIAL PROFIT", "#a6e3a1")

        # --- 2. AI BUSINESS STRATEGY BOX (New!) ---
        self.ai_box = ctk.CTkFrame(self, fg_color="#1e1e2e", border_width=2, border_color="#f5c2e7", corner_radius=15)
        self.ai_box.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(self.ai_box, text="🤖 GENIE AI STRATEGY TIPS", font=("Segoe UI", 12, "bold"), text_color="#f5c2e7").pack(pady=(10, 0))
        self.ai_tips_label = ctk.CTkLabel(self.ai_box, text="Analyzing inventory...", font=("Consolas", 12), text_color="#cdd6f4", wraplength=800)
        self.ai_tips_label.pack(pady=15, padx=20)

        # --- 3. STOCK HEALTH TABLE (With Margins) ---
        self.table_container = ctk.CTkFrame(self, fg_color="#181825", corner_radius=20, border_width=1, border_color="#45475a")
        self.table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        header_f = ctk.CTkFrame(self.table_container, fg_color="#11111b", height=50, corner_radius=15)
        header_f.pack(fill="x", padx=15, pady=15)
        
        # Added Margin to the columns
        cols = [("ID", 0.05), ("PRODUCT NAME", 0.35), ("COST", 0.12), ("SALE", 0.12), ("MARGIN %", 0.12), ("STOCK", 0.12)]
        for text, weight in cols:
            lbl = ctk.CTkLabel(header_f, text=text, font=("Segoe UI", 11, "bold"), text_color="#585b70")
            # Calculate position based on cumulative weights
            pos = sum(c[1] for c in cols[:cols.index((text, weight))]) + 0.02
            lbl.place(relx=pos, rely=0.5, anchor="w")

        self.scroll = ctk.CTkScrollableFrame(self.table_container, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.refresh_stats()

    def create_metric_card(self, col, title, color):
        card = ctk.CTkFrame(self.metrics_container, fg_color="#181825", height=110, corner_radius=15, border_width=1, border_color="#313244")
        card.grid(row=0, column=col, padx=10, sticky="ew")
        card.grid_propagate(False)
        ctk.CTkLabel(card, text=title, font=("Segoe UI", 10, "bold"), text_color=color).pack(pady=(15, 2))
        val_label = ctk.CTkLabel(card, text="0", font=("Consolas", 24, "bold"), text_color="#cdd6f4")
        val_label.pack()
        return val_label

    def generate_ai_tips(self, data, stats):
        """Simulates AI logic by analyzing the real data trends."""
        if not data:
            return "Genie is hungry for data. Add products to see business tips!"
        
        tips = []
        low_stock = [i['name'] for i in data if i['qty'] < 20]
        low_margin = [i['name'] for i in data if i['ps'] > 0 and ((i['ps']-i['pb'])/i['ps'])*100 < 15]
        
        if low_stock:
            tips.append(f"⚠️ RESTOCK ALERT: {', '.join(low_stock[:2])} are running thin. Reorder to avoid lost sales.")
        if low_margin:
            tips.append(f"💸 MARGIN WARNING: {', '.join(low_margin[:2])} have low profits. Consider a 5-10% price hike.")
        if stats['potential_profit'] > 1000:
            tips.append("🚀 GROWTH: Your potential profit looks strong. Maybe it's time to add a new category?")
        else:
            tips.append("💡 TIP: Focus on high-volume items to increase your daily cash flow.")

        return " | ".join(tips)

    def refresh_stats(self):
        stats = Engine.get_total_stats()
        data = Engine.load_data()

        self.card_items.configure(text=str(stats["items_count"]))
        self.card_stock.configure(text=str(stats["total_stock"]))
        self.card_invest.configure(text=f"${stats['investment']:,.2f}")
        self.card_profit.configure(text=f"${stats['potential_profit']:,.2f}")

        # Update AI Tips
        self.ai_tips_label.configure(text=self.generate_ai_tips(data, stats))

        for w in self.scroll.winfo_children(): w.destroy()

        for item in data:
            row = ctk.CTkFrame(self.scroll, fg_color="#1e1e2e", height=45, corner_radius=8)
            row.pack(fill="x", pady=4)
            
            # MATH FOR MARGIN
            margin_val = 0
            if item['ps'] > 0:
                margin_val = ((item['ps'] - item['pb']) / item['ps']) * 100
            
            # Colors for margin health
            m_color = "#a6e3a1" if margin_val > 30 else "#f9e2af" if margin_val > 10 else "#f38ba8"
            s_color = "#f38ba8" if item['qty'] < 20 else "#cdd6f4"

            # Horizontal Layout
            ctk.CTkLabel(row, text=item['id'], font=("Consolas", 11)).place(relx=0.02, rely=0.5, anchor="w")
            ctk.CTkLabel(row, text=item['name'], font=("Segoe UI", 13, "bold")).place(relx=0.08, rely=0.5, anchor="w")
            ctk.CTkLabel(row, text=f"${item['pb']:.2f}", text_color="#fab387").place(relx=0.42, rely=0.5, anchor="w")
            ctk.CTkLabel(row, text=f"${item['ps']:.2f}", text_color="#89dceb").place(relx=0.54, rely=0.5, anchor="w")
            ctk.CTkLabel(row, text=f"{margin_val:.1f}%", text_color=m_color, font=("Consolas", 12, "bold")).place(relx=0.67, rely=0.5, anchor="w")
            ctk.CTkLabel(row, text=str(item['qty']), font=("Consolas", 13, "bold"), text_color=s_color).place(relx=0.81, rely=0.5, anchor="w")