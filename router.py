import flet as ft
from views.main_view import Home
from views.chat_view import ChatView

def route_handler(page: ft.Page):
    return {
        "/": Home(page),
        "/chat": ChatView(page)
    }
