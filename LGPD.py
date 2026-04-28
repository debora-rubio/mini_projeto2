from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, DateTime, text
from datetime import datetime
import time
from functools import wraps
import csv

# Banco de dados fornecido pelo professor com dados fakers.
# engine = create_engine - motor de conexão do código python com o servidor postgreSQL.
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


# Atividade 4 - Ajustando o decorator de medição de tempo, e gravando em log.txt, comparar atividade 2 e 3.
 

def medir_tempo(func):
    # O @wraps é o "Decorator, que mede o tempo de execução de uma função e grava em log.txt"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()
        duracao = fim - inicio

        # mensagem de log com data/hora
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mensagem = f"[{agora}] Função '{func.__name__}' executada em {duracao:.6f} segundos.\n"

        # imprime no terminal
        print(mensagem.strip())

        # Aqui é onde vai comparar os tempos das atividades 2 e 3.
        # grava em arquivo log_tempo.txt                             # with abre o arquivo e fecha depois.
        with open("log_tempo.txt", "a", encoding="utf-8") as log:    # "a" de append, para que nao seja escrito por cima do log anterior.
            log.write(mensagem)                                      # encoding="utf-8" é um tradutor de caracteres, evitando erros de acentuação,
                                                                     # emogis, um "ç", etc que estiverem no banco de dados.
        return resultado
    return wrapper


# Atividade 1 - Anonimização - 5 nomes.


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



# Atividade 2 - Exportar por ano de nascimento com anonimização.(lista gerada ao lado, desde 1951 até 2011).


@medir_tempo
def exportar_por_ano():
    with engine.connect() as conn:    # conecta ao banco de dados, e garante que a conexão seja fechada depois do bloco.
        result = conn.execute(text("SELECT * FROM usuarios"))
        
        # Vamos guardar os registros separados por ano em um dicionário
        registros_por_ano = {}

        for row in result:
            row = LGPD(row)  # aplica anonimização
            ano = row[5].year  # data_nascimento está na posição 5 da tupla

            # Se o ano ainda não existe no dicionário, cria uma lista
            if ano not in registros_por_ano:
                registros_por_ano[ano] = []
            
            # Adiciona o registro na lista do ano correspondente
            registros_por_ano[ano].append(row)

        # Agora criamos um arquivo .csv para cada ano
        for ano, registros in registros_por_ano.items():
            nome_arquivo = f"{ano}.csv"
            with open(nome_arquivo, "w", newline="", encoding="utf-8") as f: #"w"(write), o Python apaga tudo o que já esta escrito e começa do zero.
                writer = csv.writer(f)
                # opcional: cabeçalho
                writer.writerow(["id", "nome", "cpf", "email", "telefone", "data_nascimento", "created_on", "updated_on"])
                writer.writerows(registros)


# # Atividade 3 - Arquivo todos.csv gerado ao lado - Exportar todos (nome e CPF sem anonimizar)

@medir_tempo
def exportar_todos():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM usuarios"))
        
        # Criar um único arquivo CSV
        with open("todos.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # Cabeçalho opcional
            writer.writerow(["nome", "cpf"])
            
            # Escreve todos os registros
            for row in result:
                # Dados não devem ser anonimizados nesta atividade
                id, nome, cpf, email, telefone, data_nascimento, created_on, updated_on = row
                writer.writerow([nome, cpf])


# Execução do código: aqui é onde o código realmente roda (motor), chamando as funções, garantindo que a tabela existe no
# banco de dados, imprime os 5 usuários anonimizados e depois executa as atividades 2 e 3, disparando a medição de tempo
# da atividade 4, gravando os tempos no log_tempo.txt. Imprimi no terminal o tempo de execução de cada função e compara os
# tempos das atividades 2 e 3, mostrando qual foi mais rápido.

if __name__ == "__main__":     # motor

    # Garante que a tabela existe no banco, se não existir, cria. Se já existir, não faz nada.
    metadata.create_all(engine)

    # Execução da Atividade 1: Imprimir 5 usuários anonimizados no terminal
    print("\n--- ATIVIDADE 1: 5 USUÁRIOS ANONIMIZADOS ---")
    with engine.connect() as conn:           # abre a porta de conexão com o banco de dados e fecha depois do bloco.
        result = conn.execute(text("SELECT * FROM usuarios LIMIT 5;"))
        for row in result:
            row_anon = LGPD(row)   # aqui é onde a função de anonimização é aplicada a cada linha do banco de dados.
            print(row_anon)
    print("------------------------------------------\n")

    # Execução das Atividades 2 e 3 (que disparam a Atividade 4 através do decorator)
    exportar_por_ano()
    exportar_todos()