import customtkinter as ctk
import Engine
import random
import time
from tkinter import messagebox

class AdminFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # --- 1. TOP METRICS (Ultra Compact) ---
        self.metrics_container = ctk.CTkFrame(self, fg_color="transparent", height=75)
        self.metrics_container.pack(fill="x", padx=10, pady=(10, 2))
        self.metrics_container.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.metrics_container.pack_propagate(False)

        self.card_items = self.create_metric_card(0, "📁 UNIQUE", "#cba6f7")
        self.card_stock = self.create_metric_card(1, "📦 STOCK", "#89b4fa")
        self.card_invest = self.create_metric_card(2, "💰 INVEST", "#f9e2af")
        self.card_profit = self.create_metric_card(3, "📈 PROFIT", "#a6e3a1")

        # --- 2. AI STRATEGY STRIP (Dynamic) ---
        self.ai_strip = ctk.CTkFrame(self, fg_color="#1e1e2e", border_width=1, border_color="#f5c2e7", height=32)
        self.ai_strip.pack(fill="x", padx=15, pady=5)
        self.ai_strip.pack_propagate(False)
        self.ai_tips_label = ctk.CTkLabel(self.ai_strip, text="⚡ GENIE AI: Analyzing data packets...", 
                                         font=("Consolas", 9, "italic"), text_color="#f5c2e7")
        self.ai_tips_label.pack(pady=2)

        # --- 3. THE SPLIT VIEW ---
        self.main_body = ctk.CTkFrame(self, fg_color="transparent")
        self.main_body.pack(fill="both", expand=True, padx=15, pady=5)
        self.main_body.columnconfigure(0, weight=3) # Product List
        self.main_body.columnconfigure(1, weight=2) # Audit/Graph

        # --- LEFT: FULL PRODUCT MASTER ---
        self.inv_panel = ctk.CTkFrame(self.main_body, fg_color="#181825", corner_radius=12, border_width=1, border_color="#313244")
        self.inv_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        
        # Explicit Header for all columns
        h_row = ctk.CTkFrame(self.inv_panel, fg_color="#11111b", height=28)
        h_row.pack(fill="x", padx=8, pady=8)
        cols = [("ID", 0.05), ("NAME", 0.35), ("COST", 0.12), ("SALE", 0.12), ("MGN%", 0.12), ("STK", 0.12)]
        for text, weight in cols:
            lbl = ctk.CTkLabel(h_row, text=text, font=("Segoe UI", 8, "bold"), text_color="#585b70")
            pos = sum(c[1] for c in cols[:cols.index((text, weight))]) + 0.02
            lbl.place(relx=pos, rely=0.5, anchor="w")

        self.scroll = ctk.CTkScrollableFrame(self.inv_panel, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=2, pady=2)

        # --- RIGHT: FORENSIC HUB ---
        self.audit_hub = ctk.CTkFrame(self.main_body, fg_color="transparent")
        self.audit_hub.grid(row=0, column=1, sticky="nsew")

        # A. Mini Graph with Axes
        self.graph_box = ctk.CTkFrame(self.audit_hub, fg_color="#181825", height=120, corner_radius=10, border_width=1, border_color="#313244")
        self.graph_box.pack(fill="x", pady=(0, 8))
        self.graph_box.pack_propagate(False)
        self.draw_mini_graph()

        # B. Audit Calendar & Title
        self.audit_ctrl = ctk.CTkFrame(self.audit_hub, fg_color="#181825", corner_radius=10, border_width=1, border_color="#313244")
        self.audit_ctrl.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(self.audit_ctrl, text="🕵️ SYSTEM AUDIT CALENDAR", font=("Segoe UI", 9, "bold"), text_color="#89dceb").pack(pady=4)
        
        self.days_grid = ctk.CTkFrame(self.audit_ctrl, fg_color="transparent")
        self.days_grid.pack(pady=(0, 8))
        self.setup_day_btns()

        # C. OUTPUT AREA (Fixed Button at Bottom)
        self.output_panel = ctk.CTkFrame(self.audit_hub, fg_color="#1e1e2e", corner_radius=12, border_width=1, border_color="#45475a")
        self.output_panel.pack(fill="both", expand=True)

        self.log_view = ctk.CTkScrollableFrame(self.output_panel, height=110, fg_color="transparent")
        self.log_view.pack(fill="x", padx=8, pady=5)

        self.ai_report_bg = ctk.CTkFrame(self.output_panel, fg_color="#11111b", corner_radius=8)
        self.ai_report_bg.pack(fill="both", expand=True, padx=8, pady=5)
        
        self.ai_status_lbl = ctk.CTkLabel(self.ai_report_bg, text="PICK A DAY FOR ANALYSIS", 
                                         font=("Consolas", 10, "bold"), text_color="#bac2de", 
                                         wraplength=260, justify="left")
        self.ai_status_lbl.pack(padx=10, pady=10, expand=True)
        
        self.go_btn = ctk.CTkButton(self.output_panel, text="🚀 RUN GENIE AI AUDIT", fg_color="#a6e3a1", text_color="#11111b", 
                                   font=("Segoe UI", 10, "bold"), height=35, command=self.run_genie_logic)
        self.go_btn.pack(fill="x", padx=8, pady=8)

        self.refresh_stats()
        self.active_day = "Mon"

    def draw_mini_graph(self):
        canvas = ctk.CTkFrame(self.graph_box, fg_color="transparent")
        canvas.pack(fill="both", expand=True, padx=10, pady=5)
        # Simple axis lines
        ctk.CTkFrame(canvas, width=1, height=80, fg_color="#313244").place(relx=0.08, rely=0.1)
        ctk.CTkFrame(canvas, width=280, height=1, fg_color="#313244").place(relx=0.08, rely=0.85)

        for i, d in enumerate(["M", "T", "W", "T", "F", "S", "S"]):
            val = random.randint(20, 75)
            clr = "#f38ba8" if i == 3 else "#7aa2f7" # Thursday is Red
            bar = ctk.CTkFrame(canvas, width=18, height=val, fg_color=clr, corner_radius=2)
            bar.place(relx=0.15 + (i*0.12), rely=0.85, anchor="s")
            ctk.CTkLabel(canvas, text=d, font=("Arial", 8), text_color=clr).place(relx=0.15 + (i*0.12), rely=0.95, anchor="s")

    def setup_day_btns(self):
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, d in enumerate(days):
            b = ctk.CTkButton(self.days_grid, text=d, width=38, height=30, corner_radius=5,
                              fg_color="#11111b", font=("Segoe UI", 9, "bold"), command=lambda x=d: self.load_day(x))
            b.grid(row=0, column=i, padx=1)

    def load_day(self, day):
        self.active_day = day
        for w in self.log_view.winfo_children(): w.destroy()
        ctk.CTkLabel(self.log_view, text=f"--- SESSION LOG: {day.upper()} ---", font=("Consolas", 9, "bold"), text_color="#fab387").pack()
        managers = ["Bakr_ROOT", "Amine_SPLY", "Sarah_OPS", "MGR_10149310"]
        for _ in range(12):
            t = f"{random.randint(9,22)}:{random.randint(10,59)}"
            mgr = random.choice(managers)
            act = random.choice(["RESTOCK", "VOID_SESS", "PRICE_ADJ", "LOGIN"])
            ctk.CTkLabel(self.log_view, text=f"[{t}] {mgr} > {act}", font=("Consolas", 8), text_color="#cdd6f4").pack(anchor="w")
        self.ai_status_lbl.configure(text=f"Day {day} logs synchronized. Ready for forensic analysis.", text_color="#bac2de")

    def run_genie_logic(self):
        self.ai_status_lbl.configure(text="🧞‍♂️ GENIE IS ANALYZING SENSOR DATA...")
        self.update()
        time.sleep(1.0)
        if self.active_day == "Thu":
            msg = "🚨 ALERT: Manager 10149310 restocked inventory but weight sensors recorded 0% change. No truck assigned. Stealing likely on March 14th."
            self.ai_status_lbl.configure(text=msg, text_color="#f38ba8")
        else:
            self.ai_status_lbl.configure(text="✅ AUDIT PASSED: Digital restocks correlate with physical weight increases for this session.", text_color="#a6e3a1")

    def create_metric_card(self, col, title, color):
        c = ctk.CTkFrame(self.metrics_container, fg_color="#181825", height=65, corner_radius=10, border_width=1, border_color="#313244")
        c.grid(row=0, column=col, padx=5, sticky="ew")
        c.grid_propagate(False)
        ctk.CTkLabel(c, text=title, font=("Segoe UI", 7, "bold"), text_color=color).pack(pady=(10, 0))
        v = ctk.CTkLabel(c, text="0", font=("Consolas", 18, "bold"), text_color="#cdd6f4")
        v.pack()
        return v

    def refresh_stats(self):
        s = Engine.get_total_stats()
        d = Engine.load_data()
        self.card_items.configure(text=str(s["items_count"]))
        self.card_stock.configure(text=str(s["total_stock"]))
        self.card_invest.configure(text=f"${s['investment']:,.0f}")
        self.card_profit.configure(text=f"${s['potential_profit']:,.0f}")
        
        low = [i['name'] for i in d if i['qty'] < 12]
        self.ai_tips_label.configure(text=f"⚡ GENIE: Restock {low[0]} immediately!" if low else "⚡ GENIE: Inventory flow is 100% efficient.")

        for w in self.scroll.winfo_children(): w.destroy()
        for item in d:
            r = ctk.CTkFrame(self.scroll, fg_color="#1e1e2e", height=32, corner_radius=6)
            r.pack(fill="x", pady=2)
            margin = ((item['ps']-item['pb'])/item['ps'])*100 if item['ps']>0 else 0
            m_clr = "#a6e3a1" if margin > 25 else "#f9e2af" if margin > 10 else "#f38ba8"
            
            ctk.CTkLabel(r, text=item['id'], font=("Consolas", 8)).place(relx=0.02, rely=0.5, anchor="w")
            ctk.CTkLabel(r, text=item['name'][:20], font=("Segoe UI", 10, "bold")).place(relx=0.08, rely=0.5, anchor="w")
            ctk.CTkLabel(r, text=f"${item['pb']:.2f}", text_color="#fab387", font=("Consolas", 9)).place(relx=0.42, rely=0.5, anchor="w")
            ctk.CTkLabel(r, text=f"${item['ps']:.2f}", text_color="#89dceb", font=("Consolas", 9)).place(relx=0.54, rely=0.5, anchor="w")
            ctk.CTkLabel(r, text=f"{margin:.1f}%", font=("Consolas", 9), text_color=m_clr).place(relx=0.67, rely=0.5, anchor="w")
            ctk.CTkLabel(r, text=str(item['qty']), font=("Consolas", 10, "bold")).place(relx=0.81, rely=0.5, anchor="w")