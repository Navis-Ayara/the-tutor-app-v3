import flet as ft
from pages.home import HomeView
from pages.settings import settings

class Home(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()

        # view settings
        self.page = page
        self.scroll = ft.ScrollMode.HIDDEN
        self.padding = ft.padding.only(left=10)

        self.appbar = ft.AppBar(
            elevation=10,
            title=ft.Text(
                value="Home",
                size=20,
                weight=ft.FontWeight.BOLD
            ),
            center_title=True
        )

        self.drawer = ft.NavigationDrawer(
            controls=[
                ft.NavigationDrawerDestination(
                    label="What's New?"
                )
            ]
        )

        self.navigation_bar = ft.NavigationBar(
            on_change=self.navigate,
            elevation=0,
            destinations=[
                ft.NavigationDestination(  
                    label="Home",
                    icon_content=ft.Container(
                        content=ft.Image(
                            src="/icons/Home.svg",
                            color=ft.colors.OUTLINE_VARIANT,
                            width=32
                        )
                    ),
                    selected_icon_content=ft.Container(
                        content=ft.Image(
                            src="/icons/Home.svg",
                            color=ft.colors.ON_BACKGROUND,
                            width=32
                        )
                    )
                ),
                ft.NavigationDestination(
                    label="Quiz",
                    icon_content=ft.Container(
                        content=ft.Image(
                            src="/icons/Sun.svg",
                            color=ft.colors.OUTLINE_VARIANT,
                            width=32
                        )
                    ),
                    selected_icon_content=ft.Container(
                        content=ft.Image(
                            src="/icons/Sun.svg",
                            color=ft.colors.ON_BACKGROUND,
                            width=32
                        )
                    )
                ),
                ft.NavigationDestination(
                    label="Settings",
                    icon_content=ft.Container(
                        content=ft.Image(
                            src="/icons/Settings.svg",
                            color=ft.colors.OUTLINE_VARIANT,
                            width=32
                        )
                    ),
                    selected_icon_content=ft.Container(
                        content=ft.Image(
                            src="/icons/Settings.svg",
                            color=ft.colors.ON_BACKGROUND,
                            width=32
                        )
                    )
                )
            ]
        )
        self.controls = [
            HomeView(self.page)
        ]

    
    def navigate(self, e):
        """
        This handles the page changes.
        The logic is quite simple:\n
            \t1) Listen for navbar destination selection changes\n
            \t2) Clear the current page controls\n
            \t3) Map the selected index onto a function that returns the controls of that page\n
        """
        self.controls.clear()
        match e.control.selected_index:
            case 0:
                self.appbar = ft.AppBar(
                    elevation=10,
                    title=ft.Text(
                        value="Home",
                        size=20,
                        weight=ft.FontWeight.BOLD
                    ),
                    center_title=True
                )

                self.controls.append(
                    HomeView(self.page)
                )

            case 1:
                self.page.go("/quiz")

            case 2:
                self.appbar = ft.AppBar(
                    elevation=10,
                    title=ft.Text(
                        value="Settings",
                        size=20,
                        weight=ft.FontWeight.BOLD
                    ),
                    center_title=True
                )

                self.controls.append(
                    settings(self.page)
                )
        
        self.page.update()

