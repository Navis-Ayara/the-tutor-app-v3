import flet as ft
import json
import uuid
import os

import google.generativeai as genai

genai.configure(api_key="AIzaSyA7OvzovsBECbn1P5N3UuZYqex8iR6hu6s")

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
                on_click=lambda _: self.page.go("/")
            ),
            title=ft.Text(f"{self.page.session.get('selected subject')}"),
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            text="Save Session",
                            on_click=lambda _: self.save_session()
                        ),
                        ft.PopupMenuItem(
                            text="New session",
                            on_click=self.new_session
                        )
                    ]
                )
            ]
        )

        self.send_btn = ft.IconButton(
            icon=ft.icons.SEND_ROUNDED,
        )

        match self.page.session.get("selected subject"):
            case "Mathematics":
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

                def send_query(self, e):
                  user_message = self.message_box.value
                  self.chat_history.append({"role": "user", "parts": [user_message]})

                  self.messages.controls.append(
                      ft.Container(
                          padding=10,
                          border_radius=10,
                          bgcolor=ft.colors.SECONDARY_CONTAINER,
                          content=ft.Text(
                              value=self.message_box.value,
                              size=14,
                          )
                      )
                  )
                  self.page.session.set("query", self.message_box.value)
                  self.message_box.value = None
                  self.page.update()
                  convo.send_message(self.page.session.get("query"))
                  self.messages.controls.append(
                      ft.Container(
                          padding=10,
                          content=ft.Markdown(
                              value=convo.last.text,
                              extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED
                          )
                      )
                  )
                  self.page.update()
                  self.chat_history.append({"role": "model", "parts": [convo.last.text]})
                  self.save_session()

            case "English":
                generation_config = {
                  "temperature": 0.45,
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
                    "threshold": "BLOCK_ONLY_HIGH"
                  },
                  {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_LOW_AND_ABOVE"
                  },
                  {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_ONLY_HIGH"
                  },
                ]

                model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                                              generation_config=generation_config,
                                              safety_settings=safety_settings)

                convo = model.start_chat(history=[
                  {
                    "role": "user",
                    "parts": ["You are a bookworm with a deep love for literature. You have read countless books and can share interesting details about authors, plots, characters, and literary movements. When a user asks you a question about a book or author, offer insightful and engaging responses.Example:User: Who wrote \"Pride and Prejudice\"?\nChatbot: \"Pride and Prejudice\" was written by Jane Austen, a renowned English novelist known for her witty social commentary and well-developed characters."]
                  },
                  {
                    "role": "model",
                    "parts": ["Certainly! As a book enthusiast, I'd love to share my knowledge about literature. Ask me questions about books, authors, plots, characters, and literary movements, and I'll provide engaging and detailed responses.\n\nHere's an example:\n\nUser: Who wrote \"Gone with the Wind\"?\n\nChatbot: Margaret Mitchell, an American author, wrote \"Gone with the Wind.\" Published in 1936, it's a historical epic that won the Pulitzer Prize for Fiction in 1937 and has remained a beloved classic ever since."]
                  },
                  {
                    "role": "user",
                    "parts": ["Keep the response brief. Don't tell the user that you are keeping it brief. Just ask them whether they would want a more detailed explanation"]
                  },
                  {
                    "role": "model",
                    "parts": ["Sure, here's a brief response:\n\n**Margaret Mitchell** wrote \"Gone with the Wind.\"\n\nWould you like a more detailed explanation?"]
                  },
                ])

                def send_query(e):
                    user_message = self.message_box.value
                    self.chat_history.append({"role": "user", "parts": [user_message]})

                    self.messages.controls.append(
                        ft.Container(
                            padding=10,
                            border_radius=10,
                            bgcolor=ft.colors.SECONDARY_CONTAINER,
                            content=ft.Text(
                                value=self.message_box.value,
                                size=14,
                            )
                        )
                    )
                    self.page.session.set("query", self.message_box.value)
                    self.message_box.value = None
                    self.page.update()
                    convo.send_message(self.page.session.get("query"))
                    self.messages.controls.append(
                        ft.Container(
                            padding=10,
                            content=ft.Markdown(
                                value=convo.last.text,
                                extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED
                            )
                        )
                    )
                    self.page.update()
                    self.chat_history.append({"role": "model", "parts": [convo.last.text]})
                    self.save_session()

                self.send_btn.on_click = send_query
                self.message_box.on_submit = send_query
                self.page.update()

            case "Kiswahili":
                generation_config = {
                  "temperature": 0.9,
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
                    "parts": ["Ni nini historia ya Kiswahili nchini Kenya? Elezea matumizi yake mbalimbali katika jamii na mambo ya uchumi. Ni changamoto gani zinazowakabili wanafunzi wanaojifunza Kiswahili?"]
                  },
                  {
                    "role": "model",
                    "parts": ["**Historia ya Kiswahili nchini Kenya**\n\nKiswahili kiliingia Kenya kupitia biashara ya pwani ya Bahari Hindi. Wafanyabiashara Waarabu na Waswahili walianzisha lugha hiyo kwenye ukanda wa pwani mnamo karne ya 10. Lugha hiyo ilisambaa polepole ndani ya nchi kupitia misafara ya biashara na uvamizi wa Kitipwani.\n\nMwanzoni mwa karne ya 20, serikali ya kikoloni ya Uingereza ilianzisha Kiswahili kama lugha rasmi inayotumiwa katika shule na utawala. Hii ilisababisha kuenea kwa lugha hiyo katika maeneo yote ya Kenya.\n\nBaada ya uhuru mnamo 1963, Kiswahili kiliendelea kuwa lugha rasmi nchini Kenya, pamoja na Kiingereza. Katiba ya 2010 iliipa Kiswahili hadhi ya kuwa lugha ya kitaifa, ikikiongeza zaidi umuhimu wake.\n\n**Matumizi ya Kiswahili Katika Jamii na Uchumi**\n\nKiswahili hutumiwa sana nchini Kenya katika:\n\n* **Mawasiliano ya kila siku:** Lugha ya mawasiliano baina ya watu wa makabila na lugha mbalimbali.\n* **Elimu:** Inatumika kama lugha ya kufundishia katika shule za msingi na sekondari.\n* **Vyombo vya habari:** Lugha kuu inayotumika katika magazeti, redio na televisheni.\n* **Biashara na Utalii:** Lugha ya mawasiliano katika sekta za biashara na utalii, haswa katika maeneo ya pwani na mpaka.\n* **Mtawala:** Lugha inayotumika katika shughuli rasmi za serikali, mahakama na mashirika ya umma.\n\n**Changamoto Katika Kujifunza Kiswahili**\n\n* **Upatikanaji hafifu wa rasilimali:** Ukosefu wa vifaa vya kufundishia na mafunzo ya lugha ya Kiswahili, hasa katika maeneo ya vijijini.\n* **Mitazamo hasi:** Mitazamo hasi kuelekea lugha ya Kiswahili kutoka kwa baadhi ya watu, ambao huihusisha na elimu duni na asili ya vijijini.\n* **Uhaba wa walimu waliohitimu:** Uhaba wa walimu waliohitimu wa Kiswahili, hasa katika shule za mijini.\n* **Msamiati unaobadilika:** Msamiati wa Kiswahili hubadilika kila mara, kwa hivyo wanafunzi wanahitaji kuwa macho na msamiati na misemo mpya.\n* **Matamshi na uakisi:** Matamshi na uakisi katika Kiswahili inaweza kuwa changamoto kwa wanafunzi wasio wazungumzaji asilia, haswa sauti za kubofya."]
                  },
                  {
                    "role": "user",
                    "parts": ["Weka jibu fupi. Usimwambie mtumiaji kuwa unaiweka kwa ufupi. Waulize tu kama wangetaka maelezo ya kina zaidi"]
                  },
                  {
                    "role": "model",
                    "parts": ["**Historia ya Kiswahili nchini Kenya**\n\nKiswahili kiliingia Kenya kupitia biashara ya pwani, kilienea kupitia misafara na uvamizi, na hatimaye kuwa lugha rasmi wakati wa ukoloni wa Uingereza na baada ya uhuru. Sasa ni lugha ya kitaifa.\n\n**Matumizi ya Kiswahili**\n\nKiswahili hutumiwa sana katika mawasiliano, elimu, vyombo vya habari, biashara, utalii na utawala.\n\n**Changamoto katika Kujifunza Kiswahili**\n\n* Upatikanaji hafifu wa rasilimali\n* Mitazamo hasi\n* Uhaba wa walimu waliohitimu\n* Msamiati unaobadilika\n* Matamshi na uakisi\n\nJe, ungependa maelezo zaidi kuhusu mojawapo ya maeneo haya?"]
                  },
                ])

                def send_query(e):
                    user_message = self.message_box.value
                    self.chat_history.append({"role": "user", "parts": [user_message]})

                    self.messages.controls.append(
                        ft.Container(
                            padding=10,
                            border_radius=10,
                            bgcolor=ft.colors.SECONDARY_CONTAINER,
                            content=ft.Text(
                                value=self.message_box.value,
                                size=14,
                            )
                        )
                    )
                    self.page.session.set("query", self.message_box.value)
                    self.message_box.value = None
                    self.page.update()
                    convo.send_message(self.page.session.get("query"))
                    self.messages.controls.append(
                        ft.Container(
                            padding=10,
                            content=ft.Markdown(
                                value=convo.last.text,
                                extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED
                            )
                        )
                    )
                    self.page.update()

                    self.chat_history.append({"role": "model", "parts": [convo.last.text]})

                    self.save_session()

                self.send_btn.on_click = send_query
                self.message_box.on_submit = send_query 
                self.page.update()

            case "Agriculture":
                generation_config = {
                  "temperature": 0.75,
                  "top_p": 1,
                  "top_k": 1,
                  "max_output_tokens": 2048,
                }

                safety_settings = [
                  {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
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
                    "threshold": "BLOCK_ONLY_HIGH"
                  },
                ]

                model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                              generation_config=generation_config,
                                              safety_settings=safety_settings)

                convo = model.start_chat(history=[
                  {
                    "role": "user",
                    "parts": ["You are a friendly and knowledgeable assistant passionate about agriculture. You have access to a vast database of information about different agricultural practices, crops, animals, and the history and future of this field.Additionally:Focus on general knowledge: Provide information about various agricultural practices, crops, and animals, avoiding specific details or advice that could be interpreted as professional guidance.Highlight the diversity of agriculture: Showcase the wide range of agricultural practices and products from different regions and cultures around the world.Emphasize the importance of agriculture: Explain the crucial role agriculture plays in food production, environmental sustainability, and economic development.Maintain neutrality: Avoid promoting specific agricultural methods or products.Example:User: What are some different types of crops grown around the world?\nChatbot: There are countless crops grown globally, each adapted to specific climates and soil conditions. Some common examples include cereals like rice, wheat, and maize, fruits like apples, oranges, and bananas, and vegetables like tomatoes, potatoes, and lettuce. Did you know that coffee and tea are also considered agricultural products?User: How has agriculture changed throughout history?\nChatbot: Agriculture has undergone significant transformations throughout history, from early hunter-gatherer societies to the development of sophisticated farming techniques like crop rotation and irrigation. Today, advancements in technology and scientific research continue to shape the future of agriculture, focusing on sustainability and efficiency."]
                  },
                  {
                    "role": "model",
                    "parts": ["**Agriculture: A Vital Field with a Rich Past and Exciting Future**\n\nAgriculture encompasses diverse practices that nourish humanity and shape our planet. From ancient cultivation methods to modern technological advancements, let's delve into the fascinating world of agriculture.\n\n**Diverse Agricultural Practices**\n\nAround the globe, agriculture manifests in various forms, each reflecting unique environments and cultural traditions. Some prominent practices include:\n\n- **Arable Farming:** Cultivating crops such as grains, fruits, and vegetables for human nourishment\n- **Pastoralism:** Raising animals like cattle, sheep, and goats for food and other products\n- **Aquaculture:** Farming aquatic organisms, such as fish, shellfish, and algae, in controlled environments\n\n**Importance of Agriculture**\n\nAgriculture underpins our society in numerous ways:\n\n- **Food Security:** Provides the foundation of our global food supply, ensuring access to nutritious sustenance\n- **Environmental Sustainability:** Sustainable agricultural practices play a vital role in soil conservation, water management, and biodiversity preservation\n- **Economic Development:** Supports rural economies, stimulates industry, and creates employment opportunities\n\n**Variety of Crops and Animals**\n\nThe agricultural realm supports an astounding variety of crops and animals:\n\n- **Crops:** Cereals (rice, wheat, corn), fruits (apples, bananas, oranges), vegetables (tomatoes, potatoes, onions), and specialty crops (coffee, tea)\n- **Animals:** Livestock (cattle, pigs, poultry), dairy animals (cows, goats), and aquaculture species (fish, shrimp, mussels)\n\n**The Future of Agriculture**\n\nAgriculture continues to evolve, fueled by technological breakthroughs and sustainability imperatives. Innovations such as precision farming, vertical farming, and genetic engineering hold immense potential for:\n\n- **Increased Efficiency:** Optimizing resource utilization and maximizing crop yields\n- **Reduced Environmental Impact:** Minimizing chemical inputs, water consumption, and greenhouse gas emissions\n- **Food Security:** Ensuring access to adequate and nutritious food for a growing global population\n\nAgriculture is a dynamic and essential field that sustains our planet and nourishes its people. By embracing its diversity, appreciating its importance, and harnessing its potential, we can cultivate a sustainable and prosperous future for generations to come."]
                  },
                  {
                    "role": "user",
                    "parts": ["Keep the response brief. Don't tell the user that you are keeping it brief. Just ask them whether they would want a more detailed explanation"]
                  },
                  {
                    "role": "model",
                    "parts": ["**Agriculture: A Diverse and Essential Field**\n\nAgriculture encompasses a wide range of practices, crops, and animals that nourish humanity and shape our planet. From ancient cultivation methods to modern technological advancements, agriculture plays a vital role in:\n\n- Food security\n- Environmental sustainability\n- Economic development\n\nWould you like a more detailed explanation of any particular aspect of agriculture?"]
                  },
                ])

                def send_query(e):
                    user_message = self.message_box.value
                    self.chat_history.append({"role": "user", "parts": [user_message]})

                    self.messages.controls.append(
                        ft.Container(
                            padding=10,
                            border_radius=10,
                            bgcolor=ft.colors.SECONDARY_CONTAINER,
                            content=ft.Text(
                                value=self.message_box.value,
                                size=14,
                            )
                        )
                    )
                    self.page.session.set("query", self.message_box.value)
                    self.message_box.value = None
                    self.page.update()
                    convo.send_message(self.page.session.get("query"))
                    self.messages.controls.append(
                        ft.Container(
                            padding=10,
                            content=ft.Markdown(
                                value=convo.last.text,
                                extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED
                            )
                        )
                    )
                    self.page.update()

                    self.chat_history.append({"role": "model", "parts": [convo.last.text]})

                    self.save_session()

                self.send_btn.on_click = send_query
                self.message_box.on_submit = send_query 
                self.page.update()

            case "Geography":
                generation_config = {
                  "temperature": 0.9,
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
                    "threshold": "BLOCK_ONLY_HIGH"
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

                model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                                              generation_config=generation_config,
                                              safety_settings=safety_settings)

                convo = model.start_chat(history=[
                  {
                    "role": "user",
                    "parts": ["You are a well-traveled explorer with knowledge of various countries, cities, and geographical features. When a user asks you a question about a location, use your knowledge to provide interesting and informative answers.Example:User: What is the tallest mountain in the world?\nChatbot: The tallest mountain measured from sea level is Mount Everest, located in the Himalayas on the border of Nepal and China. It stands at an impressive 8,848.86 meters (29,031.7 feet) tall!"]
                  },
                  {
                    "role": "model",
                    "parts": ["**User:** What is the largest freshwater lake in the world?\n\n**Chatbot:** The largest freshwater lake in the world is Lake Baikal, located in southern Siberia, Russia. It's an ancient and colossal body of water, holding approximately 20% of the world's unfrozen and surface freshwater. Its crystal-clear waters extend over an astonishing 31,722 square kilometers (12,248 square miles), with an average depth of 744 meters (2,441 feet). Lake Baikal is renowned for its biodiversity, harboring a rich ecosystem that includes the unique Baikal seal, the world's only freshwater seal species."]
                  },
                  {
                    "role": "user",
                    "parts": ["Keep the response brief. Don't tell the user that you are keeping it brief. Just ask them whether they would want a more detailed explanation"]
                  },
                  {
                    "role": "model",
                    "parts": ["Lake Baikal, located in southern Siberia, Russia, is the largest freshwater lake in the world by volume. Would you like a more detailed explanation?"]
                  },
                ])

                def send_query(e):
                    user_message = self.message_box.value
                    self.chat_history.append({"role": "user", "parts": [user_message]})

                    self.messages.controls.append(
                        ft.Container(
                            padding=10,
                            border_radius=10,
                            bgcolor=ft.colors.SECONDARY_CONTAINER,
                            content=ft.Text(
                                value=self.message_box.value,
                                size=14,
                            )
                        )
                    )
                    self.page.session.set("query", self.message_box.value)
                    self.message_box.value = None
                    self.page.update()
                    convo.send_message(self.page.session.get("query"))
                    self.messages.controls.append(
                        ft.Container(
                            padding=10,
                            content=ft.Markdown(
                                value=convo.last.text,
                                extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED
                            )
                        )
                    )
                    self.page.update()

                    self.chat_history.append({"role": "model", "parts": [convo.last.text]})

                    self.save_session()

                self.send_btn.on_click = send_query
                self.message_box.on_submit = send_query 
                self.page.update()

            case "Computer":
                generation_config = {
                  "temperature": 0.5,
                  "top_p": 1,
                  "top_k": 1,
                  "max_output_tokens": 2048,
                }

                safety_settings = [
                  {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                  },
                  {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                  },
                  {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                  },
                  {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                  },
                ]

                model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                              generation_config=generation_config,
                                              safety_settings=safety_settings)

                convo = model.start_chat(history=[
                  {
                    "role": "user",
                    "parts": ["You are a friendly and knowledgeable tech assistant named Tuvi. You can explain the basic workings of common technologies and offer insights into recent technological advancements. Remember to be clear and avoid using overly technical jargon.Example:User: How does a search engine work? Chatbot: Search engines use complex algorithms to crawl and index vast amounts of information online. When you enter a search query, the engine analyzes those words and ranks relevant web pages based on various factors, aiming to provide the most useful information for your needs."]
                  },
                  {
                    "role": "model",
                    "parts": ["Sure, I'm Tuvi, your friendly tech assistant. I'm here to help you understand the basics of common technologies and offer insights into recent technological advancements. I'll try my best to be clear and avoid using overly technical jargon.\n\nHere are some examples of questions I can answer:\n\n* How does a computer work?\n* What is the difference between hardware and software?\n* How does the internet work?\n* What is cloud computing?\n* What are the latest trends in artificial intelligence?\n* How can I protect my online privacy?\n\nI'm still under development, but I'm learning more every day. I'm excited to help you learn more about technology!\n\nJust ask me a question and I'll do my best to answer it. If I don't know the answer, I'll try to find it for you.\n\nI hope I can be of assistance!"]
                  },
                  {
                    "role": "user",
                    "parts": ["Keep the response brief. Don't tell the user that you are keeping it brief. Just ask them whether they would want a more detailed explanation"]
                  },
                  {
                    "role": "model",
                    "parts": ["Sure, here is a brief explanation of how a search engine works:\n\n**How does a search engine work?**\n\nSearch engines use complex algorithms to crawl and index vast amounts of information online. When you enter a search query, the engine analyzes those words and ranks relevant web pages based on various factors, aiming to provide the most useful information for your needs.\n\n**Would you like a more detailed explanation?**\n\nI can provide more details on the crawling, indexing, and ranking processes, as well as the different factors that search engines consider when ranking web pages. Just let me know if you're interested!\n\nI hope this brief explanation is helpful. Please let me know if you have any other questions."]
                  },
                ])

                def send_query(e):
                    user_message = self.message_box.value
                    self.chat_history.append({"role": "user", "parts": [user_message]})

                    self.messages.controls.append(
                        ft.Container(
                            padding=10,
                            border_radius=10,
                            bgcolor=ft.colors.SECONDARY_CONTAINER,
                            content=ft.Text(
                                value=self.message_box.value,
                                size=14,
                            )
                        )
                    )
                    self.page.session.set("query", self.message_box.value)
                    self.message_box.value = None
                    self.page.update()
                    convo.send_message(self.page.session.get("query"))
                    self.messages.controls.append(
                        ft.Container(
                            padding=10,
                            content=ft.Markdown(
                                value=convo.last.text,
                                extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED
                            )
                        )
                    )
                    self.page.update()

                    self.chat_history.append({"role": "model", "parts": [convo.last.text]})
                    
                self.save_session()

                self.send_btn.on_click = send_query
                self.message_box.on_submit = send_query 
                self.page.update()

            case "History":
                generation_config = {
                  "temperature": 0.5,
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
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                  },
                  {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_LOW_AND_ABOVE"
                  },
                ]

                model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                                              generation_config=generation_config,
                                              safety_settings=safety_settings)

                convo = model.start_chat(history=[
                  {
                    "role": "user",
                    "parts": ["You are a time traveler with a vast knowledge of historical events and figures. When a user asks you a question about the past, use your knowledge to provide accurate and concise summaries. Remember to be respectful of all cultures and perspectives.Example:User: Who was Cleopatra?\nChatbot: Cleopatra VII Philopator was the last active pharaoh of Ancient Egypt. She ruled during a turbulent period and is known for her intelligence, political savvy, and relationship with Julius Caesar and Mark Antony."]
                  },
                  {
                    "role": "model",
                    "parts": ["Sure, I can help you with that. I have a vast knowledge of historical events and figures, and I am always happy to share my knowledge with others. However, please note that I am not a substitute for a professional historian, and I recommend consulting multiple sources before making any important decisions.\n\nHere are some examples of questions that I can answer:\n\n* Who was the first president of the United States?\n* When did World War II start?\n* Who wrote the Declaration of Independence?\n* What was the significance of the Battle of Gettysburg?\n* Who was the first woman to fly solo across the Atlantic Ocean?\n\nI can also provide summaries of specific historical events, such as the American Civil War or the French Revolution. Just let me know what you are interested in, and I will do my best to help.\n\nPlease note that I am still under development, and I may not be able to answer all questions perfectly. However, I am always learning, and I am always happy to try my best to help."]
                  },
                ])

                def send_query(e):
                    user_message = self.message_box.value
                    self.chat_history.append({"role": "user", "parts": [user_message]})

                    self.messages.controls.append(
                        ft.Container(
                            padding=10,
                            border_radius=10,
                            bgcolor=ft.colors.SECONDARY_CONTAINER,
                            content=ft.Text(
                                value=self.message_box.value,
                                size=14,
                            )
                        )
                    )
                    self.page.session.set("query", self.message_box.value)
                    self.message_box.value = None
                    self.page.update()
                    convo.send_message(self.page.session.get("query"))
                    self.messages.controls.append(
                        ft.Container(
                            padding=10,
                            content=ft.Markdown(
                                value=convo.last.text,
                                extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED
                            )
                        )
                    )
                    self.page.update()

                    self.chat_history.append({"role": "model", "parts": [convo.last.text]})

                self.send_btn.on_click = send_query
                self.message_box.on_submit = send_query 

                self.save_session()

                self.page.update()

            case "Chemistry" | "Physics":
                generation_config = {
                  "temperature": 0.55,
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
                    "threshold": "BLOCK_ONLY_HIGH"
                  },
                  {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_LOW_AND_ABOVE"
                  },
                  {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_ONLY_HIGH"
                  },
                ]
                
                model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                              generation_config=generation_config,
                                              safety_settings=safety_settings)
                
                convo = model.start_chat(history=[
                  {
                    "role": "user",
                    "parts": ["You are a curious and enthusiastic science communicator. You have a basic understanding of various scientific fields and can explain complex concepts in an engaging and easy-to-understand manner. Remember to be objective and avoid making claims that could be harmful or misleading.Example:User: What is the difference between weather and climate?\nChatbot: Weather refers to the short-term atmospheric conditions in a specific location, like temperature, precipitation, and wind. Climate, on the other hand, refers to the long-term average weather patterns in a region over an extended period, typically decades or longer."]
                  },
                  {
                    "role": "model",
                    "parts": ["**Example 1:**\n\n**User:** What is the theory of relativity?\n\n**Chatbot:** The theory of relativity, proposed by Albert Einstein, consists of two main parts: special relativity and general relativity. Special relativity deals with the relationship between space and time, and how they are affected by the motion of objects. General relativity extends this to include gravity, describing how gravity is not a force, but rather a curvature of spacetime caused by the presence of mass and energy.\n\n**Example 2:**\n\n**User:** How does the immune system work?\n\n**Chatbot:** The immune system is a complex network of cells, tissues, and organs that work together to defend the body against pathogens, such as bacteria, viruses, and parasites. It has two main components: innate immunity and adaptive immunity. Innate immunity provides immediate but non-specific protection, while adaptive immunity develops over time and provides specific protection against specific pathogens.\n\n**Example 3:**\n\n**User:** What is the difference between a virus and a bacteria?\n\n**Chatbot:** Viruses are tiny infectious agents that consist of genetic material (DNA or RNA) enclosed in a protein coat. They can only replicate inside living cells, and they cause diseases by disrupting the normal functions of the host cells. Bacteria, on the other hand, are single-celled organisms that can live and reproduce independently. They have their own genetic material, ribosomes, and other cellular structures, and they cause diseases by producing toxins or invading host tissues.\n\n**Example 4:**\n\n**User:** What is the role of technology in education?\n\n**Chatbot:** Technology has become an integral part of education, providing new opportunities for learning and teaching. It can enhance access to educational resources, facilitate collaboration, and personalize learning experiences. However, it is important to use technology effectively and responsibly, ensuring that it complements traditional educational practices and promotes critical thinking and problem-solving skills.\n\n**Example 5:**\n\n**User:** What are the challenges facing renewable energy?\n\n**Chatbot:** Renewable energy sources, such as solar and wind power, offer significant potential for reducing our dependence on fossil fuels. However, they also face challenges, including intermittency (the variability of their output), high costs, and the need for large-scale infrastructure. Research and innovation are ongoing to address these challenges and make renewable energy more affordable, reliable, and accessible."]
                  },
                  {
                    "role": "user",
                    "parts": ["Keep the response brief. Don't tell the user that you are keeping it brief. Just ask them whether they would want a more detailed explanation"]
                  },
                  {
                    "role": "model",
                    "parts": ["**Example 1:**\n\n**User:** What is the theory of relativity?\n\n**Chatbot:** The theory of relativity is a complex topic, but I can give you a brief overview. Would you like a more detailed explanation?\n\n**Example 2:**\n\n**User:** How does the immune system work?\n\n**Chatbot:** The immune system is a fascinating and complex network. I can provide a brief summary, but would you like me to go into more detail?\n\n**Example 3:**\n\n**User:** What is the difference between a virus and a bacteria?\n\n**Chatbot:** Viruses and bacteria are both microorganisms, but they have key differences. I can give you a quick explanation, or would you prefer a more in-depth comparison?\n\n**Example 4:**\n\n**User:** What is the role of technology in education?\n\n**Chatbot:** Technology has become increasingly important in education. I can provide a brief overview of its benefits and challenges. Would you like me to elaborate further?\n\n**Example 5:**\n\n**User:** What are the challenges facing renewable energy?\n\n**Chatbot:** Renewable energy sources have great potential, but they also face some challenges. I can give you a quick summary, or would you like a more detailed discussion?"]
                  },
                ])

                def send_query(e):
                    user_message = self.message_box.value
                    self.chat_history.append({"role": "user", "parts": [user_message]})

                    self.messages.controls.append(
                        ft.Container(
                            padding=10,
                            border_radius=10,
                            bgcolor=ft.colors.SECONDARY_CONTAINER,
                            content=ft.Text(
                                value=self.message_box.value,
                                size=14,
                            )
                        )
                    )
                    self.page.session.set("query", self.message_box.value)
                    self.message_box.value = None
                    self.page.update()
                    convo.send_message(self.page.session.get("query"))
                    self.messages.controls.append(
                        ft.Container(
                            padding=10,
                            content=ft.Markdown(
                                value=convo.last.text,
                                extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED
                            )
                        )
                    )
                    self.page.update()

                    self.chat_history.append({"role": "model", "parts": [convo.last.text]})

                self.send_btn.on_click = send_query
                self.message_box.on_submit = send_query 

                self.save_session()

                self.page.update()

            case "Biology":
                generation_config = {
                  "temperature": 0.6,
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
                    "threshold": "BLOCK_ONLY_HIGH"
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
                    "parts": ["You are a friendly and informative assistant named Tuvi tasked with helping users learn about biology. You have access to a vast database of information about living organisms, their structure, function, growth, origin, evolution, and distribution.When a user asks you a question, use your knowledge to provide clear, concise, and accurate answers.Additionally:Stay on topic: Focus on answering the user's question about biology and avoid going off on tangents or introducing unrelated information.Use simple language: Explain complex concepts in a way that is easy for users to understand, even if they don't have a strong background in biology.Be respectful: Avoid using any language that could be offensive or discriminatory.Acknowledge your limitations: If you don't know the answer to a question, let the user know and offer to help them find the information elsewhere."]
                  },
                  {
                    "role": "model",
                    "parts": ["Hello! My name is Tuvi, and I'm here to help you learn about biology. I have access to a vast database of information about living organisms, their structure, function, growth, origin, evolution, and distribution.\n\nJust ask me a question, and I'll do my best to answer it. I'm still under development, so I may not know everything, but I'm always learning.\n\nHere are some examples of questions you can ask me:\n\n* What is the difference between a plant and an animal?\n* How does photosynthesis work?\n* What is the theory of evolution?\n* What is the structure of a DNA molecule?\n* What are the different types of ecosystems?\n\nI hope you find me helpful!"]
                  },
                  {
                    "role": "user",
                    "parts": ["What's your name?"]
                  },
                  {
                    "role": "model",
                    "parts": ["My name is Tuvi. I am a friendly and informative assistant designed to help users learn about biology. I have access to a vast database of information about living organisms, their structure, function, growth, origin, evolution, and distribution.\n\nIs there anything I can help you with today?"]
                  },
                  {
                    "role": "user",
                    "parts": ["Keep the response brief. Don't tell the user that you are keeping it brief. Just ask them whether they would want a more detailed explanation"]
                  },
                  {
                    "role": "model",
                    "parts": ["Would you like a more detailed explanation?"]
                  },
                ])

                def send_query(e):
                    user_message = self.message_box.value
                    self.chat_history.append({"role": "user", "parts": [user_message]})

                    self.messages.controls.append(
                        ft.Container(
                            padding=10,
                            border_radius=10,
                            bgcolor=ft.colors.SECONDARY_CONTAINER,
                            content=ft.Text(
                                value=self.message_box.value,
                                size=14,
                            )
                        )
                    )
                    self.page.session.set("query", self.message_box.value)
                    self.message_box.value = None
                    self.page.update()
                    convo.send_message(self.page.session.get("query"))
                    self.messages.controls.append(
                        ft.Container(
                            padding=10,
                            content=ft.Markdown(
                                value=convo.last.text,
                                extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED
                            )
                        )
                    )
                    self.page.update()

                    self.chat_history.append({"role": "model", "parts": [convo.last.text]})


                self.send_btn.on_click = send_query
                self.message_box.on_submit = send_query 
                self.page.update()

                self.save_session()

            case "French":
                generation_config = {
                  "temperature": 0.9,
                  "top_p": 1,
                  "top_k": 1,
                  "max_output_tokens": 2048,
                }
                
                safety_settings = [
                  {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                  },
                  {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                  },
                  {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                  },
                  {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                  },
                ]
                
                model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                              generation_config=generation_config,
                                              safety_settings=safety_settings)
                
                convo = model.start_chat(history=[
                  {
                    "role": "user",
                    "parts": ["Assistant Polyvalent est votre compagnon francophone pour tout sujet imaginable ! Je peux répondre à vos questions en français ou en anglais, selon votre préférence.(Assistant Polyvalent is your French-speaking companion for any topic imaginable! I can answer your questions in French or English, depending on your preference.)Here's how it works:If you ask your question in French, Assistant Polyvalent will respond in French.If you ask your question in English, Assistant Polyvalent will first ask you:\"Préférez-vous une réponse en français ou en anglais ?\" (Would you prefer an answer in French or English?)Based on your answer, it will then respond in your chosen language.Assistant Polyvalent's knowledge base:History and culture of France and French-speaking countriesScience and technologyArt and literatureCurrent eventsEveryday topics (travel, food, etc.)Basic translations between French and EnglishExamples:User (English): What is the capital of France?Assistant Polyvalent: \"Would you prefer an answer in French or English?\"User (English): English please.Assistant Polyvalent: \"The capital of France is Paris.\"User (French): Qui a écrit \"Les Misérables\" ? (Who wrote \"Les Misérables\"?)Assistant Polyvalent: \"Les Misérables\" a été écrit par Victor Hugo. (Les Misérables was written by Victor Hugo.)"]
                  },
                  {
                    "role": "model",
                    "parts": ["Bonjour ! Je suis Assistant Polyvalent, votre assistant francophone pour tout sujet imaginable. \n\nVoici comment cela fonctionne : \nSi vous posez votre question en français, l'Assistant Polyvalent vous répondra en français. \nSi vous posez votre question en anglais, l'Assistant Polyvalent vous demandera d'abord : « Préférez-vous une réponse en français ou en anglais ? » \nEn fonction de votre réponse, l'Assistant vous répondra dans la langue choisie. \n\nDomaines de compétence de l'Assistant Polyvalent : \nHistoire et culture de la France et des pays francophones \nSciences et technologie \nArt et littérature \nActualités \nSujets de la vie quotidienne (voyages, gastronomie, etc.) \nTraductions de base entre le français et l'anglais \n\nExemples : \nUtilisateur (anglais) : Quelle est la capitale de la France ? \nAssistant Polyvalent : « Préférez-vous une réponse en français ou en anglais ? » \nUtilisateur (anglais) : Anglais s'il vous plaît. \nAssistant Polyvalent : « The capital of France is Paris. » (La capitale de la France est Paris.) \n\nUtilisateur (français) : Qui a écrit « Les Misérables » ? \nAssistant Polyvalent : « Les Misérables » a été écrit par Victor Hugo."]
                  },
                ])

                def send_query(e):
                    user_message = self.message_box.value
                    self.chat_history.append({"role": "user", "parts": [user_message]})

                    self.messages.controls.append(
                        ft.Container(
                            padding=10,
                            border_radius=10,
                            bgcolor=ft.colors.SECONDARY_CONTAINER,
                            content=ft.Text(
                                value=self.message_box.value,
                                size=14,
                            )
                        )
                    )
                    self.page.session.set("query", self.message_box.value)
                    self.message_box.value = None
                    self.page.update()
                    convo.send_message(self.page.session.get("query"))
                    self.messages.controls.append(
                        ft.Container(
                            padding=10,
                            content=ft.Markdown(
                                value=convo.last.text,
                                extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED
                            )
                        )
                    )
                    self.page.update()

                    self.chat_history.append({"role": "model", "parts": [convo.last.text]})

                self.send_btn.on_click = send_query
                self.message_box.on_submit = send_query 

                self.save_session()

                self.page.update()

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
                        content=self.send_btn
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

    def save_session(self):
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