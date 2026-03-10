from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from screens import LoginScreen, SignupScreen, HomeScreen

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


if __name__ == "__main__":
    MainApp().run()