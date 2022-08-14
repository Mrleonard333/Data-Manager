import os
import mysql.connector
from time import sleep

TF = False
Sysinit = False

MSGid = 0
User = str()

# v Inicia a conxão com o database
connection = mysql.connector.connect(
    host='Host',
    user='User',
    password=r'Senha',
    database='DataBase'
)
# v Ativa o cursor
cursor = connection.cursor()

print('[Fundacao_Crypto] - [Data_Manager]\n')
sleep(1.5)
SN = str(input('[S/N] Ja possui uma conta: ')).upper()

if SN == 'S':
    Sysinit = True
    os.system('cls') # < Vai apagar as mensagens anteriores no cmd

    print('Identifique-se')
    sleep(1)
    User = str(input('Digite o seu usuario: '))
    Pass = str(input('Digite a sua senha: '))
    Login = f'{User} {Pass}' # < Vai guardar o usuario ea senha na variavel [Login]

    cursor.execute('SELECT * FROM users') # < Vai pegar todas as informações da tabela

                # v Vai mostrar uma lista com as informações
    for L in cursor.fetchall():
        Logs = f'{L[1]} {L[2]}' # < Vai guardar o usuario ea senha da tabela

        if Logs == Login:
            print('[Processo de Login feito com sucesso]')
            TF = True
            break
    
    if TF == False:
        print('[*Usuario nao identificado*]')
        # v Encerra a conexão do DataBase e o cursor
        cursor.close()
        connection.close()
        exit()

if SN == 'N':
    Sysinit = True
    os.system('cls')

    print('Cadastre-se')
    sleep(1)
    User = str(input('Digite o seu usuario: '))
    Pass = str(input('Digite a sua senha: '))

    IDs = 0
    cursor.execute('SELECT * FROM users')

    for L in cursor.fetchall():
        IDs += 1
        if L[1] == User:
            print('[*Usuario ja existe*]')
            cursor.close()
            connection.close()
            exit() # < Vai encerrar o sistema
    
    IDs += 1
    # v Vai inserir o usuario ea senha na tabela de usuarios [users]
    cursor.execute(f'INSERT INTO users (idusers, username, password) VALUES ({IDs}, "{User}", "{Pass}")')
    connection.commit() # < Irá salvar as mudanças

os.system('cls')
if not Sysinit: exit() # < Se a variavel [System_Initiate] não conter o valor true o sistema não irá encerrar

print('Operacoes disponiveis\n')
sleep(1)
print('[1] Reescrever a senha')
sleep(0.5)
print('[2] Deletar o usuario')
sleep(0.5)
print('[3] Armazenar uma mensagem')
sleep(0.5)
print('[4] Terminate')
sleep(1)
Option = int(input('\nO que deseja fazer?: '))

os.system('cls')
if not Option: exit() # < Se a variavel [Option] for nula osistema irá iniciar

if Option == 1:
    NewPass = str(input('Digite sua nova senha: '))

    cursor.execute(f'UPDATE users SET password = "{NewPass}" WHERE username = "{User}"') # < Ira atualizar os dados do usuario
    connection.commit()

    print('[Senha alterada]')

if Option == 2:
    cursor.execute(f'DELETE FROM users WHERE username = "{User}"') # < Vai deletar o dado que tenha o seu usuario
    connection.commit()

    print('[Usuario deletado]')

if Option == 3:
    while True:
        os.system('cls')

        cursor.execute('SELECT idmessage FROM message') # < Irá criar uma lista com os IDs das mensagens guardadas
        fetch = cursor.fetchall()
        lenIDS = len(fetch)

        if lenIDS <= 0:
            MSGid += 1
            print('Sistema: [Nao a conversas armazenadas]')

        else:
            cursor.execute('SELECT * FROM message')

            for msg in cursor.fetchall():
                MSGid += 1
                
                # v vai mostrar apenas as dez ultimas mensagens
                if lenIDS > 10:
                    lenIDS -= 1
                    continue
                
                if lenIDS <= 10:
                    print(f'{msg[1]}: {msg[2]}')
            MSGid += 1

        Message = str(input('\n[Exit para sair] Digite uma mensagem: '))

        if Message.upper() == 'EXIT': break

        if Message or Message != '':
            cursor.execute(f'INSERT INTO message (idmessage, user, msg) VALUES ({MSGid}, "{User}", "{Message}")')
            connection.commit()
            MSGid = 0

cursor.close()
connection.close()
