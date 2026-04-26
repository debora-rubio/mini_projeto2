from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, DateTime, insert, text
from datetime import datetime

import time
from functools import wraps


def medir_tempo(func):
    """Decorator que mede o tempo de execução de uma função."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()  # tempo inicial (mais preciso que time.time)
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()     # tempo final
        duracao = fim - inicio
        print(f"⏱ Função '{func.__name__}' executada em {duracao:.6f} segundos.")
        return resultado
    return wrapper

engine = create_engine("postgresql+psycopg2://alunos:AlunoFatec@200.19.224.150:5432/atividade2", echo=False)
metadata = MetaData()

usuarios = Table(
    'usuarios', metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String(50), nullable=False, index=True),
    Column('cpf', String(14), nullable=False),
    Column('email', String(100), nullable=False, unique=True),
    Column('telefone', String(20), nullable=False),
    Column('data_nascimento', Date, nullable=False),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)

metadata.create_all(engine)

@medir_tempo
def LGPD(row):
    return row

users = []
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM usuarios LIMIT 5;"))
    for row in result:
        row = LGPD(row)
        users.append(row)

for user in users:
    print(user)

# ---------------------------
# Atividade 1 - Anonimização
# ---------------------------

def LGPD(row):
    # Desempacotar os campos da linha (vem do SELECT * FROM usuarios)
    id, nome, cpf, email, telefone, data_nascimento, created_on, updated_on = row

    # Nome: manter só a primeira letra, resto vira *
    partes_nome = nome.split(" ")
    partes_nome[0] = partes_nome[0][0] + "*" * (len(partes_nome[0]) - 1)
    nome_anon = " ".join(partes_nome)

    # CPF: mostrar só os 3 primeiros dígitos, resto vira *
    cpf_anon = cpf[:3] + ".***.***-**"

    # Email: esconder usuário, mostrar domínio
    usuario, dominio = email.split("@")
    email_anon = usuario[0] + "*" * (len(usuario) - 1) + "@" + dominio

    # Telefone: mostrar apenas os 4 últimos dígitos
    telefone_anon = telefone[-4:]

    # Retornar a tupla com os dados anonimizados
    return (id, nome_anon, cpf_anon, email_anon, telefone_anon, data_nascimento, created_on, updated_on)


users = []
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM usuarios LIMIT 10;"))
    for row in result:
        row = LGPD(row)   # aplica anonimização
        users.append(row)

print(users)

# ---------------------------
# Atividade 2 - Exportar por ano
# ---------------------------
import csv

def exportar_por_ano():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM usuarios"))
        for row in result:
            row = LGPD(row)  # aplica anonimização
            ano = row[5].year  # data_nascimento está na posição 5 da tupla
            nome_arquivo = f"{ano}.csv"

            # abre o arquivo no modo append (adicionar linhas)
            with open(nome_arquivo, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(row)

# Testar a função
exportar_por_ano()
