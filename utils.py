import hashlib

def hash_password(password):
    hash_password = hashlib.sha256(password.encode()).hexdigest()
    return hash_password

def create_tarefa_payload(titulo, descricao, prazo):
    return {
        "titulo": titulo,
        "descricao": descricao,
        "prazo": prazo,
        "concluida": False
    }