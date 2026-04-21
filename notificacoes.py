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