import flet as ft

def main_page(page: ft.Page):
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
        {"name": "Intger", "message": "Ayo sholat Isya", "time": "Yesterday", "new_messages": 0}
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
                    bgcolor=ft.colors.PURPLE,  # Corrected parameter name
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

ft.app(target=main_page)
