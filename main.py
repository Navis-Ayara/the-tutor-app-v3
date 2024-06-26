import flet as ft
from router import route_handler

def main(page: ft.Page):
    page.title = "The Tutor"

    # window settings
    page.window_always_on_top = True
    page.window_title_bar_buttons_hidden = True
    page.window_title_bar_hidden = True
    page.padding = ft.padding.only(left=10)

    page.fonts = {
        "Onest": "fonts/Onest.ttf"
    }

    # theming
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(
        page_transitions=ft.PageTransitionsTheme(
            windows=ft.PageTransitionTheme.OPEN_UPWARDS
        ),
        font_family="Onest",
        text_theme=ft.TextTheme(
            label_medium=ft.TextStyle(
                size=13,
                weight=ft.FontWeight.BOLD
            )
        ),
        scrollbar_theme=ft.ScrollbarTheme(
            radius=0
        )
    )

    def on_route_change(route):
        page.views.clear()
        page.views.append(
            route_handler(page)[page.route]
        )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_view_pop = view_pop
    page.on_route_change = on_route_change

    page.go("/")

ft.app(target=main, use_color_emoji=True, assets_dir="assets")

