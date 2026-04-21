from plyer import notification

def enviar_notificacao(titulo, mensagem):
    notification.notify(
        title=titulo,
        message=mensagem,
        app_name="Minhas Tarefas",
        timeout=10
    )