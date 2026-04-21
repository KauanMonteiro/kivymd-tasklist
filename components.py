from kivymd.uix.button import MDIconButton,MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.app import MDApp
from services import delete_tarefa,editar_task
from kivymd.uix.pickers import MDTimePicker,MDDatePicker
class DialogContent(MDBoxLayout):

    def __init__(self, titulo="", descricao="",prazo="", **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.adaptive_height = True
        self.spacing = 15
        self.padding = 15

        self.titulo_field = MDTextField(
            hint_text="Título",
            mode="rectangle",
            text=titulo
        )

        self.descricao_field = MDTextField(
            hint_text="Descrição",
            mode="rectangle",
            text=descricao
        )

        self.prazo_field = MDRaisedButton(
            text=prazo if prazo else "Selecionar data e horário",
            on_release=self.show_date_picker
            )

        self.add_widget(self.titulo_field)
        self.add_widget(self.descricao_field)
        self.add_widget(self.prazo_field)

    def show_date_picker(self, instance):
        self.date_picker = MDDatePicker()
        self.date_picker.bind(on_save=self.on_date_selected)
        self.date_picker.open()

    def on_date_selected(self, instance, value, date_range):
        self.selected_date = value  # guarda a data
        # abre o time picker logo depois
        self.time_picker = MDTimePicker()
        self.time_picker.bind(time=self.on_time_selected)
        self.time_picker.open()

    def on_time_selected(self, instance, time):
        data_hora = f"{self.selected_date.strftime('%d/%m/%Y')} {time.strftime('%H:%M')}"
        self.prazo_field.text = data_hora

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
    def __init__(self,titulo,descricao,prazo,tarefa_id,user_id,**kwargs):
        from utils import carregar_tarefas

        app = MDApp.get_running_app()
        if prazo:
            fulltext= f'{descricao}\nPrazo:{prazo}'
        else:
            fulltext = descricao
        super().__init__(
            title=titulo,
            text=fulltext,
            buttons=[
                MDIconButton(
                    icon='pencil',
                    md_bg_color=app.theme_cls.primary_color,
                    on_release=lambda x: (EditarTask(tarefa_id=tarefa_id,user_id=user_id,titulo=titulo,descricao=descricao,prazo=prazo).open(),self.dismiss())
                ),
                MDIconButton(
                    icon='trash-can',
                    md_bg_color=app.theme_cls.primary_color,
                    on_release=lambda x: (delete_tarefa(tarefa_id=tarefa_id, user_id=user_id), self.dismiss(),app.root.get_screen(app.root.current).reload())
                ),
                MDIconButton(
                    icon='close',
                    on_release=lambda x: self.dismiss(),
                ),
            ],
            **kwargs
        )

class EditarTask(MDDialog):

    def __init__(self, titulo, descricao,prazo, tarefa_id, user_id,prazo_vencido=None, **kwargs):
        from utils import carregar_tarefas
        app = MDApp.get_running_app()

        self.dialogcontent = DialogContent(
            titulo=titulo,
            descricao=descricao,
            prazo=prazo,
        )

        super().__init__(
            title="Editar Tarefa",
            type="custom",
            content_cls=self.dialogcontent,
            buttons=[
                MDFlatButton(
                    text="Salvar",
                    on_release=lambda x: (
                        editar_task(
                            tarefa_id,
                            user_id,
                            self.dialogcontent.titulo_field.text,
                            self.dialogcontent.descricao_field.text,
                            self.dialogcontent.prazo_field.text,
                        ),
                        self.dismiss(),
                        app.root.get_screen(app.root.current).reload()
                    )
                )
            ],
            **kwargs
        )
class AddTaskDialog(MDDialog):
    def __init__(self, on_save, **kwargs):
        self.dialog_content = DialogContent()
        self.on_save_callback = on_save
        super().__init__(
            title="Adicionar Tarefa",
            type="custom",
            content_cls=self.dialog_content,
            buttons=[
                MDFlatButton(
                    text="Salvar",
                    on_release=self._on_save
                )
            ],
            **kwargs
        )

    def _on_save(self, *args):
        self.on_save_callback(
            self.dialog_content.titulo_field.text,
            self.dialog_content.descricao_field.text,
            self.dialog_content.prazo_field.text,
        )
        self.dismiss()