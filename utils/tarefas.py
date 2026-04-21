from kivymd.app import MDApp
from kivymd.uix.bottomsheet.bottomsheet import MDLabel
from kivymd.uix.list import OneLineAvatarIconListItem,IconRightWidget
from services import get_tarefas
from components import DialogContentTask

def create_tarefa_payload(titulo, descricao, prazo):
    return {
        "titulo": titulo,
        "descricao": descricao,
        "prazo": prazo,
        "concluida": False,
        "prazo_vencido": False
    }

def carregar_tarefas(self, concluida=None, prazo_vencido=None, deletada=None):
    app = MDApp.get_running_app()
    tarefas = get_tarefas(app.user_id)

    self.ids.task_list.clear_widgets()

    if not tarefas:
        self.ids.task_list.add_widget(
            MDLabel(text='Não foi encontrado nenhuma tarefa')
        )
        return

    for id, tarefa in tarefas.items():
        if concluida is not None and tarefa['concluida'] != concluida:
            continue
        if prazo_vencido is not None and tarefa['prazo_vencido'] != prazo_vencido:
            continue
        if deletada is not None and tarefa.get('deletada', False) != deletada:
            continue

        item = OneLineAvatarIconListItem(
            text=tarefa["titulo"],
            on_release=lambda x, titulo=tarefa["titulo"], descricao=tarefa["descricao"],
                prazo=tarefa["prazo"], tarefa_id=id: DialogContentTask(
                    titulo=titulo,
                    descricao=descricao,
                    tarefa_id=tarefa_id,
                    prazo=prazo,
                    user_id=app.user_id
                ).open()
        )

        icon_widget = IconRightWidget(
            icon="check",
            on_release=lambda x, titulo=tarefa["titulo"], descricao=tarefa["descricao"],
                prazo=tarefa["prazo"], tarefa_id=id: self.concluir_tarefa(
                    titulo=titulo,
                    descricao=descricao,
                    tarefa_id=tarefa_id,
                    prazo=prazo,
                )
        )

        item.add_widget(icon_widget)
        self.ids.task_list.add_widget(item)