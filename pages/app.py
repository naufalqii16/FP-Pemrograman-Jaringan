from datetime import datetime
import flet as ft
import json
import os
from chatcli import ChatClient  # Import ChatClient

# Global variable to store logged-in user
current_user = None
current_chat_room = None  # To store the current chat room
current_group_chat = None  # To store the current group chat
current_chat_file = None
chat_temp = []
token_id = None

def main(page: ft.Page):
    chatService = ChatClient()  # Initialize ChatClient

    global chat_room, message_input, send_button, chat_room_messages

    page.title = "Login Screen"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    chat_room_messages = []  # Initialize chat room messages list
    
    def open_chat_option(profile):
        global current_chat_room

        def close_dialog(e):
            dialog.open = False
            page.update()
        
        def open_chat_and_close_dialog(e):
            open_chat(profile)
            close_dialog(e)

        def open_chat_file_and_close_dialog(e):
            open_chat_file(profile)
            close_dialog(e)
        
        dialog = ft.AlertDialog(
            title=ft.Text("Open Chat Option"),
            content=ft.Column([
                ft.Text(f"Profile: {profile}"),
                ft.TextButton(text="Open Chat", on_click=lambda e: open_chat_and_close_dialog(profile)),
                ft.TextButton(text="Open Chat File", on_click=lambda e: open_chat_file_and_close_dialog(profile)),
            ]),
            actions=[ft.TextButton(text="Cancel", on_click=close_dialog)]
        )
        page.dialog = dialog
        dialog.open = True
        page.update()
        
    def open_chat(profile):
        global current_chat_room
        global current_group_chat  # Use global to modify global variable
        global current_chat_file
        global chat_temp

        if current_chat_room != profile:
            current_chat_room = profile
            current_group_chat = None  # Reset group chat
            current_chat_file = None
            chat_temp = []  # Reset chat_temp
            chat_room_messages.clear()  # Clear previous messages

            page.snack_bar = ft.SnackBar(
                ft.Text(f"Opening chat with {profile}"),
                bgcolor=ft.colors.GREEN,
            )
            page.snack_bar.open = True
            page.update()
            update_chat_room(profile)

            # Fetch private messages using ChatClient
            chat = chatService.inbox(current_chat_room)  # Adjust this according to your API
            # for message in chat["messages"]:
            #     if (message["sender"] == current_user and message["receiver"] == current_chat_room) or (message["sender"] == current_chat_room and message["receiver"] == current_user):
            #         chat_temp.append(message)

            print("CHAT TEMP:", chat_temp)
            print("chat['messages']:", chat["messages"])
            print("current user:", current_user)

            # Display Chat
            if chat:
                for message in chat['messages']:  # Iterate over chat_temp instead of chat['messages']
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
                    elif message["sender"] == current_chat_room:
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
    
    def open_chat_file(profile):
        global current_chat_room
        global current_group_chat  # Use global to modify global variable
        global current_chat_file

        file_name = []
        directory = 'file_receive'  # Specify the directory path

        file_name = []
        for filename in os.listdir(directory):
            file_name.append(filename)

        if current_chat_file != profile:
            current_chat_file = profile
            current_group_chat = None  # Reset group chat
            current_chat_room = None
            chat_room_messages.clear()  # Clear previous messages

            page.snack_bar = ft.SnackBar(
                ft.Text(f"Opening chat with {profile}"),
                bgcolor=ft.colors.GREEN,
            )
            page.snack_bar.open = True
            page.update()
            update_chat_room(profile)

            # Fetch file messages using ChatClient
            chat = chatService.receivefile(current_chat_file)  # Adjust this according to your API

            # print("CHAT TEMP:", chat)
            print("CUREEEENT:", current_chat_file)

            # Check if all senders and receivers have files in the directory
            if chat:
                for message in chat['content']:
                    sender = message['sender']
                    receiver = message['receiver']
                    if sender not in file_name or receiver not in file_name:
                        # Handle missing files here
                        pass

            # Display Chat
            if chat:
                for message in chat['content']:
                    if message["sender"] == current_user:
                        chat_room_messages.append(
                            ft.Container(
                                ft.Image(
                                    # src=f'D:\\Vscode\\Semester 6\\Progjar\\fp-pemrograman-jaringan\\file_receive\\{message['sender']}\\{message["file_name"]}',
                                    # src=f'./file_receive/{message["sender"]}/{message["file_name"]}',
                                    width=200,
                                    height=200,
                                ),
                                alignment=ft.alignment.center_right,
                            )
                        )
                    else:
                        chat_room_messages.append(
                            ft.Container(
                                ft.Image(
                                    # src=f'D:\\Vscode\\Semester 6\\Progjar\\fp-pemrograman-jaringan\\file_receive\\{message['receiver']}\\{message["file_name"]}',
                                    # src=f'./file_receive/{message["sender"]}/{message["file_name"]}',
                                    width=200,
                                    height=200,
                                ),
                                alignment=ft.alignment.center_left,
                            )
                        )
                    page.update()
    
    def open_group_chat(group_name):
        global current_group_chat
        global current_chat_room  # Use global to modify global variable
        global current_chat_file

        if current_group_chat != group_name:
            current_group_chat = group_name
            current_chat_room = None  # Reset private chat
            current_chat_file = None
            chat_room_messages.clear()  # Clear previous messages

            page.snack_bar = ft.SnackBar(
                ft.Text(f"Opening chat in group {group_name}"),
                bgcolor=ft.colors.GREEN,
            )
            page.snack_bar.open = True
            page.update()
            update_chat_room(group_name)

            chat_group = chatService.inbox_group(current_group_chat)  # Adjust this according to your API

            # Display Chat
            if chat_group:
                for message in chat_group['messages']:  # Iterate over chat_temp instead of chat['messages']
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
                    elif message["sender"] != current_user:
                        chat_room_messages.append(
                            ft.Container(
                                ft.Column([
                                    ft.Text(message["sender"], style=ft.TextStyle(color=ft.colors.RED)),
                                    ft.Text(message["message"], style=ft.TextStyle(color=ft.colors.BLUE)),
                                ]),
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

        # Fetch users from the server using ChatClient
        data = chatService.getallusers()  # Adjust this according to your API

        if data["status"] == "OK":
            users = data["users"]
        else:
            users = []  # Replace this with a call to fetch users from the server
        
        # message_list = chatService.inbox()  # Adjust this according to your API
        message_list = []

        for msg in users:
            if msg != current_user:  # Exclude current user's profile
                message_list.append(
                    ft.ListTile(
                        leading=ft.CircleAvatar(
                            content=ft.Text(
                                msg[0],
                                style=ft.TextStyle(color=ft.colors.WHITE, size=20)
                            ),
                            bgcolor=ft.colors.PURPLE,
                            radius=20
                        ),
                        title=ft.Text(msg, weight=ft.FontWeight.BOLD),
                        height=70,
                        on_click=lambda e, msg=msg: open_chat_option(msg)  # Make each profile clickable
                    )
                )

        # Fetch groups from the server using ChatClient
        user_groups = chatService.get_groups()  # Adjust this according to your API 
        # user_groups = user_groups['groups']
        print("USER GROUPS:", user_groups)
        if(user_groups['status'] == 'OK'):
            group_temp = user_groups['groups']  
            for group_name in group_temp:
                message_list.append(
                    ft.ListTile(
                        leading=ft.CircleAvatar(
                            content=ft.Text(
                                # print(group_name['groupname']),
                                group_name['groupname'][0:2],
                                style=ft.TextStyle(color=ft.colors.WHITE, size=20)
                            ),
                            bgcolor=ft.colors.PURPLE,
                            radius=20
                        ),
                        title=ft.Text(group_name['groupname'], weight=ft.FontWeight.BOLD),
                        height=70,
                        on_click=lambda e, group_name=group_name['groupname']: open_group_chat(group_name)  # Make each group clickable
                    )
                )
        else:
            message_list.append(
                ft.ListTile(
                    title=ft.Text("No Group", weight=ft.FontWeight.BOLD),
                    height=70,
                )
            )
            

        def show_create_group_dialog(e):
            group_name_field = ft.TextField(label="Group Name", hint_text="Enter group name")
            error_message = ft.Text(value="", color=ft.colors.RED, max_lines=2)

            def create_group(e):
                group_name = group_name_field.value.strip()
                result = chatService.create_group(group_name)  # Call ChatClient to create group

                if "successfully created" in result:
                    dialog.open = False  # Close the dialog
                    page.update()
                else:
                    error_message.value = result  # Show error message
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

        def show_join_group_dialog(e):
            group_name_field = ft.TextField(label="Group Name", hint_text="Enter group name")
            error_message = ft.Text(value="", color=ft.colors.RED, max_lines=2)

            def join_group(e):
                group_name = group_name_field.value.strip()
                result = chatService.join_group(group_name)  # Call ChatClient to join group

                if "successfully joined" in result:
                    dialog.open = False  # Close the dialog
                    page.update()
                else:
                    error_message.value = result  # Show error message
                    page.update()

            def cancel_join_group(e):
                dialog.open = False
                page.update()

            dialog = ft.AlertDialog(
                title=ft.Text("Join Group"),
                content=ft.Container(
                    content=ft.Column([group_name_field, error_message], spacing=10),
                    padding=ft.padding.all(10),
                    width=300,
                    height=150
                ),
                actions=[
                    ft.ElevatedButton(text="Join", on_click=join_group),
                    ft.TextButton(text="Cancel", on_click=cancel_join_group)
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
        
        join_group_button = ft.ElevatedButton(
            text="Join Group",
            icon=ft.icons.GROUP,
            on_click=show_join_group_dialog
        )

        def send_message(e):
            message = message_input.value
            if message:
                chat_room_messages.append(ft.Text(message))
                message_input.value = ""
                page.update()

                if current_chat_room:
                    if message.endswith('.jpeg') or message.endswith('.jpg') or message.endswith('.png'):
                        result = chatService.sendfile(current_chat_room, message)  # Call ChatClient to send file
                    else:
                        result = chatService.sendmessage(current_chat_room, message)  # Call ChatClient to send message
                elif current_group_chat:
                    result = chatService.sendmessage_group(current_group_chat, message)  # Call ChatClient to send group message

                # Handle response from ChatClient
                if "Error" in result:
                    page.snack_bar = ft.SnackBar(
                        ft.Text(result, color=ft.colors.WHITE),
                        bgcolor=ft.colors.RED,
                    )
                    page.snack_bar.open = True
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
                            ft.Row([join_group_button]),
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
        login_page_content()

    def back_to_login(e):
        global current_user  # Use global to modify global variable
        global current_chat_room
        global current_group_chat
        current_group_chat = None
        current_user = None
        current_chat_room = None
        login_page_content()

    def login_page_content():
        page.clean()
        page.title = "Login Screen"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER

        def on_login(e):
            global current_user  # Use global to modify global variable
            global token_id
            username = username_field.value
            password = password_field.value

            result = chatService.login(username, password)  # Call ChatClient to login

            if result['status'] == 'OK':
                current_user = username
                token_id = result['token_id']
                main_page_content()  # Switch to main page content
            else:
                page.snack_bar = ft.SnackBar(
                    ft.Text(result, color=ft.colors.WHITE),
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

            result = chatService.register(username, password)  # Call ChatClient to register

            if result['status'] == 'OK':
                page.snack_bar = ft.SnackBar(
                    ft.Text(result, color=ft.colors.WHITE),
                    bgcolor=ft.colors.GREEN,
                )
                page.snack_bar.open = True
                page.update()
                login_page_content()  # Switch back to login page after successful registration
            else:
                page.snack_bar = ft.SnackBar(
                    ft.Text(result, color=ft.colors.WHITE),
                    bgcolor=ft.colors.RED,
                )
                page.snack_bar.open = True
                page.update()

        username_register = ft.TextField(label="Username", hint_text="username", width=300)
        password_register = ft.TextField(label="Password", password=True, width=300)

        register_button = ft.ElevatedButton(
            text="Sign Up",
            on_click=on_register,
            width=300,
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE,
        )

        back_to_login_button = ft.TextButton(
            text="Back to Login",
            on_click=back_to_login,
        )

        page.add(
            ft.Column(
                [
                    ft.Text("Create an account", size=24, weight=ft.FontWeight.BOLD),
                    username_register,
                    password_register,
                    register_button,
                    ft.Row(
                        [
                            back_to_login_button,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )
        )

    def register_form():
        register_page_content()

    login_page_content()

ft.app(target=main)
