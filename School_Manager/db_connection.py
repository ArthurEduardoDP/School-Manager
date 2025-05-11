# importando a biblioteca necessária..
import sqlite3 as sq

try:
    # Conexão com o Banco de Dados. (foi usado o caminho exato pois sempre que eu tento inserir somente o nome do DataBase, ocorre um erro.)
    conn = sq.connect('database.db')

    # Cursor
    cursor = conn.cursor()

    # Criando a tabela e etc..
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Alunos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Nome TEXT NOT NULL,
    Idade INTEGER NOT NULL,
    Turma INTEGER NOT NULL,
    Nota_Final REAL NOT NULL
    );                
    """)

except Exception as erro:
    # se ocorrer um erro, irá mostrar uma mensagem juntamente com o erro.
    print(f'\033[31mOcorreu um erro inesperado..\n\nERRO: {erro}.\033[m')

else:
    # se a conexão for bem sucedida, irá mostrar uma mensagem.
    print(' ','-'*42,'\n  \033[1;32mConectado com sucesso ao Banco de Dados.\033[m\n','-'*42)