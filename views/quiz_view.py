import flet as ft

class QuizView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.route = "/quiz"

        self.padding = 0

        self.messages = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True
        )

        self.message_box = ft.TextField(
            on_change=self.change_border_radius,
            filled=True,
            expand=True,
            border_radius=50,
            shift_enter=True,
            max_lines=5
        )

        self.appbar = ft.AppBar(
            leading=ft.IconButton(
                icon=ft.icons.ARROW_BACK_ROUNDED,
                on_click=lambda _: page.go("/")
            ),
            title=ft.Text("Quiz"),
        )

        self.controls = [
            self.messages,
            ft.Container(
                bgcolor=ft.colors.SECONDARY_CONTAINER,
                padding=10,
                content=ft.Row([
                    self.message_box,
                    ft.Container(
                        height=65,
                        alignment=ft.alignment.center,
                        content=ft.IconButton(
                            icon=ft.icons.SEND_ROUNDED,
                            on_click=self.send
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

    def send(self, e):
        self.messages.controls.append(
            ft.Container(
                expand=False,
                padding=7,
                content=ft.Row([
                    ft.Text(
                        value="You:",
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Text(
                        self.message_box.value,
                        weight=ft.FontWeight.BOLD
                    ),
                ])
            )
        )

        self.message_box.value = ""

        self.page.update()