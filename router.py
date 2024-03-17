import flet as ft
from views.main_view import Home
from views.chat_view import ChatView
from views.quiz_view import QuizView

def route_handler(page: ft.Page):
    return {
        "/": Home(page),
        "/chat": ChatView(page),
        "/quiz": QuizView(page)
    }
