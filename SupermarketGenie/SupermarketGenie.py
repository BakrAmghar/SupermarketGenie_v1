import customtkinter as ctk
from PIL import Image
import os
from tkinter import messagebox
import time

# The 3 Original Pillars
import View_Supply, View_Admin, View_Cashier

class SupermarketGenie(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🧞‍♂️ SUPERMARKET GENIE v2.0 - SECURE TERMINAL")
        self.geometry("1350x800")
        self.configure(fg_color="#0b0b10")

        # Main Screen Container
        self.main_screen = ctk.CTkFrame(self, fg_color="transparent")
        self.main_screen.pack(fill="both", expand=True)

        self.logo_path = r"C:\Users\amgha\OneDrive\Desktop\Programmation C\SupermarketGenie\Icon.png"
        self.show_login()

    def add_legal_protection(self, parent):
        footer = ctk.CTkFrame(parent, height=50, fg_color="transparent")
        footer.pack(side="bottom", fill="x", pady=10)
        footer.pack_propagate(False) 
        txt = "⚠️ SECURED BY KB102-3040 | DEVELOPER: BAKR AMGHAR (EMSI)\nENCRYPTED RETAIL INTELLIGENCE SYSTEM"
        ctk.CTkLabel(footer, text=txt, font=("Segoe UI", 9, "bold"), text_color="#3e3e4a").pack(expand=True)

    def show_login(self):
        """Initial Entrance Screen"""
        for widget in self.main_screen.winfo_children(): widget.destroy()
        
        # Entrance Animation Wrapper
        self.login_wrapper = ctk.CTkFrame(self.main_screen, fg_color="transparent")
        self.login_wrapper.pack(expand=True)

        self.login_card = ctk.CTkFrame(self.login_wrapper, width=450, height=600, 
                                       fg_color="#16161e", corner_radius=35, 
                                       border_width=2, border_color="#7aa2f7")
        self.login_card.pack(pady=20)
        self.login_card.pack_propagate(False)

        if os.path.exists(self.logo_path):
            img = ctk.CTkImage(Image.open(self.logo_path), size=(140, 140))
            ctk.CTkLabel(self.login_card, image=img, text="").pack(pady=(50, 10))
        
        ctk.CTkLabel(self.login_card, text="GENIE ACCESS", font=("Impact", 35), text_color="#7aa2f7").pack()
        
        self.u_ent = ctk.CTkEntry(self.login_card, placeholder_text="Master Username", width=320, height=50, corner_radius=15)
        self.u_ent.pack(pady=15)
        self.p_ent = ctk.CTkEntry(self.login_card, placeholder_text="Master Password", show="*", width=320, height=50, corner_radius=15)
        self.p_ent.pack(pady=5)

        ctk.CTkButton(self.login_card, text="INITIALIZE SYSTEM", width=320, height=55, corner_radius=15,
                      fg_color="#7aa2f7", text_color="#1a1b26", font=("Segoe UI", 14, "bold"),
                      command=self.handle_system_init).pack(pady=35)
        self.add_legal_protection(self.login_card)

    def handle_system_init(self):
        if self.u_ent.get() == "admin" and self.p_ent.get() == "1234":
            self.build_main_ui()
        else: messagebox.showerror("System Error", "Authorization Failed")

    def build_main_ui(self):
        for widget in self.main_screen.winfo_children(): widget.destroy()
        
        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self.main_screen, width=280, fg_color="#11111b", corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        if os.path.exists(self.logo_path):
            s_img = ctk.CTkImage(Image.open(self.logo_path), size=(90, 90))
            ctk.CTkLabel(self.sidebar, image=s_img, text="").pack(pady=(40, 0))
        
        ctk.CTkLabel(self.sidebar, text="GENIE OS", font=("Impact", 24), text_color="#bb9af7").pack(pady=(10, 40))
        
        # Navigation
        nav = [("🛒 CASHIER", "cashier"), ("📦 SUPPLY", "supply"), ("🏛️ ADMIN", "admin")]
        for t, n in nav:
            btn = ctk.CTkButton(self.sidebar, text=t, height=60, fg_color="transparent", 
                                anchor="w", font=("Segoe UI", 15, "bold"), text_color="#a9b1d6", 
                                hover_color="#1e1e2e", corner_radius=10,
                                command=lambda name=n: self.switch_tab(name))
            btn.pack(fill="x", padx=20, pady=5)

        ctk.CTkButton(self.sidebar, text="LOGOUT", text_color="#f7768e", command=self.show_login).pack(side="bottom", pady=30)

        # --- CONTENT AREA ---
        self.container = ctk.CTkFrame(self.main_screen, fg_color="transparent")
        self.container.pack(side="right", fill="both", expand=True)
        
        # BUG FIX: Automatically start on a locked screen (no free preview)
        self.switch_tab("supply")

    def switch_tab(self, tab_name):
        """Standard Switch Tab - ALWAYS starts locked"""
        for widget in self.container.winfo_children(): widget.destroy()
        self.add_legal_protection(self.container)

        # 1. Load the target view (but keep it hidden under the lock)
        if tab_name == "cashier": self.view = View_Cashier.CashierFrame(self.container)
        elif tab_name == "supply": self.view = View_Supply.SupplyFrame(self.container)
        elif tab_name == "admin": self.view = View_Admin.AdminFrame(self.container)
        
        self.view.pack(fill="both", expand=True)

        # 2. Drop the Security Shield (The Lock Screen)
        self.security_shield = ctk.CTkFrame(self.view, fg_color="#0b0b10") 
        self.security_shield.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Animated Lock Box
        self.lock_box = ctk.CTkFrame(self.security_shield, width=420, height=450, 
                                     fg_color="#16161e", corner_radius=30, 
                                     border_width=2, border_color="#7aa2f7")
        self.lock_box.place(relx=0.5, rely=0.5, anchor="center")
        self.lock_box.pack_propagate(False)
        
        ctk.CTkLabel(self.lock_box, text="🔒 RESTRICTED ZONE", font=("Impact", 28), text_color="#f7768e").pack(pady=(50, 10))
        ctk.CTkLabel(self.lock_box, text=f"ACCESSING: {tab_name.upper()}", font=("Segoe UI", 12), text_color="#565f89").pack()
        
        self.cred_input = ctk.CTkEntry(self.lock_box, placeholder_text="Employee Credentials", 
                                       show="*", width=300, height=55, corner_radius=15, 
                                       fg_color="#0b0b10", border_color="#24283b")
        self.cred_input.pack(pady=40)
        
        self.v_btn = ctk.CTkButton(self.lock_box, text="VERIFY CLEARANCE", width=220, height=50, 
                                   corner_radius=15, fg_color="#7aa2f7", text_color="#1a1b26",
                                   font=("Segoe UI", 14, "bold"), command=self.run_verification_anim)
        self.v_btn.pack()

    def run_verification_anim(self):
        """Complex Unlock Animation Sequence"""
        if self.cred_input.get() == "1234":
            # 1. UI Feedback
            self.v_btn.configure(text="DECRYPTING...", state="disabled", fg_color="#9ece6a")
            self.update()
            time.sleep(0.7)
            
            # 2. Welcome Animation
            self.cred_input.destroy()
            self.v_btn.destroy()
            
            welcome_msg = ctk.CTkLabel(self.lock_box, text="WELCOME BACK,\nKB102-3040", 
                                       font=("Segoe UI", 26, "bold"), text_color="#bb9af7")
            welcome_msg.pack(pady=60)
            
            status = ctk.CTkLabel(self.lock_box, text="Access Granted. Initializing...", font=("Consolas", 11), text_color="#7aa2f7")
            status.pack()
            
            # Sub-animation: Flickering welcome
            for _ in range(3):
                welcome_msg.configure(text_color="#7aa2f7")
                self.update()
                time.sleep(0.1)
                welcome_msg.configure(text_color="#bb9af7")
                self.update()
                time.sleep(0.1)
            
            time.sleep(0.8)
            
            # 3. Lift the shield
            self.security_shield.destroy()
        else:
            # Shake animation (Simulated by moving slightly)
            original_x = 0.5
            for i in range(4):
                offset = 0.01 if i % 2 == 0 else -0.01
                self.lock_box.place(relx=original_x + offset, rely=0.5, anchor="center")
                self.update()
                time.sleep(0.05)
            self.lock_box.place(relx=0.5, rely=0.5, anchor="center")
            messagebox.showerror("Denied", "Security Violation: Invalid Credentials")

if __name__ == "__main__":
    app = SupermarketGenie()
    app.mainloop()