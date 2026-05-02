from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.app import MDApp
from services import editar_task

class EditarTask(MDDialog):

    def __init__(self, titulo, descricao,prazo, tarefa_id, user_id,prazo_vencido=None,deletado=False, **kwargs):
        from .dialogs import DialogContent

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
