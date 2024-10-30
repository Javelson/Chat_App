import flet as ft
from flet_toast import flet_toast
from views.controls import Message

class Home(ft.View):
    def __init__(self, page: ft.Page):
        self.page = page
        super().__init__()
        self.route = '/'
        self.padding = ft.padding.all(0)
        self.controls = [
            ft.Stack(
                controls=[
                    ChatBackGroud(page=page, image_path='assents/R.jpeg'),
                    Username(page=page)
                ],
                alignment=ft.alignment.center
            )
        ]

    def send_message(self, message: Message):
        chatspace: ft.Container = self.page.views[-1].controls[0].controls[1]

        if message.message:
            chatspace.content.controls.append(
                ft.Row(
                    controls=[
                        UserMessage(
                            page=self.page,
                            message=Message(
                                username=message.username,
                                message=message.message,
                                session_id=message.session_id
                            )
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END if message.session_id == self.page.session_id else None
                )
            )
        else:
            chatspace.content.controls.append(
                Joinuser(
                    page=self.page,
                    username=message.username
                )
            )
        
        self.page.update()

class ChatBackGroud(ft.Container):
    def __init__(self, page: ft.Page, image_path: str):
        super().__init__()
        self.image_path = image_path
        self.width = page.width
        self.height = page.height
        self.image = ft.DecorationImage(
            src=self.image_path,
            fit=ft.ImageFit.COVER
        )

class Username(ft.TextField):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.prefix_icon = ft.icons.PERSON
        self.hint_text = 'Username'
        self.autofocus = True
        self.hint_style = ft.TextStyle(
            color=ft.colors.with_opacity(0.8, 'black'),
            size=14,
            weight='bold'
        )
        self.bgcolor = ft.colors.with_opacity(0.88, 'black')
        self.border_width = 1
        self.border_color = self.bgcolor
        self.focused_border_color = self.bgcolor
        self.width = page.width * 1 / 4
        self.on_submit = self.get_username

    def get_username(self, e: ft.ControlEvent):
        if e.control.value.strip():
            page: ft.Page = e.page
            chatSpace: ChatSpace = ChatSpace(page=page, username=e.control.value.strip())

            page.views[-1].controls[0].alignment = ft.alignment.bottom_center
            page.views[-1].controls[0].controls.remove(self)
            
            page.views[-1].controls[0].controls.append(chatSpace)
            page.views[-1].controls[0].controls.append(
                WriteSpace(page=page, username=e.control.value.strip())
            )
            
            page.pubsub.send_all(message=Message(
                username=e.control.value.strip(),
                message=None,
                session_id=e.page.session_id
            ))
            page.update()
        else:
            flet_toast.warning(
                page=e.page,
                message='Username Inválido',
                position=flet_toast.Position.TOP_RIGHT
            )

class WriteSpace(ft.Container):
    def __init__(self, page: ft.Page, username: str):
        super().__init__()
        self.username = username
        self.width = page.width
        self.bgcolor = ft.colors.with_opacity(0.9, 'white')
        self.padding = ft.padding.only(left=10)
        self.alignment = ft.alignment.bottom_left
        self.image = ft.DecorationImage(
            src='assents/R.jpeg',
            fit=ft.ImageFit.COVER
        )
        self.background = ft.BoxDecoration(image=self.image)
        self.content = ft.ResponsiveRow(
            controls=[
                Space_menssege := ft.TextField(
                    hint_text='Escreva sua mensagem',
                    hint_style=ft.TextStyle(
                        color=ft.colors.with_opacity(0.8, 'black'),
                        size=14,
                        weight='bold'
                    ),
                    border=ft.InputBorder.NONE,
                    autofocus=True,
                    text_style=ft.TextStyle(
                        color=ft.colors.with_opacity(0.8, 'black'),
                        size=14,
                        weight='bold'
                    ),
                    col={'xs': 10.6, 'sm': 11, 'md': 11.4},
                    on_submit=self.send_messege
                ),
                ft.IconButton(
                    icon=ft.icons.SEND,
                    icon_color=ft.colors.with_opacity(0.8, 'red'),
                    icon_size=18,
                    col={'xs': 1, 'sm': 1, 'md': 0.6},
                    on_click=self.send_messege
                )
            ],
            vertical_alignment=ft.CrossAxisAlignment.END
        )
        self.Space_messege = Space_menssege

    def send_messege(self, e: ft.ControlEvent):
        if self.Space_messege.value:
            e.page.pubsub.send_all(message=Message(
                username=self.username,
                message=self.Space_messege.value,
                session_id=e.page.session_id
            ))
            self.Space_messege.value = ''
            self.Space_messege.focus()
        e.page.update()

class ChatSpace(ft.Container):
    def __init__(self, page: ft.Page, username: str):
        super().__init__()
        self.username = username
        self.top = 2
        self.width = page.width 
        self.height = page.height - 50
        self.padding = ft.padding.only(left=10, right=10)
        self.content = ft.Column(
            controls=[],
            scroll=ft.ScrollMode.ADAPTIVE,
            auto_scroll=True,
            width=self.width,
        )

class Joinuser(ft.Row):
    def __init__(self, page: ft.Page, username: str):
        super().__init__()
        self.username = username
        self.alignment = ft.MainAxisAlignment.CENTER
        self.controls = [
           ft.Container(
               padding=ft.padding.only(left=4, right=4, top=2, bottom=2),
               border_radius=3,
               width=page.width,
               bgcolor=ft.colors.with_opacity(0.6, 'black'),
               content=ft.Text(
                   value=f'--- {username} Joined on the chat ---',
                   size=13,
                   weight='bold',
                   color=ft.colors.BLUE_GREY,
                   italic=True
               )
           )
        ]

class UserMessage(ft.Container):
    def __init__(self, page: ft.Page, message: Message):
        super().__init__()
        self.bgcolor = ft.colors.GREEN if message.session_id != page.session_id else ft.colors.RED
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
                    value=message.message,
                    weight='bold',
                    size=13,
                    color=ft.colors.with_opacity(0.9, 'black'),
                    no_wrap=False
                )
            ],
            spacing=1
        )
