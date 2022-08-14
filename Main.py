import os
import mysql.connector
from time import sleep

TF = False
Sysinit = False

MSGid = 0
User = str()

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password=r'Senha',
    database='message_db'
)
cursor = connection.cursor()

print('[Fundacao_Crypto] - [Data_Manager]\n')
sleep(1.5)
SN = str(input('[S/N] Ja possui uma conta: ')).upper()

if SN == 'S':
    Sysinit = True
    os.system('cls')

    print('Identifique-se')
    sleep(1)
    User = str(input('Digite o seu usuario: '))
    Pass = str(input('Digite a sua senha: '))
    Login = f'{User} {Pass}'

    cursor.execute('SELECT * FROM users')

    for L in cursor.fetchall():
        Logs = f'{L[1]} {L[2]}'

        if Logs == Login:
            print('[Processo de Login feito com sucesso]')
            TF = True
            break
    
    if TF == False:
        print('[*Usuario nao identificado*]')
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
            exit()
    
    IDs += 1
    cursor.execute(f'INSERT INTO users (idusers, username, password) VALUES ({IDs}, "{User}", "{Pass}")')
    connection.commit()

os.system('cls')
if not Sysinit: exit()

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
if not Option: exit()

if Option == 1:
    NewPass = str(input('Digite sua nova senha: '))

    cursor.execute(f'UPDATE users SET password = "{NewPass}" WHERE username = "{User}"')
    connection.commit()

    print('[Senha alterada]')

if Option == 2:
    cursor.execute(f'DELETE FROM users WHERE username = "{User}"')
    connection.commit()

    print('[Usuario deletado]')

if Option == 3:
    while True:
        os.system('cls')

        cursor.execute('SELECT idmessage FROM message')
        fetch = cursor.fetchall()
        lenIDS = len(fetch)

        if lenIDS <= 0:
            MSGid += 1
            print('Sistema: [Nao a conversas armazenadas]')

        else:
            cursor.execute('SELECT * FROM message')

            for msg in cursor.fetchall():
                MSGid += 1

                if lenIDS > 10:
                    lenIDS -= 1
                    continue
                
                if lenIDS <= 10:
                    print(f'{MSGid} {msg[1]}: {msg[2]}')
            MSGid += 1

        Message = str(input('\n[Exit para sair] Digite uma mensagem: '))

        if Message.upper() == 'EXIT': break

        if Message or Message != '':
            cursor.execute(f'INSERT INTO message (idmessage, user, msg) VALUES ({MSGid}, "{User}", "{Message}")')
            connection.commit()
            MSGid = 0

cursor.close()
connection.close()