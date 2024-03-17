import flet as ft


def settings(page: ft.Page):

    dlg = ft.AlertDialog(
        title=ft.Text(
            value="About",
            size=18,
            weight=ft.FontWeight.BOLD
        ),
        content=ft.Column([
            ft.Text("App Version: 1.0.0")
        ], expand=False)
    )

    def open_about(e):
        page.dialog = dlg
        dlg.open = True
        page.update()

    def theme_changed(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        c.label = (
            "Light theme" if page.theme_mode == ft.ThemeMode.LIGHT else "Dark theme"
        )
        page.update()
    c = ft.Switch(label="Light theme", on_change=theme_changed)
    return ft.Column([
        c,
        ft.ElevatedButton(
            icon=ft.icons.INFO_OUTLINE,
            text="About",
            on_click=open_about
        )
    ])
