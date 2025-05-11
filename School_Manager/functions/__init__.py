# importando a biblioteca necessária.
import db_connection as db
from time import sleep
import os
import platform

# função para decoração..
def novaLinha():
    sleep(3)
    # o Windows tem um método diferente dos outros sistemas operacionais para limpar o terminal.
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

# função para registro no Banco de Dados..
def registro(nome='teste',idade=0,turma='turma 72',nota_final=9.500):
    # criando a conexão..
    conn = db.conn

    # criando o cursor.
    cursor = db.conn.cursor()

    # AJUSTES -----------------------------------------------------------

    # ajustando a nota_final para ficar com só um número após o ponto.
    nota_final = float(f'{nota_final:.1f}')

    # --------------------------------------------------------------------

    try:
        # inserindo dados.
        cursor.execute("""
        INSERT INTO Alunos(Nome,Idade,Turma,Nota_Final) VALUES(?,?,?,?)
        """,(nome,idade,turma,nota_final))
        # obs: Sempre usar tuplas ao os inserir dados.
    except Exception as erro:
        print(f'\033[31mOcorreu um erro ao tentar registrar os dados.\n\nERRO: \033[1;31m{erro}\033[m')
    # Salvando os dados no Banco de Dados.
    else:
        # salvando as alterações..
        conn.commit()

    finally:

        # fechando o cursor..
        cursor.close()
        
        # fechando a conexão..
        conn.close()

# função para exibir uma mensagem na tela com o nome de todos os alunos salvos no Banco de Dados. (nesse eu tive auxílio, pois não conseguia exibir a mensagem sem os (' ',) )  
def listarAlunos():
    # criando o cursor..
    cursor = db.conn.cursor()

    # pegando os dados da coluna "Id" e "Nome" do Banco de Dados. (não sabia que podia salvar 2 dados de 2 colunas em uma mesma tupla kkj)
    cursor.execute('''
    SELECT id,Nome,Idade,Nota_Final FROM Alunos
    ''')

    # guardando os dados em uma tupla.
    alunos = cursor.fetchall()
    
    # mensagem que será colocada acima da lista (somente um design.)
    mensagem_acima = "\033[3;36mLISTA DE ALUNOS REGISTRADOS\033[m"

    # para ficar mais visível ao usuário.
    novaLinha()

    # Mostrando a mensagem na tela.
    print(f'{mensagem_acima:-^80}')
    # só pra dar espaço mesmo.
    print()
    # pega separadamente o id e nome, sem isso seria "aluno[0]" e "aluno[1]".
    for aluno_id, aluno_nome, aluno_idade, aluno_notafinal in alunos:
        # mostra a mensagem.
        print(f'ID: \033[3;34m{aluno_id:<5}\033[m Nome: \033[3;34m{aluno_nome:<20}\033[m Idade: \033[3;34m{aluno_idade:<5}\033[m Nota Final: \033[3;34m{aluno_notafinal:<10}\033[m')
    print()
    print('-' * 70)
    input('Pressione Enter para continuar: ')
    novaLinha()

    # fechando o cursor..
    cursor.close()
        
    # fechando a conexão..
    db.conn.close()

# função para remover um Aluno por Id.
def deletarAluno(mensagem='Digite o id: '):

# CONTINUAR -------------------------------------------------
    try:
        
        id = int(input(mensagem))

        # criando o cursor..
        cursor = db.conn.cursor()

        # recebendo o Id máximo do Database.
        cursor.execute("""
SELECT Id FROM Alunos;
""")

        # pega todos os ids por linha. row é linha em inglês.
        IDS = [row[0] for row in cursor.fetchall()]

        # verifica se o id está nos IDs registrados.
        if id in IDS:
            cursor.execute('DELETE FROM Alunos WHERE id = ?', (id,))
            db.conn.commit()
            cursor.close()  # Ensure the cursor is closed after committing changes
        else:
            while id not in IDS:
                try:
                    id = int(input('\033[31mERRO! o id digitado não está registrado.\033[33m\n\nDigite novamente: \033[m'))
                except ValueError:
                    print('\033[31mERRO! Digite um número válido.\033[m')
                    return

    except Exception as erro:
        print(f'\033[31mHouve um erro inesperado no processo..\n\nerro: \033[1;31m{erro}.\033[m')
    
    else:
        # verificação se o Id máximo corresponde ao id pego.


        # mensagem..
        print('\033[32m\nAluno Removido com sucesso do Banco de Dados!\033[m')

        input('Pressione Enter para continuar: ')

        # salvando as alterações..
        db.conn.commit()
    
    finally:

        # fechando o cursor..
        cursor.close()
        
        # fechando a conexão..
        db.conn.close()

        novaLinha()

def atualizarAluno(CEN='name.',id=1):
    # a lista de modificações são:
    # name.NOMENOVO, years.IDADENOVA, class.TURMANOVA, finalnote.NOTAFINALNOVA
    tabela = ['Nome','Idade','Turma','Nota_Final']

    try:
        #pegando o cursor..
        cursor = db.conn.cursor()
    except Exception as erro:
        print(f'\033[31mOcorreu um erro inesperado..\n\nERRO: \033[1;31m{erro}\033[m')
        novaLinha

    MOD = CEN.split('.')[-1] # separa pelo ponto e pega a última string da lista, no caso o comando.

    VARIABLE =  CEN.split('.')[0] # separa pelo ponto e pega o primeiro string da lista, no caso o dado que vai ser modificado.

    if VARIABLE in tabela:
        cursor.execute(f'''
    UPDATE Alunos SET {VARIABLE} = ? WHERE id = ?
    ''',(MOD,id))
        # salvando.
        db.conn.commit()
        print('\033[32m\nAluno atualizado com sucesso!')
        input('\n\nPressione Enter para continuar: ')
    else:
        while VARIABLE not in tabela:
            VARIABLE = str(input('\033[31mERRO! digite uma coluna do DataBase válido!\n\n\033[33mDigite: \033[m'))
    # fechando o cursor..
    cursor.close()
        
    # fechando a conexão..
    db.conn.close()

# função para registrar um aluno com validações e loopings corrigidos.
def registrarAlunoM():
    while True:
        novaLinha()
        # pega o nome e cria um novo texto
        nome = str(input('\033[33mNome do Aluno: ')).strip().title()
        try:
            # tenta pegar a idade
            idade = int(input('\033[33mIdade do Aluno: '))
        except ValueError:
            # se der erro, vai iniciar um looping até dar certo.
            print('\033[1;31mERRO! escreva novamente.\033[m')
            continue
        else:
            # ajuste para a idade não ser salva como negativa.
            if idade <= 0:
                print('\033[31mERRO! a idade não pode ser negativa ou igual a 0, tente novamente.\033[m')
                continue
            turma = str(input('\033[33mTurma do Aluno: ')).strip()
            try:
                # tenta pegar a nota final.
                nota_final = float(input('\033[33mNota Final do Aluno: '))
            except ValueError:
                # se der erro, vai iniciar um looping até dar certo.
                print('\033[1;31mERRO! escreva novamente.\033[m')
                continue
            else:
                if nota_final > 10 or nota_final < 0:
                    print('\033[1;31mERRO! a nota não pode ser maior que 10 ou menor que 0.\033[m')
                    continue
                sleep(1)
                # usa a função de registro para inserir no Banco de Dados.
                registro(nome=nome, idade=idade, turma=turma, nota_final=nota_final)
                print('\033[1;32mAluno registrado com sucesso!\033[m')
                # para deixar quanto tempo quiser na tela, usei o input.
                input('Pressione Enter para continuar: ')
                novaLinha()
                break

# função para modificar dados de um aluno com validações e loopings corrigidos.
def modificarAlunoM():
    while True:
        try:
            # Menu de opções..
            novaLinha()
            # pegando o id que o usuário escolheu
            idAluno = int(input('\033[33mInsira o id do Aluno: \033[m'))

            # cursor:
            cursor = db.conn.cursor()

            # pegando os dados
            cursor.execute('SELECT id FROM Alunos')

            # lista
            ids = [linha[0] for linha in cursor.fetchall()]

            # condição pra saber se o id está realmente nos ids do Banco de Dados.
            if idAluno in ids:
                menuMod = int(input('''
\033[3;35m<< SELECIONE O DADO QUE DESEJA MODIFICAR. >>\033[m
\033[34m------------------------------------------------                                    
[1] Nome
[2] Idade
[3] Turma
[4] Nota Final                                  
------------------------------------------------\033[m
\033[32mDigite a opção: \033[m'''))

                if menuMod == 1:
                    nome = str(input('\033[33mDigite o novo nome do Aluno: \033[m')).title().strip()
                    atualizarAluno(CEN=f'Nome.{nome}', id=idAluno)
                elif menuMod == 2:
                    while True:
                        try:
                            # tenta pegar a idade
                            idade = int(input('\033[33mDigite a nova idade do Aluno: \033[m'))
                            if idade <= 0:
                                print('\033[31mERRO! a idade não pode ser negativa ou igual a 0, tente novamente.\033[m')
                                continue
                            atualizarAluno(CEN=f'Idade.{idade}', id=idAluno)
                            break
                        except ValueError:
                            print('\033[1;31mERRO! escreva novamente.\033[m')
                            continue

                elif menuMod == 3:
                    turma = str(input('\033[33mDigite a turma nova do Aluno: \033[m'))
                    atualizarAluno(CEN=f'Turma.{turma}', id=idAluno)

                elif menuMod == 4:
                    while True:
                        try:
                            # tenta pegar a nota final.
                            nota_final = float(input('\033[33mNota Final do Aluno: \033[m'))
                            if nota_final > 10 or nota_final < 0:
                                print('\033[1;31mERRO! a nota não pode ser maior que 10 ou menor que 0.\033[m')
                                continue
                            atualizarAluno(CEN=f'Nota_Final.{nota_final}', id=idAluno)
                            break
                        except ValueError:
                            print('\033[1;31mERRO! escreva novamente.\033[m')
                            continue
                break
            else:
                print('\033[31mERRO! O ID informado não está registrado.\033[m')
                novaLinha()
                continue

        except Exception as erro:
            print(f'\033[31mERRO! {erro}\033[m')
            novaLinha()
            continue


# menu para o usuário escolher o que deseja fazer.. 
def menu():
    
    # looping.. -----------------------------
    while True:
        # criando o texto..--------------------------------------------
        print('''\033[3;33m<<< Bem vindo ao School Manager. >>>\033[m
\033[3;35m<<< Made by Arthur Eduardo. >>>\033[m
\033[1;34m-------------------------------------------------
Escolha uma das opções abaixo:
\033[1;34m
[1] Registrar Aluno
[2] Listar Alunos
[3] Remover Aluno
[4] Atualizar Aluno
[5] Sair do programa
-------------------------------------------------\033[m''')
        
        # pegando a escolha do usuário..
        try:
            opcao = int(input('\033[32mDigite: \033[m'))
        except:
            print('\033[1;31mERRO! escreva novamente.\033[m')
            novaLinha()
            continue
        

        # condições.. -------------------------------------------------

        # verificação se o número está entre as opções.
        if 1 <= opcao <= 5:

            # Cadastro/Registro do Aluno ---------------------
            if opcao == 1:
                # função de menu pra registro.
                registrarAlunoM()
                        
            # listar os alunos -------------------------------
            elif opcao == 2:
                # usa a função de listar alunos.
                listarAlunos()

            elif opcao == 3:
                novaLinha()
                # pegando o id que o usuário quer remover+informação para saber o id..
                deletarAluno('\033[33mDigite o ID do Aluno: \033[m')

            elif opcao == 4:
                modificarAlunoM()


            elif opcao == 5:
                novaLinha()
                print('\033[3;34mAté mais!\033[m')
                db.conn.close()
                exit()
       # se o número da opção for fora das escolhas..                 
        else:
            print('\033[1;31mERRO! Número fora das escolhas, tente novamente!\033[m')
            novaLinha()
            sleep(2)
            continue