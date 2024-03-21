import flet as ft
import os

images = [f for f in os.listdir('assets/images')]

def print_all_sessions():
    chat_history_files = [f for f in os.listdir('data/history') if f.startswith('chat_history_')]
    if not chat_history_files:
        print("No saved sessions found.")
    else:
        print("Saved sessions:")
        for file in chat_history_files:
            session_id = file.split('_')[2].split('.')[0]
            print(f"Session ID: {session_id}")


class HomeView(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.page = page
        self.subjects = [
            "Mathematics",
            "English",
            "Kiswahili",
            "Chemistry",
            "Biology",
            "Physics",
            "History",
            "Geography",
            "Computer",
            "French",
            "Agriculture"
        ]
        self.recent_sessions = []
        self.load_recent_sessions()

    def go_to_chat(self, e):
        self.page.session.set("selected subject", e.control.content.value)
        self.page.go("/chat")

    def load_chat(self, e=None):
        self.page.session.set("session_id", e.control.content.value)
        self.page.go("/chat")

    def load_recent_sessions(self):
        self.recent_sessions = []
        chat_history_files = [f for f in os.listdir('data/history') if f.startswith('chat_history_')]

        for file in chat_history_files:
            session_id = file.split('_')[2].split('.')[0]
            self.recent_sessions.append(
                ft.Card(
                    
                )
            )

    def build(self):
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
                    on_click=self.go_to_chat,
                    # image_src=images[i],
                    image_fit=ft.ImageFit.COVER,
                    content=ft.Text(
                        value=i if i != "Mathematics" else "",
                        size=20,
                        weight=ft.FontWeight.W_500
                    ),
                    alignment=ft.alignment.center
                )
                for i in self.subjects
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
                controls=self.recent_sessions if self.recent_sessions else [
                    ft.Text(
                        value="No recent sessions found"
                    )
                ],
            )
        ])