import tkinter as tk
import serial
from datetime import datetime
import time
import mysql.connector
from mysql.connector import Error
import keyboard as kb


def atualiza_temp():
    global ard
    arduino = serial.Serial('COM4', 9600)
    ard = str(arduino.read(5))
    ard = ard[2:7]
    print("temperatura é ", ard)
    arduino.close()

def abrir_conexao():
    global conexao
    conexao = mysql.connector.connect( #gera os dados para poder conectar
    host = 'localhost',
    user = 'root',
    password = '@dmin123',
    database = 'ibsystemssoftware')
    print('conexão criada')

while kb.is_pressed('f')!=1:
    try:
        abrir_conexao()

        cursor = conexao.cursor()
        atualiza_temp()
        hoje = str(datetime.now())
        hoje = hoje[0:19]
        print (hoje)
        inserir_dados = f'INSERT INTO temp_amb_automacao (data, temperatura) VALUES ("{hoje}", "{ard}")'
        cursor.execute(inserir_dados)
        conexao.commit()
        cursor.close() #fim do processo de envio de info para o BD
        conexao.close()
    #except error as erro: como descobrir o tipo de erro?
        #print(erro)

    finally:
        time.sleep(10)