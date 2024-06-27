from flet import *

h = 750
w = 350

class App(UserControl):
    def __init__(self, pg):
        super().__init__()
        self.pg = pg
        self.animation_style = animation.Animation(500, AnimationCurve.DECELERATE)
        self.active_page = 'page1'  # Halaman aktif awal
        self.init_helper()

    def init_helper(self):
        self.side_bar_column = Column(
            spacing=0,
            controls=[
                self.create_sidebar_item("Alice", 'aw2.jpeg', 'page1'),
                self.create_sidebar_item("Bob", 'sabdaps.jpg', 'page2'),
                self.create_sidebar_item("Charlie", 'sabdaps.jpg', 'page3'),
            ]
        )

        self.indicator = Container(
            height=40,
            bgcolor='red',
            offset=transform.Offset(0, 0),
            animate_offset=animation.Animation(500, AnimationCurve.DECELERATE)
        )

        self.page1 = Container(
            alignment=alignment.center,
            offset=transform.Offset(0, 0),
            animate_offset=self.animation_style,
            bgcolor='blue',
            content=Text('PAGE 1', size=50)
        )

        self.page2 = Container(
            alignment=alignment.center,
            offset=transform.Offset(0, 0),
            animate_offset=self.animation_style,
            bgcolor='green',
            content=Text('PAGE 2', size=50)
        )

        self.page3 = Container(
            alignment=alignment.center,
            offset=transform.Offset(0, 0),
            animate_offset=self.animation_style,
            bgcolor='orange',
            content=Text('PAGE 3', size=50),
        )

        self.switch_control = {
            'page1': self.page1,
            'page2': self.page2,
            'page3': self.page3,
        }

        self.pg.add(
            Container(
                bgcolor='white',
                expand=True,
                content=Row(
                    spacing=0,
                    controls=[
                        Container(
                            width=280,
                            border=border.only(right=border.BorderSide(width=1, color='#22888888'),),
                            content=Column(
                                alignment='spaceBetween',
                                controls=[
                                    Container(height=100),
                                    Container(
                                        height=500,
                                        content=Row(
                                            spacing=0,
                                            controls=[
                                                Container(expand=True, content=self.side_bar_column),
                                                Container(
                                                    width=3,
                                                    content=Column(
                                                        controls=[
                                                            self.indicator,
                                                        ]
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                    Container(height=50),
                                ]
                            )
                        ),
                        Container(
                            expand=True,
                            content=Stack(
                                controls=[
                                    self.page1,
                                    self.page2,
                                    self.page3,
                                ]
                            )
                        ),
                    ]
                )
            )
        )

    def create_sidebar_item(self, name, image_path, page):
        return Row(
            controls=[
                Container(
                    data=page,
                    on_click=lambda e: self.switch_page(e, page),
                    expand=True,
                    height=40,
                    content=Row(
                        controls=[
                            Container(
                                width=30,
                                height=30,
                                border_radius=15,
                                clip_behavior=ClipBehavior.HARD_EDGE,
                                content=Image(
                                    src=image_path,
                                    fit=ImageFit.COVER
                                ),
                            ),
                            Text(name, style={'paddingLeft': '10px'})  # Apply padding using style
                        ]
                    ),
                    bgcolor=self.get_bgcolor(page),
                    padding=5
                ),
            ]
        )

    def get_bgcolor(self, page):
        return 'lightblue' if self.active_page == page else 'transparent'

    def switch_page(self, e, point):
        self.active_page = point
        
        # Update indicator position
        self.indicator.offset.y = e.control.top
        self.indicator.update()

        for control in self.side_bar_column.controls:
            for container in control.controls:
                container.bgcolor = self.get_bgcolor(container.data)
                container.update()

        for page in self.switch_control:
            self.switch_control[page].offset.x = 2
            self.switch_control[page].update()

        self.switch_control[point].offset.x = 0
        self.switch_control[point].update()

app(target=App, assets_dir='assets')
