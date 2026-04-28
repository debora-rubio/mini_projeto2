Projeto LGPD - Manipulação de Dados e Performance

Este projeto foi desenvolvido como parte das atividades da faculdade Fatec Rio Claro, na matéria Linguagem de Programação II. O objetivo principal é aplicar os conceitos da Lei Geral de Proteção de Dados (LGPD) em um ambiente de banco de dados PostgreSQL, focando em anonimização de dados, exportação organizada e monitoramento de performance. O Banco de Dados fornecido pelo professor, possuem dados fakers.

Tecnologias Utilizadas:

Python: Linguagem principal do projeto.
SQLAlchemy: Para conexão e execução de comandos no banco de dados.
CSV: Biblioteca nativa para geração de relatórios.
PostgreSQL: Banco de dados utilizado para armazenamento dos usuários.

Funcionalidades (Atividades):

Atividade 1 - Anonimização de Dados:

Implementação da função `LGPD(row)` para tratar dados sensíveis conforme as regras.
Nome: Mantém a primeira letra e oculta o restante com asteriscos.
CPF: Exibe apenas os 3 primeiros dígitos.
E-mail: Oculta o nome de usuário, mantendo o domínio visível.
Telefone: Exibe apenas os 4 últimos dígitos.

Atividade 2 - Exportação por Ano:

O sistema filtra todos os usuários do banco e gera arquivos CSV individuais nomeados pelo ano de nascimento (ex: `1990.csv`), contendo os dados devidamente anonimizados.

Atividade 3 - Exportação Geral (Dados Brutos):

Geração de um arquivo único chamado `todos.csv` contendo apenas os campos **Nome** e **CPF** sem anonimização.

Atividade 4 - Monitoramento e Log:

Utilização de um **decorator** (`medir_tempo`) para capturar o tempo de execução das atividades de exportação. Os logs são exibidos no terminal e registrados permanentemente no arquivo `log_tempo.txt` com data e hora.

Como Executar:

1-Certifique-se de ter as bibliotecas necessárias instaladas:

pip install sqlalchemy==2.0.43 psycopg2-binary==2.9.12 packaging==26.2 setuptools==82.0.1 typing_extensions==4.15.0 wheel==0.47.0

* SQLAlchemy (2.0.43): Para a abstração e conexão com o banco de dados.
* psycopg2-binary (2.9.12): Driver de conexão para o PostgreSQL.
* packaging (26.2): Controle de pacotes.
* setuptools (82.0.1)
* wheel (0.47.0): Suporte para instalação e compilação de pacotes.
* typing_extensions (4.15.0): Suporte para tipagem avançada em versões do Python.CSV
* Functools: Bibliotecas nativas para geração de relatórios e manipulação de funções.  

    
2-Execute o script principal:

python seu_arquivo.py
    
3-Resultados esperados:

* Visualização de 5 usuários anonimizados no terminal.
* Criação dos arquivos `.csv` por ano.
* Criação do arquivo `todos.csv`.
* Atualização do arquivo `log_tempo.txt`.

Estrutura de Arquivos:

`seu_arquivo.py`: Código fonte principal.
`log_tempo.txt`: Registro de performance das funções.
`*.csv`: Relatórios gerados pelo sistema.



