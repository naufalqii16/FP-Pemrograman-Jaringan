from datetime import datetime
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
            update_chat_room(profile["username"])

            with open('../db/private_message_lol.json', 'r') as f:
                private_messages = json.load(f)

            chat = []
            for message in private_messages["data"]:
                if (message["sender"] == current_user and message["receiver"] == current_chat_room) or (message["sender"] == current_chat_room and message["receiver"] == current_user):
                    chat.append(message)

            # Display Chat
            if chat:
                for message in chat:    
                    if message["sender"] == current_user:
                        chat_room_messages.append(
                            ft.Container(
                                ft.Text(message["message"], style=ft.TextStyle(color=ft.colors.WHITE)),
                                bgcolor=ft.colors.BLUE,
                                padding=10,
                                border_radius=10,
                                margin=5,
                                alignment=ft.alignment.center_right,
                                width="fit"
                            )
                        )
                    else:
                        chat_room_messages.append(
                            ft.Container(
                                ft.Text(message["message"], style=ft.TextStyle(color=ft.colors.BLUE)),
                                bgcolor=ft.colors.WHITE,
                                padding=10,
                                border_radius=10,
                                margin=5,
                                alignment=ft.alignment.center_left,
                                width="fit"
                            )
                        )
                    page.update()
    
    def update_chat_room(room_name):
        chat_room.content = ft.Column([
            ft.Text(f"Chat Room: {room_name}", style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)),
            ft.Container(
                content=ft.ListView(
                    chat_room_messages,
                    # expand=True
                ),
                expand=True,
            ),
            ft.Row(
                [
                    message_input,
                    send_button
                ],
                alignment=ft.MainAxisAlignment.START,
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

        # Load groups
        with open('../db/group_user.json', 'r') as f:
            group_users = json.load(f)

        user_groups = [group["groupname"] for group in group_users["data"] if group["username"] == current_user]

        for group_name in user_groups:
            message_list.append(
                ft.ListTile(
                    leading=ft.CircleAvatar(
                        content=ft.Text(
                            group_name[0],
                            style=ft.TextStyle(color=ft.colors.WHITE, size=20)
                        ),
                        bgcolor=ft.colors.PURPLE,
                        radius=20
                    ),
                    title=ft.Text(group_name, weight=ft.FontWeight.BOLD),
                    height=70,
                    on_click=lambda e, group_name=group_name: open_chat({"username": group_name})  # Make each group clickable
                )
            )

        def show_create_group_dialog(e):
            group_name_field = ft.TextField(label="Group Name", hint_text="Enter group name")
            error_message = ft.Text(value="", color=ft.colors.RED, max_lines=2)

            def create_group(e):
                group_name = group_name_field.value.strip()

                # Read existing groups from group.json
                try:
                    with open('../db/group.json', 'r') as f:
                        group_data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    group_data = {"data": []}

                # Check for empty group name
                if not group_name:
                    error_message.value = "Group name cannot be empty."
                    page.update()
                    return

                # Check for duplicate group name
                for group in group_data["data"]:
                    if group["group_name"].lower() == group_name.lower():
                        error_message.value = "Group name already exists. Please choose a different name."
                        page.update()
                        return

                # Add new group to JSON data
                group_data["data"].append({"group_name": group_name})

                # Write back to the JSON file
                with open('../db/group.json', 'w') as f:
                    json.dump(group_data, f, indent=4)

                # Add new group_user data
                group_user_entry = {
                    "username": current_user,
                    "groupname": group_name,
                    "realm_id": "c8adceb6-b41e-47e2-818a-a38c3451c9a0"
                }

                # Read existing group_user data from group_user.json
                try:
                    with open('../db/group_user.json', 'r') as f:
                        group_user_data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    group_user_data = {"data": []}

                # Add new entry to group_user data
                group_user_data["data"].append(group_user_entry)

                # Write back to the JSON file
                with open('../db/group_user.json', 'w') as f:
                    json.dump(group_user_data, f, indent=4)

                dialog.open = False  # Close the dialog
                page.update()

            def cancel_create_group(e):
                dialog.open = False
                page.update()

            dialog = ft.AlertDialog(
                title=ft.Text("Create New Group"),
                content=ft.Container(
                    content=ft.Column([group_name_field, error_message], spacing=10),
                    padding=ft.padding.all(10),
                    width=300,
                    height=150
                ),
                actions=[
                    ft.ElevatedButton(text="Create", on_click=create_group),
                    ft.TextButton(text="Cancel", on_click=cancel_create_group)
                ]
            )
            page.dialog = dialog
            dialog.open = True
            page.update()

        create_group_button = ft.ElevatedButton(
            text="Create New Group",
            icon=ft.icons.GROUP_ADD,
            on_click=show_create_group_dialog
        )
        
        def send_message(e):
            message = message_input.value
            if message:
                chat_room_messages.append(ft.Text(message))
                message_input.value = ""
                page.update()

                # Read existing messages or initialize if file doesn't exist
                try:
                    with open('../db/private_message.json', 'r') as f:
                        messages_data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    messages_data = {"data": []}

                # Append the new message
                new_message = {
                    "sender": current_user,
                    "sender_realm": "c8adceb6-b41e-47e2-818a-a38c3451c9a0",
                    "receiver": current_chat_room,
                    "receiver_realm": "c8adceb6-b41e-47e2-818a-a38c3451c9a0",
                    "message": message,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                }
                messages_data["data"].append(new_message)

                # Write back to the JSON file
                with open('../db/private_message_lol.json', 'w') as f:
                    json.dump(messages_data, f, indent=4)

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