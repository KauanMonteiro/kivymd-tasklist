from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from screens import LoginScreen, SignupScreen, HomeScreen
from kivy.clock import Clock
from utils import verificar_prazo
from services import get_tarefas
class Manager(ScreenManager):
    pass

class MainApp(MDApp):

    def build(self):
        self.user = None
        self.user_id = None

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Pink"

        sm = Manager()

        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SignupScreen(name="signup"))
        sm.add_widget(HomeScreen(name="home"))

        return sm
    def on_start(self):
        Clock.schedule_interval(self.update_status, 60)

    def update_status(self, dt):
        tarefas = get_tarefas(self.user_id)

        if not tarefas:
            return

        for tarefa_id, tarefa in tarefas.items():
            verificar_prazo(
                tarefa_id,
                self.user_id,
                tarefa.get("titulo"),
                tarefa.get("descricao"),
                tarefa.get("prazo"),
                tarefa.get("concluida", False),
                tarefa.get("prazo_vencido", False),
            )
        home_screen = self.root.get_screen("home")
        home_screen.carregar_tarefas()
if __name__ == "__main__":
    MainApp().run()