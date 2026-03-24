# GenieViews.py
import flet as ft
import GenieEngine

class AdminView(ft.Container):
    def __init__(self):
        super().__init__(expand=True, padding=40, bgcolor="#0b0e14")
        stats = GenieEngine.get_stats()
        self.content = ft.Column([
            ft.Text("ADMIN DASHBOARD", size=32, weight="black", color="#ffffff"),
            ft.Divider(height=30, color="#24283b"),
            ft.Row([
                self.stat_card("INVESTMENT", f"${stats['inv']:.2f}", "#7aa2f7"),
                self.stat_card("PROFIT", f"${stats['profit']:.2f}", "#9ece6a"),
            ], spacing=20)
        ])

    def stat_card(self, title, val, color):
        return ft.Container(
            expand=True, bgcolor="#16161e", padding=30, border_radius=20,
            border=ft.Border.all(1, "#24283b"),
            content=ft.Column([
                # FIXED: letter_spacing ONLY lives in TextStyle now
                ft.Text(
                    title, 
                    color=color, 
                    weight="bold", 
                    size=12,
                    style=ft.TextStyle(letter_spacing=1.5)
                ),
                ft.Text(val, size=35, weight="bold", color="white")
            ])
        )

class CashierView(ft.Container):
    def __init__(self):
        super().__init__(expand=True, padding=40, content=ft.Text("CASHIER TERMINAL", size=30, color="white", weight="black"))

class SupplyView(ft.Container):
    def __init__(self):
        super().__init__(expand=True, padding=40, content=ft.Text("SUPPLY MANAGER", size=30, color="white", weight="black"))