import flet as ft
from flet_toast import flet_toast
from views.controls import Message

class Home(ft.View):
    def __init__(
        self,
        page: ft.Page
    ):
        self.Page = page
        super().__init__()
        self.route = '/'
        self.padding = ft.padding.all(0)
        self.controls = [
            ft.Stack(
                controls=[
                    ChatBackGround(page=page, image_path='chatmessage_bg.jpg'),
                    Username(page=page)
                ],
                alignment=ft.alignment.center
            )
        ]
    
    def send_message(self, message: Message):
        chatspace: ft.Container = self.Page.views[-1].controls[0].controls[1]
        
        if message.message:
            chatspace.content.controls.append(
                ft.Row(
                    controls=[
                        UserMessage(
                            page=self.Page,
                            message=Message(
                                username=message.username,
                                message=message.message,
                                session_id=message.session_id
                            )
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END if message.session_id == self.Page.session_id else None
                )
            )
        
        else:
            chatspace.content.controls.append(
                JoinUser(
                    page=self.Page,
                    username=message.username
                )
            )
        
        self.Page.update()

class ChatBackGround(ft.Container):
    def __init__(
        self,
        page: ft.Page,
        image_path: str
    ):
        super().__init__()
        self.image_path = image_path
        self.width = page.width
        self.height = page.height
        self.image = ft.DecorationImage(
            src=self.image_path,
            fit=ft.ImageFit.COVER
        )

class Username(ft.TextField):
    def __init__(
        self,
        page: ft.Page
    ):
        super().__init__()
        self.prefix_icon = ft.icons.PERSON
        self.hint_text = 'Username'
        self.autofocus = True
        self.hint_style = ft.TextStyle(
            color=ft.colors.with_opacity(0.4, 'black'),
            size=14,
            weight='bold'
        )
        self.text_style = ft.TextStyle(
            color=ft.colors.with_opacity(0.8, 'black'),
            size=14,
            weight='bold'
        )
        self.bgcolor = ft.colors.with_opacity(0.80, 'white')
        self.border_width = 1
        self.border_color = self.bgcolor
        self.focused_border_color = self.bgcolor
        self.width = page.width * 1/4
        self.on_submit = self.get_username
    
    def get_username(self, e: ft.ControlEvent):
        if e.control.value.strip():
            page: ft.Page = e.page

            chatspace: ChatSpace = ChatSpace(
                page=page,
                username=e.control.value.strip()
            )

            page.views[-1].controls[0].alignment = ft.alignment.bottom_center
            page.views[-1].controls[0].controls.remove(self)

            page.views[-1].controls[0].controls.append(
                chatspace
            )

            page.views[-1].controls[0].controls.append(
                WriteSpace(
                    page=page,
                    username=e.control.value.strip()
                )
            )

            page.pubsub.send_all(message=Message(
                    username=e.control.value.strip(),
                    message=None,
                    session_id=e.page.session_id
                )
            )

            page.update()
        
        else:
            flet_toast.warning(
                page=e.page,
                message='Username inválido!',
                position=flet_toast.Position.TOP_RIGHT
            )

class WriteSpace(ft.Container):
    def __init__(
        self,
        page: ft.Page,
        username: str
    ):
        super().__init__()
        self.username = username
        self.width = page.width
        self.bgcolor = ft.colors.with_opacity(0.9, 'white')
        self.padding = ft.padding.only(
            left=10
        )
        self.content = ft.ResponsiveRow(
            controls=[
                space_message := ft.TextField(
                    hint_text='Escreva a sua messagem',
                    hint_style = ft.TextStyle(
                        color=ft.colors.with_opacity(0.4, 'black'),
                        size=14,
                        weight='bold'
                    ),
                    border=ft.InputBorder.NONE,
                    text_vertical_align=-0.5,
                    autofocus=True,
                    text_style = ft.TextStyle(
                        color=ft.colors.with_opacity(0.8, 'black'),
                        size=14,
                        weight='bold'
                    ),
                    col={'xs': 10.6, 'sm': 11, 'md': 11.4},
                    on_submit=self.send_message
                ),
                ft.IconButton(
                    icon=ft.icons.SEND,
                    icon_color=ft.colors.with_opacity(0.4, 'black'),
                    icon_size=18,
                    col={'xs': 1.4, 'sm': 1, 'md': 0.6},
                    on_click=self.send_message
                )
            ],
            vertical_alignment=ft.CrossAxisAlignment.END
        )

        self.space_message = space_message
    
    def send_message(self, e: ft.ControlEvent):
        if self.space_message.value:
            e.page.pubsub.send_all(message=Message(
                    username=self.username,
                    message=self.space_message.value,
                    session_id=e.page.session_id
                )
            )

            self.space_message.value = ''
            self.space_message.focus()
        
        e.page.update()

class ChatSpace(ft.Container):
    def __init__(
        self,
        page: ft.Page,
        username: str
    ):
        super().__init__()
        self.username = username
        self.top = 2
        self.width = page.width
        self.height = page.height - 50
        self.padding = ft.padding.only(
            left=10,
            right=10
        )
        self.content = ft.Column(
            controls=[

            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            auto_scroll=True,
            width=self.width
        )

class JoinUser(ft.Row):
    def __init__(
        self,
        page: ft.Page,
        username: str
    ):
        super().__init__()
        self.alignment = ft.MainAxisAlignment.CENTER
        self.controls = [
            ft.Container(
                padding=ft.padding.only(
                    left=4,
                    right=4,
                    top=2,
                    bottom=2
                ),
                border_radius = 3,
                bgcolor = ft.colors.with_opacity(0.6, 'black'),
                content = ft.Text(
                    value=f'--- {username} joined on the chat ---',
                    size=13,
                    weight='bold',
                    color=ft.colors.BLUE_GREY
                )
            )
        ]

class UserMessage(ft.Container):
    def __init__(
        self,
        page: ft.Page,
        message: Message
    ):
        super().__init__()
        self.bgcolor = ft.colors.GREEN
        self.border_radius = ft.border_radius.only(
            top_left=0 if message.session_id != page.session_id else 4,
            top_right=4 if message.session_id != page.session_id else 0,
            bottom_left=4,
            bottom_right=4
        )
        self.padding = ft.padding.all(4)
        self.content = ft.Column(
            controls=[
                ft.Text(
                    value=message.username,
                    weight='bold',
                    size=13
                ),
                ft.Text(
                    value=message.message,
                    size=13,
                    color=ft.colors.with_opacity(0.8, 'black'),
                    no_wrap=False
                )
            ],
            spacing=1
        )