import flet as ft

class ChatView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.route = "/chat"

        self.padding = 0

        self.appbar = ft.AppBar(
            leading=ft.IconButton(
                icon=ft.icons.ARROW_BACK_ROUNDED,
                on_click=lambda _: page.go("/")
            ),
            title=ft.Text("[subject]"),
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            text="Save Session"
                        ),
                        ft.PopupMenuItem(
                            text="New session"
                        )
                    ]
                )
            ]
        )

        self.controls = [
            ft.ListView(
                expand=True
            ),
            ft.Container(
                bgcolor=ft.colors.SECONDARY_CONTAINER,
                padding=10,
                content=ft.Row([
                    ft.TextField(
                        on_change=self.change_border_radius,
                        filled=True,
                        expand=True,
                        border_radius=50,
                        shift_enter=True,
                        max_lines=5
                    ),
                    ft.Container(
                        height=65,
                        alignment=ft.alignment.center,
                        content=ft.IconButton(
                            icon=ft.icons.SEND_ROUNDED
                        )
                    )
                ], tight=True, vertical_alignment=ft.CrossAxisAlignment.END)
            )
        ]

    def change_border_radius(self, e):
        if len(e.control.value) > 19:
            e.control.border_radius = 14

        else:
            e.control.border_radius = 50

        self.page.update()

        
