# Mini Projeto 2 - LGPD

Este projeto foi desenvolvido como parte da disciplina de Linguagem de Programação II na FATEC.  
O objetivo é aplicar conceitos da **Lei Geral de Proteção de Dados (LGPD)** em manipulação de dados usando Python.
Os dados de cada registro são dados fakers fornecidos pelo professor.

---

## Estrutura do Projeto
- `LGPD.py` → Script principal com todas as atividades.
- `todos.csv` → Arquivo único com nome e CPF de todos os registros (sem anonimização).
- `ANO.csv` → Arquivos separados por ano de nascimento (com anonimização).
- `log_tempo.txt` → Arquivo de log com os tempos de execução das atividades 2 e 3.
- `requirements.txt` → Dependências do projeto.

---

## Atividades

### Atividade 1
Anonimização de dados sensíveis (nome, CPF, email, telefone) usando função `LGPD(row)`.

### Atividade 2
Exportar registros anonimizados em arquivos separados por ano de nascimento.  
Exemplo: `2006.csv`, `1990.csv`.

### Atividade 3
Gerar um único relatório (`todos.csv`) contendo **nome e CPF** de todos os registros, sem anonimização.

### Atividade 4
Aplicar o decorador `@medir_tempo` para medir o tempo de execução das atividades 2 e 3.  
Os resultados são gravados em `log_tempo.txt` para comparação.

---

## Como executar
1. Clone o repositório ou copie os arquivos para sua máquina.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
