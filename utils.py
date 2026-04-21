import hashlib
from datetime import datetime
from services import editar_task
from kivymd.app import MDApp
from kivymd.uix.bottomsheet.bottomsheet import MDLabel
from kivymd.uix.list import OneLineAvatarIconListItem,IconRightWidget
from services import get_tarefas
from components import DialogContentTask,editar_task
from notificacoes import enviar_notificacao
def hash_password(password):
    hash_password = hashlib.sha256(password.encode()).hexdigest()
    return hash_password

def create_tarefa_payload(titulo, descricao, prazo):
    return {
        "titulo": titulo,
        "descricao": descricao,
        "prazo": prazo,
        "concluida": False,
        "prazo_vencido": False
    }

def verificar_prazo(tarefa_id, user_id, titulo, descricao, prazo, concluida, prazo_vencido):
    if not prazo:
        return

    try:
        data_prazo = datetime.strptime(prazo, "%d/%m/%Y %H:%M")
    except ValueError:
        return

    agora = datetime.now()
    diferenca = data_prazo - agora
    minutos = diferenca.total_seconds() / 60
    app = MDApp.get_running_app()

    if agora > data_prazo:
        chave = f"{tarefa_id}_atrasada"
        if chave not in app.notificacoes_enviadas:
            enviar_notificacao(titulo="Tarefa atrasada", mensagem=f"{titulo} está atrasada!,",user_id=user_id)
            app.notificacoes_enviadas.add(chave)
        return editar_task(
            tarefa_id,
            user_id,
            titulo,
            descricao,
            prazo,
            prazo_vencido=True
        )
    elif 0 < minutos <= 15:
        chave = f"{tarefa_id}_15min"
        if chave not in app.notificacoes_enviadas:
            enviar_notificacao(titulo="Lembrete de tarefa", mensagem=f"{titulo} vence em 15 minutos!",user_id=user_id)
            app.notificacoes_enviadas.add(chave)

    elif 15 < minutos <= 30:
        chave = f"{tarefa_id}_30min"
        if chave not in app.notificacoes_enviadas:
            enviar_notificacao(titulo="Lembrete de tarefa", mensagem=f"{titulo} vence em 30 minutos!",user_id=user_id)
            app.notificacoes_enviadas.add(chave)
    else:
        return False
    
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