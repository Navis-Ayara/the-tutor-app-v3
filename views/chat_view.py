import flet as ft
import json
import uuid
import os

import google.generativeai as genai

genai.configure(api_key="AIzaSyA7OvzovsBECbn1P5N3UuZYqex8iR6hu6s")

# Set up the model
generation_config = {
  "temperature": 0.75,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_LOW_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_LOW_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_LOW_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_LOW_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["You are a highly knowledgeable and experienced AI assistant specializing in mathematics. You possess a deep understanding of various mathematical fields and can explain complex concepts in a clear and concise manner.Additionally:Focus on providing solutions and explanations: When presented with a problem, prioritize providing clear and well-explained solutions, not just answers.Adapt to different levels of expertise: Tailor your communication and explanations to the user's level of understanding, avoiding overly technical language unless necessary.Encourage exploration and learning: Guide users towards additional resources or suggest alternative approaches to problem-solving, fostering independent learning and critical thinking.Maintain ethical boundaries: Avoid providing complete solutions to complex problems, especially for academic purposes.Example:User: I'm struggling to understand the concept of group theory. Can you explain it to me?\nChatbot: Absolutely! Group theory is a branch of abstract algebra that studies the properties of groups. A group consists of a set of elements and a binary operation that combines any two elements to produce another element within the set. This operation must satisfy certain properties like associativity, identity, and inverses, defining the structure of the group. Here are some resources that offer further explanation with interactive examples, allowing you to explore the concept at your own pace."]
  },
  {
    "role": "model",
    "parts": ["Certainly! Graph theory is a fascinating field of mathematics that studies the relationships between vertices and edges in graphs. Here are the steps involved in solving a graph theory problem:\n\n1. **Understand the problem:** Read the problem carefully and identify the given information and what you need to find.\n\n2. **Draw a graph:** If the problem does not already provide a graph, draw one to visualize the relationships between the vertices and edges.\n\n3. **Apply graph theory concepts:** Use your knowledge of graph theory concepts like paths, cycles, connectivity, and coloring to analyze the graph and find the solution.\n\n4. **Prove or explain your solution:** Once you have a solution, prove it using mathematical reasoning or provide an explanation of how you arrived at it.\n\nHere are some additional tips that may help you:\n\n* **Break down the problem:** If the problem is complex, break it down into smaller, more manageable parts.\n* **Consider different approaches:** There may be multiple ways to solve a graph theory problem. Explore different approaches and choose the one that seems most efficient.\n* **Use graph theory tools:** There are many tools available to help you solve graph theory problems, such as software and online resources.\n\nPlease let me know if you have any specific graph theory problems that you need help with. I would be happy to provide guidance and協助."]
  },
  {
    "role": "user",
    "parts": ["You are a \"Reply-as-text\" model. You cannot generate visual elements"]
  },
  {
    "role": "model",
    "parts": ["My apologies. As a \"Reply-as-text\" model, I cannot generate visual elements like graphs. However, I can still provide you with step-by-step instructions on how to draw a graph, or I can verbally describe the graph to you.\n\nFor example, if you need help drawing a graph to represent a social network, I could give you the following instructions:\n\n1. Draw a circle for each person in the network.\n2. Draw a line between each pair of people who are friends.\n\nOnce you have drawn the graph, you can use it to answer questions about the social network, such as:\n\n* Who has the most friends?\n* Are there any groups of people who are all friends with each other?\n* Is it possible to get from one person to another by only following friendship connections?\n\nI hope this helps!"]
  },
])


def save_chat_history(chat_history, session_id):
    file_path = f"data/history/chat_history_{session_id}.json"
    with open(file_path, "w") as file:
        json.dump(chat_history, file, indent=4)

def load_chat_history(session_id):
    file_path = f"/data/history/chat_history_{session_id}.json"
    try:
        with open(file_path, "r") as file:
            chat_history = json.load(file)
    except FileNotFoundError:
        chat_history = []
    return chat_history

def print_chat_history(chat_history):
    for item in chat_history:
        role = item["role"]
        parts = item["parts"]
        for part in parts:
            print(f"{role}: {part}")

def print_all_sessions():
    chat_history_files = [f for f in os.listdir('/data/history/') if f.startswith('chat_history_')]
    if not chat_history_files:
        print("No saved sessions found.")
    else:
        print("Saved sessions:")
        for file in chat_history_files:
            session_id = file.split('_')[1].split('.')[0]
            print(f"Session ID: {session_id}")

class ChatView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.route = "/chat"
        self.page = page

        self.session_id = self.page.session.get("session_id")

        self.chat_history = []

        self.messages = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True
        )

        if self.session_id != None:
            chat_history = load_chat_history(self.session_id)
            for message in chat_history:
                role = message["role"]
                parts = message["parts"]
                for part in parts:
                    self.messages.controls.append(
                        ft.Container(
                            expand=False,
                            padding=7,
                            content=ft.Row([
                                ft.Text(
                                    value=f"{role}:",
                                    weight=ft.FontWeight.BOLD
                                ),
                                ft.Text(
                                    part,
                                    weight=ft.FontWeight.BOLD
                                ),
                            ])
                        )
                    )

        else:
            self.new_session()

        self.padding = 0
        
        self.message_box = ft.TextField(
            on_change=self.change_border_radius,
            filled=True,
            expand=True,
            border_radius=50,
            shift_enter=True,
            max_lines=5
        )

        self.appbar = ft.AppBar(
            leading=ft.IconButton(
                icon=ft.icons.ARROW_BACK_ROUNDED,
                on_click=lambda _: page.go("/")
            ),
            title=ft.Text(f"{page.session.get('selected subject')}"),
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            text="Save Session",
                            on_click=self.save_session
                        ),
                        ft.PopupMenuItem(
                            text="New session",
                            on_click=self.new_session
                        )
                    ]
                )
            ]
        )

        self.controls = [
            self.messages,
            ft.Container(
                bgcolor=ft.colors.SECONDARY_CONTAINER,
                padding=10,
                content=ft.Row([
                    self.message_box,
                    ft.Container(
                        height=65,
                        alignment=ft.alignment.center,
                        content=ft.IconButton(
                            icon=ft.icons.SEND_ROUNDED,
                            on_click=self.send
                        )
                    )
                ], tight=True, vertical_alignment=ft.CrossAxisAlignment.END)
            )
        ]

    def change_border_radius(self, e):
        if len(e.control.value) > 19:
            e.control.border_radius = 14
        else:
            e.control.border_radius = 50
        self.page.update()

    def send(self, e):
        user_message = self.message_box.value
        self.chat_history.append({"role": "user", "parts": [user_message]})

        self.messages.controls.append(
            ft.Container(
                expand=False,
                padding=7,
                content=ft.Row([
                    ft.Text(
                        value="You:",
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Text(
                        user_message,
                        weight=ft.FontWeight.BOLD
                    ),
                ])
            )
        )
        self.page.update()

        convo.send_message(user_message)

        self.messages.controls.append(
            ft.Container(
                expand=False,
                padding=7,
                content=ft.Row([
                    ft.Text(
                        value="Tutor:",
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Markdown(
                        value=convo.last.text,
                        selectable=True,
                        auto_follow_links=True,
                        expand=True
                    )
                ], vertical_alignment=ft.CrossAxisAlignment.START)
            )
        )

        self.chat_history.append({"role": "model", "parts": [convo.last.text]})

        self.save_session()

        self.message_box.value = ""
        self.page.update()

    def save_session(self, e):
        if not self.session_id:
            self.session_id = str(uuid.uuid4())
            self.page.session.set("session_id", self.session_id)
        save_chat_history(self.chat_history, self.session_id)

    def new_session(self, e=None):
        self.session_id = str(uuid.uuid4())
        self.page.session.set("session_id", self.session_id)
        self.chat_history = []
        self.messages.controls = []
        self.page.update()