import flet as ft
import json

def main(page: ft.Page):
    page.title = "Login Screen"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Define main page content
    def main_page_content():
        page.title = "ConvoHub"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.padding = 20

        search_box = ft.TextField(
            hint_text="Search",
            prefix_icon=ft.icons.SEARCH,
            width=300,
            height=40,
            border_color=ft.colors.BLUE
        )

        messages = [
            {"name": "Ddedida", "message": "Ayo sholat Jumat", "time": "11.43", "new_messages": 1},
            {"name": "Remaja Masjid", "message": "Kapan sholat rek", "time": "10.55", "new_messages": 1},
            {"name": "Intger", "message": "Ayo sholat Isya", "time": "Yesterday", "new_messages": 1}
        ]

        message_list = []
        for msg in messages:
            message_list.append(
                ft.ListTile(
                    leading=ft.CircleAvatar(
                        content=ft.Text(
                            msg["name"][0],
                            style=ft.TextStyle(color=ft.colors.WHITE, size=20)
                        ),
                        bgcolor=ft.colors.PURPLE,
                        radius=20
                    ),
                    title=ft.Text(msg["name"], weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(msg["message"]),
                    trailing=ft.Column(
                        [
                            ft.Text(msg["time"]),
                            ft.Container(
                                content=ft.Text(str(msg["new_messages"]), color=ft.colors.WHITE),
                                bgcolor=ft.colors.BLUE,
                                padding=ft.Padding(left=6, top=2, right=6, bottom=2),
                                border_radius=ft.border_radius.all(12)
                            ) if msg["new_messages"] > 0 else ft.Container()
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    height=70
                )
            )

        new_message_button = ft.FloatingActionButton(
            content=ft.Icon(ft.icons.ADD),
            bgcolor=ft.colors.BLUE,
            on_click=lambda _: print("New message")
        )

        page.add(
            ft.Column(
                [
                    ft.Row([ft.Text("ConvoHub.", style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD))]),
                    ft.Row([search_box], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Column(message_list, spacing=10, width=350),
                    ft.Row([new_message_button], alignment=ft.MainAxisAlignment.END)
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.START
            )
        )

    # Define login page content and logic
    def login_page_content():
        def on_login(e):
            username = username_field.value
            password = password_field.value

            # Read the JSON file with user data
            try:
                with open('../db/user.json', 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                print("User database not found.")
                page.snack_bar = ft.SnackBar(
                    ft.Text("User database not found.", color=ft.colors.WHITE),
                    bgcolor=ft.colors.RED,
                )
                page.snack_bar.open = True
                page.update()
                return

            # Check the provided credentials
            if username in data and data[username] == password:
                print("Login Successful")
                page.clean()  # Clean the page content
                main_page_content()  # Switch to main page content
            else:
                print("Username or Password Incorrect")
                page.snack_bar = ft.SnackBar(
                    ft.Text("Username or Password Incorrect", color=ft.colors.WHITE),
                    bgcolor=ft.colors.RED,
                )
                page.snack_bar.open = True
                page.update()

        username_field = ft.TextField(label="username", hint_text="username.example.com", width=300)
        password_field = ft.TextField(label="Password", password=True, width=300)

        login_button = ft.ElevatedButton(
            text="Log in",
            on_click=on_login,
            width=300,
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE,
        )

        signup_text = ft.TextButton(
            text="Sign Up",
            on_click=lambda e: print("Navigate to Sign Up"),
        )

        forgot_password_text = ft.TextButton(
            text="Forgot Password?",
            on_click=lambda e: print("Navigate to Forgot Password"),
        )

        page.add(
            ft.Column(
                [
                    ft.Text("Let's sign you in!", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text("Welcome back, you have been missed :(", size=16),
                    username_field,
                    password_field,
                    forgot_password_text,
                    login_button,
                    ft.Row(
                        [
                            ft.Text("Don't have an account? "),
                            signup_text,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )
        )

    # Start with the login page
    login_page_content()

ft.app(target=main)
