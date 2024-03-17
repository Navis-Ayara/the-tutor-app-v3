import flet as ft
import os

def print_all_sessions():
    chat_history_files = [f for f in os.listdir('data/history') if f.startswith('chat_history_')]
    if not chat_history_files:
        print("No saved sessions found.")
    else:
        print("Saved sessions:")
        for file in chat_history_files:
            session_id = file.split('_')[2].split('.')[0]
            print(f"Session ID: {session_id}")

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

    recent_sessions = []

    def load_chat(e):
        page.session.set("session_id", e.control.content.value)

        page.go("/chat")

    chat_history_files = [f for f in os.listdir('data/history') if f.startswith('chat_history_')]
    
    for file in chat_history_files:
        session_id = file.split('_')[2].split('.')[0]
        recent_sessions.append(
            ft.Container(
                padding=5,
                border_radius=5,
                content=ft.Text(
                    value=session_id
                ),
                on_click=load_chat
            )
        )

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
                    value=i,
                    size=16,
                    weight=ft.FontWeight.W_500
                ),
                alignment=ft.alignment.center
            )
            for i in subjects
        ], scroll=ft.ScrollMode.ALWAYS),
        ft.Container(
            padding=10,
            content=ft.Text(
                value="Recent Sessions",
                size=18,
                weight=ft.FontWeight.W_600
            )
        ),
        ft.ListView(
            spacing=10,
            auto_scroll=True,
            controls=recent_sessions if recent_sessions else [
                ft.Text(
                    value="No recent sessions found"
                )
            ],
        )
    ])