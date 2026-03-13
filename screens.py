from kivymd.uix.bottomsheet.bottomsheet import MDLabel
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import OneLineAvatarIconListItem,IconRightWidget
from services import get_usuarios,post_usuario,get_tarefas,post_tarefa,editar_task
from components import DialogContent,ErrorDialog,DialogContentTask
from utils import hash_password

class LoginScreen(Screen):

    def LoginValidation(self, email, password):

        usuarios = get_usuarios()
        password_hash = hash_password(password)

        if usuarios:
            for id, usuario in usuarios.items():
                if usuario["email"] == email and usuario["password"] == password_hash:

                    app = MDApp.get_running_app()

                    app.user = usuario
                    app.user_id = id

                    self.manager.current = "home"
                    return

        ErrorDialog("Email ou senha incorretos").open()

class SignupScreen(Screen):

    def SignupValidation(self, email, password):
        password_hash = hash_password(password)
        if post_usuario(email, password_hash):
            self.manager.current = "login"
        else:
            ErrorDialog("Erro ao cadastrar").open()

class HomeScreen(Screen):
    def carregar_tarefas(self):

        app = MDApp.get_running_app()
        tarefas = get_tarefas(app.user_id)
        if tarefas:
            self.ids.task_list.clear_widgets()
            for id, tarefa in tarefas.items():
                if not tarefa['concluida']:
                    item = OneLineAvatarIconListItem(
                        text=tarefa["titulo"],
                        on_release=lambda x, titulo=tarefa["titulo"], descricao=tarefa["descricao"],
                            prazo=tarefa["prazo"], tarefa_id=id: DialogContentTask(
                                titulo=titulo, descricao=descricao,
                                tarefa_id=tarefa_id, prazo=prazo,
                                user_id=app.user_id
                            ).open()
                    )

                    icon_widget = IconRightWidget(
                        icon="check",
                        on_release=lambda x, titulo=tarefa["titulo"], descricao=tarefa["descricao"],
                            prazo=tarefa["prazo"], tarefa_id=id: self.concluir_tarefa(
                                titulo=titulo, descricao=descricao,
                                tarefa_id=tarefa_id, prazo=prazo,
                                
                            )
                    )
                    item.add_widget(icon_widget)
                    self.ids.task_list.add_widget(item)
        else:
            self.ids.task_list.clear_widgets()
            self.ids.task_list.add_widget(
                MDLabel(
                    text='Não foi encontrado nem uma tarefa'
                )
            )

    def on_enter(self, *args):

        app = MDApp.get_running_app()

        if app.user:

            self.carregar_tarefas()

        else:
            self.manager.current = "login"

    def concluir_tarefa(self, tarefa_id, titulo, descricao, prazo):
        app = MDApp.get_running_app()
        editar_task(
            tarefa_id=tarefa_id, user_id=app.user_id,
            titulo=titulo, descricao=descricao,
            prazo=prazo, concluida=True
        )
        self.carregar_tarefas()  

    def logout(self):

        app = MDApp.get_running_app()
        app.user = None

        self.manager.current = "login"

    def add_task_form(self):

        self.dialogcontent = DialogContent()

        self.form = MDDialog(
            title="Adicionar Tarefa",
            type="custom",
            content_cls=self.dialogcontent,
            buttons=[
                MDFlatButton(
                    text="Salvar",
                    on_release=lambda x: self.add_task(
                        self.dialogcontent.titulo_field.text,
                        self.dialogcontent.descricao_field.text,
                        self.dialogcontent.prazo_field.text,
                    ),
                )
            ],
        )

        self.form.open()

    def add_task(self, titulo, descricao,prazo):

        tarefa = {
            "titulo": titulo,
            "descricao": descricao,
            "prazo":prazo,
            "concluida":False
        }

        app = MDApp.get_running_app()

        if post_tarefa(app.user_id, tarefa):

            self.carregar_tarefas()
            self.form.dismiss()

        else:
            ErrorDialog("Erro ao cadastrar").open()