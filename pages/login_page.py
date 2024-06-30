import flet as ft
import json
import os

def loginpage(page: ft.Page):
    page.title = "Login Screen"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def on_login(e):
        username = username_field.value
        password = password_field.value

        # Read the JSON file with user data
        try:
            with open('db/user.json', 'r') as f:
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
            page.snack_bar = ft.SnackBar(
                ft.Text("Login Successful", color=ft.colors.WHITE),
                bgcolor=ft.colors.GREEN,
            )
            
            # Set session or perform any post-login actions here
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

ft.app(target=loginpage)
