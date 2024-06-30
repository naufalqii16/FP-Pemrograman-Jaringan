
import flet as ft

def main(page: ft.Page):
    page.title = "Login Screen"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def on_login(e):
        # Handle the login action
        username = username_field.value
        password = password_field.value
        print(f"username: {username}, Password: {password}")

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

ft.app(target=main)
