import customtkinter as ctk
import Engine
from tkinter import filedialog, messagebox
from PIL import Image
import os

class SupplyFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.selected_image_path = ""
        self.sort_mode = "id" 

        # --- 1. INTELLIGENCE DASHBOARD (Stretches to Full Width) ---
        self.dashboard = ctk.CTkFrame(self, fg_color="#11111b", height=90, corner_radius=15, border_width=2, border_color="#313244")
        self.dashboard.pack(fill="x", padx=20, pady=(15, 0))
        self.dashboard.grid_columnconfigure((0, 1), weight=1)

        # Zone A: Big Rollers
        self.roller_f = ctk.CTkFrame(self.dashboard, fg_color="transparent")
        self.roller_f.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
        ctk.CTkLabel(self.roller_f, text="🚀 BIG ROLLERS (>50%)", font=("Segoe UI", 13, "bold"), text_color="#a6e3a1").pack()
        self.roller_data = ctk.CTkLabel(self.roller_f, text="None", font=("Consolas", 12), text_color="#94e2d5")
        self.roller_data.pack()

        # Zone B: Close to End
        self.stock_f = ctk.CTkFrame(self.dashboard, fg_color="transparent")
        self.stock_f.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)
        ctk.CTkLabel(self.stock_f, text="⚠️ CLOSE TO END (<40)", font=("Segoe UI", 13, "bold"), text_color="#f38ba8").pack()
        self.stock_data = ctk.CTkLabel(self.stock_f, text="Healthy", font=("Consolas", 12), text_color="#f9e2af")
        self.stock_data.pack()

        # --- 2. MAIN WORKSPACE (The "Horizontally Longer" Engine) ---
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        
        # Grid Weights for wide screen
        self.container.grid_columnconfigure(0, weight=4) 
        self.container.grid_columnconfigure(1, weight=8) 
        self.container.grid_rowconfigure(0, weight=1)

        # ================= LEFT: THE WIDE EDITOR =================
        self.editor = ctk.CTkFrame(self.container, fg_color="#181825", corner_radius=20, border_width=1, border_color="#45475a")
        self.editor.grid(row=0, column=0, padx=15, pady=20, sticky="nsew")

        ctk.CTkLabel(self.editor, text="PRODUCT WIZARD", font=("Segoe UI", 16, "bold"), text_color="#cba6f7").pack(pady=15)

        # Row 1: Image & ID/Name
        self.row1 = ctk.CTkFrame(self.editor, fg_color="transparent")
        self.row1.pack(fill="x", padx=25)
        
        self.preview_frame = ctk.CTkFrame(self.row1, width=100, height=100, fg_color="#11111b", corner_radius=12)
        self.preview_frame.pack(side="left", padx=(0, 15))
        self.preview_frame.pack_propagate(False)
        self.preview_label = ctk.CTkLabel(self.preview_frame, text="NO IMAGE", font=("Arial", 9))
        self.preview_label.place(relx=0.5, rely=0.5, anchor="center")

        self.c1_inputs = ctk.CTkFrame(self.row1, fg_color="transparent")
        self.c1_inputs.pack(side="left", fill="x", expand=True)
        self.entry_id = self.create_input(self.c1_inputs, "Product ID")
        self.entry_name = self.create_input(self.c1_inputs, "Product Name")

        # Row 2: Financials & Stock
        self.row2 = ctk.CTkFrame(self.editor, fg_color="transparent")
        self.row2.pack(fill="x", padx=25, pady=15)
        
        self.entry_pb = ctk.CTkEntry(self.row2, placeholder_text="Cost (PB)", height=45)
        self.entry_pb.pack(side="left", padx=5, expand=True, fill="x")
        self.entry_pb.bind("<KeyRelease>", self.update_margin)
        
        self.entry_ps = ctk.CTkEntry(self.row2, placeholder_text="Sale (PS)", height=45)
        self.entry_ps.pack(side="left", padx=5, expand=True, fill="x")
        self.entry_ps.bind("<KeyRelease>", self.update_margin)
        
        self.entry_qty = ctk.CTkEntry(self.row2, placeholder_text="Qty", height=45)
        self.entry_qty.pack(side="left", padx=5, expand=True, fill="x")

        self.margin_label = ctk.CTkLabel(self.editor, text="Margin: 0%", font=("Segoe UI", 12, "italic"), text_color="#585b70")
        self.margin_label.pack(anchor="w", padx=30)

        # Action Buttons Grid (Stretched)
        self.btn_f = ctk.CTkFrame(self.editor, fg_color="transparent")
        self.btn_f.pack(fill="x", padx=25, pady=20)
        self.btn_f.grid_columnconfigure((0,1), weight=1)

        ctk.CTkButton(self.btn_f, text="📷 PHOTO", height=40, fg_color="#45475a", command=self.upload_photo).grid(row=0, column=0, padx=4, pady=4, sticky="ew")
        ctk.CTkButton(self.btn_f, text="🧹 RESET", height=40, fg_color="transparent", border_width=1, border_color="#f38ba8", text_color="#f38ba8", command=self.clear_form).grid(row=0, column=1, padx=4, pady=4, sticky="ew")
        
        ctk.CTkButton(self.btn_f, text="✨ SAVE PRODUCT", height=55, fg_color="#a6e3a1", text_color="#11111b", font=("Segoe UI", 15, "bold"), command=self.validate_and_save).grid(row=1, column=0, padx=4, pady=4, sticky="ew")
        ctk.CTkButton(self.btn_f, text="📥 BULK IMPORT", height=55, fg_color="#f5c2e7", text_color="#11111b", font=("Segoe UI", 15, "bold"), command=self.open_bulk_window).grid(row=1, column=1, padx=4, pady=4, sticky="ew")


        # ================= RIGHT: THE ULTRA-WIDE LIVE VIEW =================
        self.viewer = ctk.CTkFrame(self.container, fg_color="#181825", corner_radius=20)
        self.viewer.grid(row=0, column=1, padx=15, pady=20, sticky="nsew")

        self.search_bar = ctk.CTkEntry(self.viewer, placeholder_text="🔍 Filter database by name or ID...", height=45, corner_radius=12)
        self.search_bar.pack(fill="x", padx=30, pady=20)
        self.search_bar.bind("<KeyRelease>", self.update_live_list)

        # Sorting Controls
        self.sort_f = ctk.CTkFrame(self.viewer, fg_color="transparent")
        self.sort_f.pack(fill="x", padx=30)
        ctk.CTkButton(self.sort_f, text="Sort by Name", width=120, height=32, fg_color="#fab387", text_color="#11111b", command=lambda: self.set_sort("name")).pack(side="left", padx=5)
        ctk.CTkButton(self.sort_f, text="Sort by Profit %", width=140, height=32, fg_color="#89dceb", text_color="#11111b", command=lambda: self.set_sort("margin")).pack(side="left", padx=5)
        ctk.CTkButton(self.sort_f, text="Sort by Stock", width=120, height=32, fg_color="#f9e2af", text_color="#11111b", command=lambda: self.set_sort("qty")).pack(side="left", padx=5)

        self.scroll = ctk.CTkScrollableFrame(self.viewer, fg_color="#11111b", corner_radius=15)
        self.scroll.pack(fill="both", expand=True, padx=30, pady=20)

        self.update_live_list()

    def create_input(self, parent, p):
        e = ctk.CTkEntry(parent, placeholder_text=p, height=45, corner_radius=12)
        e.pack(pady=6, fill="x")
        return e

    def render_image(self, path):
        if path and os.path.exists(path):
            try:
                img = Image.open(path)
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(95, 95))
                self.preview_label.configure(image=ctk_img, text="")
                self.preview_label.image = ctk_img
            except:
                self.preview_label.configure(image=None, text="ERR IMG")
        else:
            self.preview_label.configure(image=None, text="NO IMAGE")

    def set_sort(self, mode):
        self.sort_mode = mode
        self.update_live_list()

    def update_margin(self, event=None):
        try:
            pb, ps = float(self.entry_pb.get()), float(self.entry_ps.get())
            if ps > 0:
                m = ((ps-pb)/ps)*100
                self.margin_label.configure(text=f"Margin: {m:.1f}%", text_color="#a6e3a1" if m > 0 else "#f38ba8")
        except: self.margin_label.configure(text="Margin: --%", text_color="#585b70")

    def update_live_list(self, event=None):
        for w in self.scroll.winfo_children(): w.destroy()
        data = Engine.load_data()

        # Update Dashboard
        rollers = [i['name'] for i in data if i['ps'] > 0 and ((i['ps']-i['pb'])/i['ps'])*100 > 50]
        self.roller_data.configure(text=", ".join(rollers[:3]) if rollers else "None")
        low = [f"{i['name']}({i['qty']})" for i in data if i['qty'] < 40]
        self.stock_data.configure(text=", ".join(low[:3]) if low else "Healthy")

        query = self.search_bar.get().lower()
        filtered = [i for i in data if query in i['id'].lower() or query in i['name'].lower()]

        if self.sort_mode == "margin": filtered.sort(key=lambda x: ((x['ps']-x['pb'])/x['ps'] if x['ps']>0 else 0), reverse=True)
        elif self.sort_mode == "qty": filtered.sort(key=lambda x: x['qty'], reverse=True)
        elif self.sort_mode == "name": filtered.sort(key=lambda x: x['name'].lower())

        for item in filtered:
            f = ctk.CTkFrame(self.scroll, fg_color="#311b1b" if item['qty'] < 40 else "#1e1e2e", height=60)
            f.pack(fill="x", pady=5, padx=10)
            ctk.CTkLabel(f, text=item['name'], font=("Segoe UI", 14, "bold")).pack(side="left", padx=25)
            ctk.CTkButton(f, text="🗑️", width=40, height=32, fg_color="#f38ba8", text_color="#11111b", command=lambda i=item: self.delete_item(i['id'])).pack(side="right", padx=15)
            ctk.CTkButton(f, text="INFO", width=80, height=32, fg_color="#89dceb", text_color="#11111b", command=lambda i=item: self.show_details(i)).pack(side="right", padx=5)
            ctk.CTkButton(f, text="MODIFY", width=80, height=32, fg_color="#fab387", text_color="#11111b", command=lambda i=item: self.fill_form_from_list(i)).pack(side="right", padx=5)

    def fill_form_from_list(self, item):
        self.clear_form()
        self.entry_id.insert(0, item['id']); self.entry_name.insert(0, item['name'])
        self.entry_pb.insert(0, str(item['pb'])); self.entry_ps.insert(0, str(item['ps']))
        self.entry_qty.insert(0, str(item['qty']))
        self.selected_image_path = item.get('image', "")
        self.render_image(self.selected_image_path)
        self.update_margin()

    def show_details(self, item):
        win = ctk.CTkToplevel(self)
        win.title("Product Intel")
        win.geometry("350x450")
        win.attributes("-topmost", True) 
        win.configure(fg_color="#181825")

        header = ctk.CTkFrame(win, fg_color="#89b4fa", height=60, corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(header, text=item['name'].upper(), font=("Segoe UI", 18, "bold"), text_color="#11111b").pack(pady=15)

        body = ctk.CTkFrame(win, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=25, pady=25)

        details = [
            ("🆔 PRODUCT ID", item['id']),
            ("💰 UNIT COST", f"${item['pb']}"),
            ("🏷️ SALE PRICE", f"${item['ps']}"),
            ("📦 STOCK LEVEL", f"{item['qty']} units"),
            ("📅 ADDED ON", item.get('added_at', 'N/A'))
        ]

        for label, val in details:
            row = ctk.CTkFrame(body, fg_color="transparent")
            row.pack(fill="x", pady=8)
            ctk.CTkLabel(row, text=label, font=("Segoe UI", 11, "bold"), text_color="#585b70").pack(side="left")
            ctk.CTkLabel(row, text=val, font=("Consolas", 12), text_color="#cdd6f4").pack(side="right")

    def open_bulk_window(self):
        win = ctk.CTkToplevel(self)
        win.title("Bulk Data Engine")
        win.geometry("500x600")
        win.attributes("-topmost", True) 
        win.configure(fg_color="#181825")
        
        guide_f = ctk.CTkFrame(win, fg_color="#11111b", border_width=1, border_color="#89dceb")
        guide_f.pack(fill="x", padx=25, pady=20)
        
        guide_text = "📖 IMPORT GUIDE:\nFormat: ID, Name, Cost, Sale, Qty\nUse commas to separate values.\nExample: 101, Coffee, 2.50, 5.00, 100"
        ctk.CTkLabel(guide_f, text=guide_text, justify="left", font=("Segoe UI", 12), text_color="#89dceb").pack(padx=20, pady=20)

        txt = ctk.CTkTextbox(win, width=450, height=300, fg_color="#11111b", text_color="#a6e3a1", font=("Consolas", 13))
        txt.pack(pady=15)
        
        def process():
            lines = txt.get("1.0", "end-1c").split("\n")
            for line in lines:
                p = [x.strip() for x in line.split(",")]
                if len(p) == 5: Engine.add_or_update_product(p[0], p[1], p[2], p[3], p[4])
            self.update_live_list(); win.destroy()

        ctk.CTkButton(win, text="🚀 EXECUTE IMPORT", fg_color="#a6e3a1", text_color="#11111b", font=("Segoe UI", 16, "bold"), height=50, command=process).pack(pady=15)

    def delete_item(self, p_id):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this product?"):
            if Engine.remove_product(p_id): self.update_live_list()

    def upload_photo(self):
        file = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        if file:
            self.selected_image_path = file
            self.render_image(file)

    def validate_and_save(self):
        try:
            Engine.add_or_update_product(self.entry_id.get(), self.entry_name.get(), self.entry_pb.get(), self.entry_ps.get(), self.entry_qty.get(), self.selected_image_path)
            self.update_live_list(); self.clear_form()
        except: messagebox.showerror("Error", "Check data types! Prices must be numbers.")

    def clear_form(self):
        for e in [self.entry_id, self.entry_name, self.entry_pb, self.entry_ps, self.entry_qty]: 
            if hasattr(e, 'delete'): e.delete(0, 'end')
        self.selected_image_path = ""
        self.render_image("")