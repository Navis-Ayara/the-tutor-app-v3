import flet as ft
from pages.home import _home

class Home(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.page = page

        self.scroll = ft.ScrollMode.ADAPTIVE

        self.padding = ft.padding.only(left=10)

        self.appbar = ft.AppBar(
            elevation=10,
            leading=ft.Container(
                margin=ft.margin.only(left=10),
                content=ft.CircleAvatar(bgcolor=ft.colors.BACKGROUND)
            ),
            actions=[
                ft.Container(
                    margin=ft.margin.only(right=10),
                    content=ft.IconButton(
                        icon=ft.icons.MENU_ROUNDED,
                        style=ft.ButtonStyle(
                            side=ft.BorderSide(0.7, ft.colors.OUTLINE_VARIANT),
                            color=ft.colors.OUTLINE_VARIANT
                        )
                    )
                )
            ]
        )

        self.navigation_bar = ft.NavigationBar(
            on_change=self.navigate,
            elevation=0,
            label_behavior=ft.NavigationBarLabelBehavior.ONLY_SHOW_SELECTED,
            destinations=[
                ft.NavigationDestination(  
                    label="Home",
                    icon_content=ft.Container(
                        content=ft.Image(
                            src="icons/Home.svg",
                            color=ft.colors.OUTLINE_VARIANT,
                            width=32
                        )
                    ),
                    selected_icon_content=ft.Container(
                        content=ft.Image(
                            src="icons/Home.svg",
                            color=ft.colors.ON_BACKGROUND,
                            width=32
                        )
                    )
                ),
                ft.NavigationDestination(
                    label="Quiz",
                    icon_content=ft.Container(
                        content=ft.Image(
                            src="icons/Sun.svg",
                            color=ft.colors.OUTLINE_VARIANT,
                            width=32
                        )
                    ),
                    selected_icon_content=ft.Container(
                        content=ft.Image(
                            src="icons/Sun.svg",
                            color=ft.colors.ON_BACKGROUND,
                            width=32
                        )
                    )
                ),
                ft.NavigationDestination(
                    label="History",
                    icon_content=ft.Container(
                        content=ft.Image(
                            src="icons/Clock.svg",
                            color=ft.colors.OUTLINE_VARIANT,
                            width=32
                        )
                    ),
                    selected_icon_content=ft.Container(
                        content=ft.Image(
                            src="icons/Clock.svg",
                            color=ft.colors.ON_BACKGROUND,
                            width=32
                        )
                    )
                ),
                ft.NavigationDestination(
                    label="Profile",
                    icon_content=ft.Container(
                        content=ft.Image(
                            src="icons/User.svg",
                            color=ft.colors.OUTLINE_VARIANT,
                            width=32
                        )
                    ),
                    selected_icon_content=ft.Container(
                        content=ft.Image(
                            src="icons/User.svg",
                            color=ft.colors.ON_BACKGROUND,
                            width=32
                        )
                    )
                )
            ]
        )
        self.controls = [
            _home(self.page)
        ]

    def navigate(self, e):
        match e.control.selected_index:
            case 0:
                self.appbar = ft.AppBar(
                    elevation=10,
                    leading=ft.Container(
                        margin=ft.margin.only(left=10),
                        content=ft.CircleAvatar(bgcolor=ft.colors.BACKGROUND)
                    ),
                    actions=[
                        ft.Container(
                            margin=ft.margin.only(right=10),
                            content=ft.IconButton(
                                icon=ft.icons.MENU_ROUNDED,
                                style=ft.ButtonStyle(
                                    side=ft.BorderSide(0.7, ft.colors.OUTLINE_VARIANT),
                                    color=ft.colors.OUTLINE_VARIANT
                                )
                            )
                        )
                    ]
                )

                self.controls.clear()
                self.controls.append(
                    _home(self.page)
                )

            case 1:
                self.appbar = ft.AppBar(
                    elevation=10,
                    automatically_imply_leading=False,
                    title=ft.Text(
                        value="Quiz",
                        size=20,
                        weight=ft.FontWeight.BOLD
                    )
                )

                self.controls.clear()
                self.controls.append(
                    ft.Text(
                        value="Quizz"
                    )
                )

            case 2:
                self.appbar = ft.AppBar(
                    elevation=10,
                    title=ft.Text(
                        value="Sessions History",
                        size=20,
                        weight=ft.FontWeight.BOLD
                    ),
                    center_title=True,
                    automatically_imply_leading=False,
                )

                self.controls.clear()

            case 3:
                self.appbar = ft.AppBar(
                    elevation=10,
                    leading=ft.Container(
                        margin=ft.margin.only(left=10),
                        content=ft.CircleAvatar(bgcolor=ft.colors.BACKGROUND)
                    ),
                    title=ft.Text(
                        value="Profile",
                        size=20,
                        weight=ft.FontWeight.BOLD
                    ),
                    center_title=True
                )

                self.controls.clear()
                self.controls.append(
                    ft.Text("Profile")
                )
        
        self.page.update()
