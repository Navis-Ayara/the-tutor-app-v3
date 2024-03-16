import flet as ft

def quiz_tab(page: ft.Page):
    page.expand = True

    return ft.Column(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.ListView(
                
            ),
            ft.Container(
                padding=10,
                content=ft.Row([
                    
                ])
            )
        ]
    )