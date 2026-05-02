import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timezone
load_dotenv()

FIREBASE_URL = os.getenv("FIREBASE_URL")

def get_tarefas(user_id):
    response = requests.get(f"{FIREBASE_URL}/Tarefas/{user_id}.json")
    if response.ok:
        return response.json()
    return None

def soft_delete_tarefa(user_id, tarefa_id):
    deletado_em = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    data = {
        "deletada": True,
        "deletado_em": deletado_em,  # ex: "2026-05-02T14:32:00Z"
    }

def post_tarefa(user_id, tarefa):
    response = requests.post(f"{FIREBASE_URL}/Tarefas/{user_id}.json", json=tarefa)
    return response.ok

def delete_tarefa(user_id,tarefa_id):
    response = requests.delete(f"{FIREBASE_URL}/Tarefas/{user_id}/{tarefa_id}.json")
    return response.ok

def editar_task(tarefa_id, user_id, titulo, descricao, prazo,deletado_em, concluida=False,prazo_vencido=False,deletado=False):
    data = {"titulo": titulo, "descricao": descricao, "prazo": prazo, "concluida": concluida,"prazo_vencido":prazo_vencido,"deletado":deletado,"deletado_em":deletado_em}
    response = requests.patch(f'{FIREBASE_URL}/Tarefas/{user_id}/{tarefa_id}.json', json=data)
    return response.ok