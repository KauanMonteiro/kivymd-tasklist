from datetime import datetime
from services import editar_task
from kivymd.app import MDApp
from plyer import notification
import requests

def enviar_notificacao(titulo, mensagem, user_id):
    notification.notify(
        title=titulo,
        message=mensagem,
        app_name="Minhas Tarefas",
        timeout=10
    )
    try:
        requests.post(
            f"https://ntfy.sh/{user_id}-tarefas",
            json={"title": titulo, "message": mensagem}
        )
    except Exception:
        pass

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
    if not concluida:
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
 
