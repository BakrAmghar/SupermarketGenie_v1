import customtkinter as ctk
from PIL import Image
import os
import time
from tkinter import messagebox
import webbrowser

# Import your original View files
import View_Supply, View_Admin, View_Cashier

class SupermarketGenie(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🧞‍♂️ GENIE RETAIL OS")
        self.geometry("1350x800")
        self.attributes("-alpha", 0.0)
        
        self.current_theme = "dark" 
        self.setup_themes()
        
        self.logo_path = r"C:\Users\amgha\OneDrive\Desktop\Programmation C\SupermarketGenie\Icon.png"
        
        # FIXED: Explicitly set the main screen background
        self.main_screen = ctk.CTkFrame(self, fg_color="transparent")
        self.main_screen.pack(fill="both", expand=True)
        
        ctk.set_appearance_mode(self.current_theme)
        
        # Initial Boot
        self.show_loading_screen("SYSTEM INITIALIZING...", self.show_login)

    def setup_themes(self):
        self.themes = {
            "dark": {"bg": "#0a0b10", "card": "#12141d", "text": "#ffffff", "subtext": "#636da6", "border": "#1f2335", "accent": "#7aa2f7"},
            "light": {"bg": "#f8f9fc", "card": "#ffffff", "text": "#1a1b26", "subtext": "#4e5173", "border": "#e2e8f0", "accent": "#3d59a1"}
        }

    # --- UPDATED THEME TOGGLE (THE "FIX") ---
    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        t = self.themes[self.current_theme]
        
        # Force the Window and Appearance mode to update
        ctk.set_appearance_mode(self.current_theme)
        self.configure(fg_color=t["bg"]) 
        
        # Reload the current view to apply the new color dictionary
        if hasattr(self, 'current_view_name'):
            if self.current_view_name == "hub":
                self.show_hub()
            else:
                self.show_login()

    def animate_fade(self, target, step=0.04, callback=None):
        curr = self.attributes("-alpha")
        if abs(curr - target) > 0.01:
            next_alpha = curr + step if curr < target else curr - step
            self.attributes("-alpha", max(0, min(1, next_alpha)))
            self.after(10, lambda: self.animate_fade(target, step, callback))
        elif callback:
            callback()

    def show_loading_screen(self, message, next_func):
        self.clear_screen()
        t = self.themes[self.current_theme]
        self.configure(fg_color=t["bg"]) # Set root window color
        self.animate_fade(1.0)

        container = ctk.CTkFrame(self.main_screen, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(container, text=message, font=("Georgia", 48, "italic", "bold"), 
                     text_color=t["text"]).pack(pady=(0, 40))
        
        self.bar = ctk.CTkProgressBar(container, width=600, height=14, corner_radius=10,
                                       fg_color=t["border"], progress_color=t["accent"])
        self.bar.pack(pady=10)
        self.bar.set(0)

        self.run_cubic_loading(0, next_func)

    def run_cubic_loading(self, val, next_func):
        if val <= 1.0:
            self.bar.set(val)
            increment = 0.008 if val < 0.4 else (0.06 if val < 0.7 else 0.2)
            self.after(35, lambda: self.run_cubic_loading(val + increment, next_func))
        else:
            self.after(500, next_func)

    def clear_screen(self):
        for widget in self.main_screen.winfo_children(): widget.destroy()

    # --- LOGIN ---
    def show_login(self):
        self.current_view_name = "login"
        self.clear_screen()
        t = self.themes[self.current_theme]
        self.configure(fg_color=t["bg"])

        ctk.CTkButton(self.main_screen, text="🌓", width=45, height=45, fg_color=t["card"], 
                      text_color=t["text"], corner_radius=12, command=self.toggle_theme).place(relx=0.97, rely=0.03, anchor="ne")

        if os.path.exists(self.logo_path):
            img = ctk.CTkImage(Image.open(self.logo_path), size=(200, 200))
            ctk.CTkLabel(self.main_screen, image=img, text="").pack(pady=(40, 5))

        ctk.CTkLabel(self.main_screen, text="SEAMLESS LOGISTICS. SUPERIOR CONTROL.", 
                     font=("Georgia", 24, "italic", "bold"), text_color=t["accent"]).pack()
        ctk.CTkLabel(self.main_screen, text="Designed, Coded, and Operated by Bakr Amghar", 
                     font=("Segoe UI", 12, "italic"), text_color=t["subtext"]).pack(pady=(2, 0))
        
        card = ctk.CTkFrame(self.main_screen, width=440, height=360, fg_color=t["card"], corner_radius=25, border_width=1, border_color=t["border"])
        card.pack(pady=30); card.pack_propagate(False)

        ctk.CTkLabel(card, text="SYSTEM AUTHORIZATION", font=("Segoe UI", 22, "bold"), text_color=t["text"]).pack(pady=(40, 15))
        u_ent = ctk.CTkEntry(card, placeholder_text="User ID", width=340, height=50, fg_color=t["bg"])
        u_ent.pack(pady=10)
        p_ent = ctk.CTkEntry(card, placeholder_text="Access Token", show="*", width=340, height=50, fg_color=t["bg"])
        p_ent.pack(pady=10)

        ctk.CTkButton(card, text="INITIALIZE SESSION", width=340, height=55, fg_color=t["accent"], 
                      font=("Segoe UI", 16, "bold"), command=lambda: self.handle_login(u_ent.get(), p_ent.get())).pack(pady=25)
        self.add_footer(self.main_screen, t)

    def handle_login(self, u, p):
        if u == "admin" and p == "1234":
            self.animate_fade(0, callback=lambda: self.show_loading_screen("Welcome Back at Shopping.test", self.show_hub))
        else:
            messagebox.showerror("Security", "Invalid Credentials")

    # --- HUB ---
    def show_hub(self):
        self.current_view_name = "hub"
        self.clear_screen()
        self.animate_fade(1.0)
        t = self.themes[self.current_theme]
        self.configure(fg_color=t["bg"])

        ctk.CTkButton(self.main_screen, text="🌓", width=45, height=45, fg_color=t["card"], 
                      text_color=t["text"], corner_radius=12, command=self.toggle_theme).place(relx=0.97, rely=0.03, anchor="ne")

        if os.path.exists(self.logo_path):
            hub_img = ctk.CTkImage(Image.open(self.logo_path), size=(160, 160))
            ctk.CTkLabel(self.main_screen, image=hub_img, text="").pack(pady=(30, 5))

        ctk.CTkLabel(self.main_screen, text="GENIE CONTROL CENTER", font=("Segoe UI", 36, "bold"), text_color=t["text"]).pack()
        ctk.CTkLabel(self.main_screen, text="Seamless Logistics. Superior Control.", 
                     font=("Georgia", 18, "italic", "bold"), text_color=t["accent"]).pack(pady=5)
        ctk.CTkLabel(self.main_screen, text="Designed, Coded, and Operated by Bakr Amghar", 
                     font=("Segoe UI", 11, "italic"), text_color=t["subtext"]).pack()

        btn_frame = ctk.CTkFrame(self.main_screen, fg_color="transparent")
        btn_frame.pack(expand=True)

        for text, color, key in [("🛒 CASHIER", "#22c55e", "cashier"), ("📦 SUPPLY", "#3b82f6", "supply"), ("🏛️ ADMIN", "#a855f7", "admin")]:
            ctk.CTkButton(btn_frame, text=text, width=280, height=180, fg_color=t["card"], text_color=color,
                          font=("Segoe UI", 22, "bold"), corner_radius=30, border_width=1, border_color=t["border"],
                          hover_color=t["bg"], command=lambda k=key, c=color: self.secure_entry(k, c)).pack(side="left", padx=20)

        ctk.CTkButton(self.main_screen, text="TERMINATE SESSION", fg_color="transparent", text_color="#ef4444", 
                      font=("Segoe UI", 12, "bold"), command=self.show_login).pack(side="bottom", pady=20)
        self.add_footer(self.main_screen, t)

    def secure_entry(self, key, color):
        t = self.themes[self.current_theme]
        pop = ctk.CTkToplevel(self)
        pop.configure(fg_color=t["bg"]); pop.attributes("-topmost", True)
        pop.geometry("420x340")
        px = self.winfo_x() + (1350//2) - 210; py = self.winfo_y() + (800//2) - 170
        pop.geometry(f"+{px}+{py}")
        
        ctk.CTkLabel(pop, text="VERIFY ACCESS", font=("Segoe UI", 20, "bold"), text_color=t["text"]).pack(pady=40)
        ent = ctk.CTkEntry(pop, show="*", width=300, height=50, fg_color=t["card"]); ent.pack()
        ctk.CTkButton(pop, text="VERIFY", fg_color=color, width=300, height=50, corner_radius=12,
                      command=lambda: [pop.destroy(), self.load_module(key)] if ent.get()=="1234" else None).pack(pady=25)

    def load_module(self, key):
        self.clear_screen(); t = self.themes[self.current_theme]
        self.configure(fg_color=t["bg"])
        nav = ctk.CTkFrame(self.main_screen, height=70, fg_color=t["card"], border_width=1, border_color=t["border"])
        nav.pack(fill="x")
        ctk.CTkButton(nav, text="← HUB", command=self.show_hub, width=120, height=40, fg_color=t["accent"]).pack(side="left", padx=20)
        
        content = ctk.CTkFrame(self.main_screen, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=20)
        
        if key == "cashier": View_Cashier.CashierFrame(content).pack(fill="both", expand=True)
        elif key == "supply": View_Supply.SupplyFrame(content).pack(fill="both", expand=True)
        elif key == "admin": View_Admin.AdminFrame(content).pack(fill="both", expand=True)

    def add_footer(self, parent, theme):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(side="bottom", pady=20)
        ctk.CTkLabel(f, text="GitHub: @BakrAmghar", font=("Consolas", 11, "bold"), text_color=theme["accent"]).pack(side="left", padx=20)
        ctk.CTkLabel(f, text="LinkedIn: Bakr Amghar", font=("Consolas", 11, "bold"), text_color=theme["accent"]).pack(side="left", padx=20)

if __name__ == "__main__":
    app = SupermarketGenie()
    app.mainloop()