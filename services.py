import requests
from dotenv import load_dotenv
import os

load_dotenv()

FIREBASE_URL = os.getenv("FIREBASE_URL")


def get_usuarios():
    response = requests.get(f"{FIREBASE_URL}/usuarios.json")
    if response.ok:
        return response.json()
    return None


def post_usuario(email, password):
    usuario = {"email": email, "password": password}
    response = requests.post(f"{FIREBASE_URL}/usuarios.json", json=usuario)
    return response.ok


def get_tarefas(user_id):
    response = requests.get(f"{FIREBASE_URL}/Tarefas/{user_id}.json")
    if response.ok:
        return response.json()
    return None


def post_tarefa(user_id, tarefa):
    response = requests.post(f"{FIREBASE_URL}/Tarefas/{user_id}.json", json=tarefa)
    return response.ok