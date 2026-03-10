from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

class DialogContent(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.adaptive_height = True
        self.spacing = 15
        self.padding = 15

        self.titulo_field = MDTextField(
            hint_text="Título",
            mode="rectangle",
        )
        self.descricao_field = MDTextField(
            hint_text="Descrição",
            mode="rectangle",
        )
        self.add_widget(self.titulo_field)
        self.add_widget(self.descricao_field)


class ErrorDialog(MDDialog):

    def __init__(self, message, **kwargs):

        super().__init__(
            title="Error",
            text=message,
            buttons=[
                MDFlatButton(
                    text="X",
                    on_release=lambda x: self.dismiss()
                )
            ],
            **kwargs
        )