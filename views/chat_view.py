import flet as ft

class ChatView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.route = "/chat"

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

        
