import flet as ft

def _home(page: ft.Page):
    def go_to_chat(e):
        page.session.set("selected subject", e.control.content.value)
        page.go("/chat")

    subjects = [
        "Mathematics",
        "English",
        "Kiswahili",
        "Chemistry",
        "Biology",
        "Chemistry",
        "Human Sciences",
        "Computer Studies",
        "French",
        "Agriculture"
    ]

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
                on_click=go_to_chat,
                content=ft.Text(
                    value=i
                ),
                alignment=ft.alignment.center
            )
        for i in subjects], scroll=ft.ScrollMode.ALWAYS),
        ft.Container(
            padding=10,
            content=ft.Text(
                value="Recent Sessions",
                size=18,
                weight=ft.FontWeight.W_600
            )
        ),
        ft.ListView([
            ft.Text(
                value="Your history will appear here"
            )
        ], spacing=10)
    ])
