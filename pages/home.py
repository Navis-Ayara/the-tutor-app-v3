import flet as ft

def _home(page: ft.Page):
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
                bgcolor=ft.colors.SECONDARY_CONTAINER
            )
        for i in range(7)], scroll=ft.ScrollMode.ALWAYS),
        ft.Container(
            padding=10,
            content=ft.Row([
                ft.Text(
                    value="Recent Sessions",
                    size=18,
                    weight=ft.FontWeight.W_600
                ),
                ft.TextButton(
                    text="See More"
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ),
        ft.ListView([
            ft.Container(
                height=50,
                bgcolor=ft.colors.TERTIARY_CONTAINER,
                border_radius=17,
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
