import flet as ft
from router import route_handler

def main(page: ft.Page):
    page.title = "The Tutor"

    # window settings
    page.window_always_on_top = True
    page.window_title_bar_buttons_hidden = True
    page.window_title_bar_hidden = True
    page.padding = ft.padding.only(left=10)

    page.scroll = ft.ScrollMode.ADAPTIVE

    page.fonts = {
        "Onest": "fonts/Onest.ttf"
    }

    # theming
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        page_transitions=ft.PageTransitionsTheme(
            windows=ft.PageTransitionTheme.CUPERTINO
        ),
        font_family="Onest"
    )


    def on_route_change(route):
        page.views.clear()
        page.views.append(
            route_handler(page)[page.route]
        )

        page.update()

    page.on_route_change = on_route_change

    page.go("/")

ft.app(target=main, use_color_emoji=True)

