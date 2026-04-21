from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from services import get_usuarios,post_usuario
from utils import hash_password
from components import ErrorDialog

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
   