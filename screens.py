from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from services import get_usuarios,post_usuario,post_tarefa
from utils import hash_password, create_tarefa_payload,carregar_tarefas
from components import ErrorDialog, DialogContentTask, AddTaskDialog,editar_task

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

    def _on_task_release(self, tarefa, tarefa_id):
        app = MDApp.get_running_app()
        DialogContentTask(
            titulo=tarefa["titulo"],
            descricao=tarefa["descricao"],
            prazo=tarefa["prazo"],
            tarefa_id=tarefa_id,
            user_id=app.user_id
        ).open()
    def reload(self):
        carregar_tarefas(self, concluida=False, prazo_vencido=False, deletada=False)
    def on_enter(self, *args):
        app = MDApp.get_running_app()
        if app.user:
            carregar_tarefas(self,concluida= False,prazo_vencido=False,deletada=False)
        else:
            self.manager.current = "login"
    def concluir_tarefa(self, tarefa_id, titulo, descricao, prazo):
        app = MDApp.get_running_app()
        editar_task(
            tarefa_id=tarefa_id, user_id=app.user_id,
            titulo=titulo, descricao=descricao,
            prazo=prazo, concluida=True,
        )
        carregar_tarefas(self,concluida= False,prazo_vencido=False,deletada=False)

    def logout(self):
        app = MDApp.get_running_app()
        app.user = None
        self.manager.current = "login"

    def add_task_form(self):
        AddTaskDialog(on_save=self.add_task).open()

    def add_task(self, titulo, descricao, prazo):
        app = MDApp.get_running_app()
        tarefa = create_tarefa_payload(titulo, descricao, prazo)
        if post_tarefa(app.user_id, tarefa):
           carregar_tarefas(self,concluida= False,prazo_vencido=False,deletada=False)
        else:
            ErrorDialog("Erro ao cadastrar").open()

class AtrasadasScreen(Screen):
    def _on_task_release(self, tarefa, tarefa_id):
        app = MDApp.get_running_app()
        DialogContentTask(
            titulo=tarefa["titulo"],
            descricao=tarefa["descricao"],
            prazo=tarefa["prazo"],
            tarefa_id=tarefa_id,
            user_id=app.user_id
        ).open()
    def reload(self):
        carregar_tarefas(self, concluida=False, prazo_vencido=True, deletada=False)
    def on_enter(self, *args):
        app = MDApp.get_running_app()
        if app.user:
            carregar_tarefas(self,concluida=False,prazo_vencido=True,deletada=False)
        else:
            self.manager.current = "login"
    def concluir_tarefa(self, tarefa_id, titulo, descricao, prazo):
        app = MDApp.get_running_app()
        editar_task(
            tarefa_id=tarefa_id, user_id=app.user_id,
            titulo=titulo, descricao=descricao,
            prazo=prazo, concluida=True,
        )
        carregar_tarefas(self,concluida= False,prazo_vencido=True,deletada=False)

class ConcluidasScreen(Screen):
    def _on_task_release(self, tarefa, tarefa_id):
        app = MDApp.get_running_app()
        DialogContentTask(
            titulo=tarefa["titulo"],
            descricao=tarefa["descricao"],
            prazo=tarefa["prazo"],
            tarefa_id=tarefa_id,
            user_id=app.user_id
        ).open()
    def reload(self):
        carregar_tarefas(self, concluida=True, deletada=False)
    def on_enter(self, *args):
        app = MDApp.get_running_app()
        
        if not app.user:
            self.manager.current = "login"
            return

        carregar_tarefas(self, concluida=True,deletada=False)