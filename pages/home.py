import flet as ft

def _home(page: ft.Page):
    def go_to_chat(e):
        page.go("/chat")

    return ft.Column([
        ft.Container(
            padding=10,
            content=ft.Text(
                value="Subjects",
                size=18,
                weight=ft.FontWeight.W_600
            )
        ),
        ft.Row([
            ft.Container(
                width=200,
                height=200,
                border_radius=17,
                bgcolor=ft.colors.SECONDARY_CONTAINER,
                on_click=go_to_chat
            )
        for i in range(7)], scroll=ft.ScrollMode.ALWAYS),
        ft.Container(
            padding=10,
            content=ft.Text(
                value="Recent Sessions",
                size=18,
                weight=ft.FontWeight.W_600
            )
        ),
        ft.ListView([
            ft.Container(
                height=50,
                bgcolor=ft.colors.TERTIARY_CONTAINER,
                border_radius=12,
                padding=7,
                content=ft.Column([
                    ft.Text(
                        value="Yesterday",
                        size=15,
                        weight=ft.FontWeight.W_600
                    ),
                    ft.Text(
                        value="This is a history item",
                        size=14
                    )
                ], spacing=0)
            )
        for i in range(5)], spacing=10)
    ])
