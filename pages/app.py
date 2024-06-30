import flet as ft
import json

# Global variable to store logged-in user
current_user = None
current_chat_room = None  # To store the current chat room

def main(page: ft.Page):
    global chat_room, message_input, send_button, chat_room_messages

    page.title = "Login Screen"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    chat_room_messages = []  # Initialize chat room messages list

    def open_chat(profile):
        global current_chat_room  # Use global to modify global variable

        if current_chat_room != profile["username"]:
            current_chat_room = profile["username"]
            chat_room_messages.clear()  # Clear previous messages

            page.snack_bar = ft.SnackBar(
                ft.Text(f"Opening chat with {profile['username']}"),
                bgcolor=ft.colors.GREEN,
            )
            page.snack_bar.open = True
            page.update()
            update_chat_room(profile["username"])  # Update chat room with new room name

    def update_chat_room(room_name):
        chat_room.content = ft.Column([
            ft.Text(f"Chat Room: {room_name}", style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)),
            ft.Column(chat_room_messages, expand=True),
            ft.Row(
                [
                    message_input,
                    send_button
                ],
                alignment=ft.MainAxisAlignment.END,
                spacing=10
            )
        ])
        page.update()

    def main_page_content():
        global chat_room, message_input, send_button  # Define these variables globally

        page.clean()
        page.title = "ConvoHub"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.padding = 20

        with open('../db/user.json', 'r') as f:
            data = json.load(f)

        messages = data["data"]

        message_list = []
        for msg in messages:
            if msg["username"] != current_user:  # Exclude current user's profile
                message_list.append(
                    ft.ListTile(
                        leading=ft.CircleAvatar(
                            content=ft.Text(
                                msg["username"][0],
                                style=ft.TextStyle(color=ft.colors.WHITE, size=20)
                            ),
                            bgcolor=ft.colors.PURPLE,
                            radius=20
                        ),
                        title=ft.Text(msg["username"], weight=ft.FontWeight.BOLD),
                        height=70,
                        on_click=lambda e, msg=msg: open_chat(msg)  # Make each profile clickable
                    )
                )

        create_group_button = ft.ElevatedButton(
            text="Create New Group",
            icon=ft.icons.GROUP_ADD,
            on_click=lambda e: print("Create New Group Clicked")
        )

        def send_message(e):
            message = message_input.value
            if message:
                chat_room_messages.append(ft.Text(message))
                message_input.value = ""
                page.update()

        message_input = ft.TextField(hint_text="Type a message", expand=True, border_color=ft.colors.WHITE)
        send_button = ft.ElevatedButton(text="Send", on_click=send_message)

        logout_button = ft.ElevatedButton(
            text="Logout",
            on_click=logout,
            bgcolor=ft.colors.RED,
            color=ft.colors.WHITE,
            width=100,
        )

        chat_room = ft.Container(
            expand=True
        )

        page.add(
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Row([ft.Text("ConvoHub.", style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD))]),
                            ft.Row([create_group_button]),
                            ft.Column(message_list, spacing=10, width=350),
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.START
                    ),
                    ft.Container(
                        width=1,
                        bgcolor=ft.colors.GREY,
                        height="100%",  # Set height to fill available space
                    ),
                    ft.Column(
                        [
                            ft.Row([logout_button], alignment=ft.MainAxisAlignment.END),
                            chat_room
                        ],
                        expand=True
                    )
                ],
                expand=True
            )
        )

    def logout(e):
        global current_user  # Use global to modify global variable
        current_user = None
        login_page_content()

    def back_to_login(e):
        login_page_content()

    def login_page_content():
        page.clean()
        page.title = "Login Screen"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER

        def on_login(e):
            global current_user  # Use global to modify global variable
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
            for user in data["data"]:
                if user["username"] == username and user["password"] == password:
                    print("Login Successful")
                    current_user = username
                    main_page_content()  # Switch to main page content
                    return

            print("Username or Password Incorrect")
            page.snack_bar = ft.SnackBar(
                ft.Text("Username or Password Incorrect", color=ft.colors.WHITE),
                bgcolor=ft.colors.RED,
            )
            page.snack_bar.open = True
            page.update()

        def show_register_form(e):
            register_form()

        username_field = ft.TextField(label="Username", hint_text="username", width=300)
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
            on_click=show_register_form,
        )


        page.add(
            ft.Column(
                [
                    ft.Text("Let's sign you in!", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text("Welcome back, you have been missed :(", size=16),
                    username_field,
                    password_field,
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

    def register_page_content():
        page.clean()
        page.title = "Register"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER

        def on_register(e):
            username = username_register.value
            password = password_register.value

            # Read existing user data or initialize an empty dictionary if the file doesn't exist
            try:
                with open('../db/user.json', 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = {"data": []}

            # Check if username already exists
            for user in data["data"]:
                if user["username"] == username:
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Username already exists. Please choose a different username.", color=ft.colors.WHITE),
                        bgcolor=ft.colors.RED,
                    )
                    page.snack_bar.open = True
                    page.update()
                    return

            # Add new user to JSON data
            data["data"].append({"username": username, "password": password})

            # Write back to the JSON file
            with open('../db/user.json', 'w') as f:
                json.dump(data, f, indent=4)

            page.snack_bar = ft.SnackBar(
                ft.Text("Registration successful. You can now log in.", color=ft.colors.WHITE),
                bgcolor=ft.colors.GREEN,
            )
            page.snack_bar.open = True
            page.update()

            login_page_content()

        username_register = ft.TextField(label="Username", hint_text="Enter your username", width=300)
        password_register = ft.TextField(label="Password", hint_text="Enter your password", password=True, width=300)

        register_button = ft.ElevatedButton(
            text="Register",
            on_click=on_register,
            width=300,
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
        )

        back_to_login_button = ft.TextButton(
            text="Back to Login",
            on_click=back_to_login,
        )

        page.add(
            ft.Column(
                [
                    ft.Text("Create an Account", size=24, weight=ft.FontWeight.BOLD),
                    username_register,
                    password_register,
                    register_button,
                    back_to_login_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )
        )

    def register_form():
        login_page_content()  # Clear login page content
        register_page_content()

    login_page_content()

ft.app(target=main)
