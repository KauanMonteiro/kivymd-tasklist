import hashlib
from datetime import datetime
from services import editar_task
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

    if agora > data_prazo:
        return editar_task(
            tarefa_id,
            user_id,
            titulo,
            descricao,
            prazo,
            concluida = False,
            prazo_vencido=True
        )
    else:
        return False