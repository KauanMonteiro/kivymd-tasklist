from kivymd.uix.bottomsheet.bottomsheet import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.app import MDApp
from services import delete_tarefa
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

class DialogContentTask(MDDialog):
    def __init__(self,titulo,descricao,tarefa_id,user_id,**kwargs):
        app = MDApp.get_running_app()
        super().__init__(
            title=titulo,
            text=descricao,
            buttons=[
                MDIconButton(
                    icon='pencil',
                    md_bg_color=app.theme_cls.primary_color,
                ),
                MDIconButton(
                    icon='trash-can',
                    md_bg_color=app.theme_cls.primary_color,
                    on_release=lambda x: (delete_tarefa(tarefa_id=tarefa_id, user_id=user_id), self.dismiss(),app.root.get_screen('home').carregar_tarefas())
                ),
                MDIconButton(
                    icon='close',
                    on_release=lambda x: self.dismiss(),
                ),
            ],
            **kwargs
        )