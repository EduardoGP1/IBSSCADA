#_____________________BIBLIOTECAS__________________________
from tkinter import *
from tkinter import messagebox
from datetime import datetime #importante para colocar datas nos registros
import mysql.connector
from mysql.connector import Error
from tkinter import ttk
import serial
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
#___________________________________________________________

'''________________________OBJETIVOS________________________
-Pode criar um contador de erros de senha por usuário
-Consertar botão de "deslogar" para "destruir" componentes ativos.
-Arrumas menu cascade em menubar
-Colocar scrollbar dentro da treeview, consertar ordens dos comandos
-Criar gráfico a partir do banco de dados da temperatura
_________________________________________________________'''
x_da_janela = 0
y_da_janela = 0
largura = 1063
altura = 385

def abrir_conexao():
    global conexao
    conexao = mysql.connector.connect( #gera os dados para poder conectar
    host = 'localhost',
    user = 'root',
    password = '@dmin123',
    database = 'ibsystemssoftware')


def funcao_login():
    global tela,login_usuario, login_senha, hoje, hoje_date, hoje_hour, hoje_minute
    login_usuario = str(entry_usuario.get())
    login_senha = str(entry_senha.get())
    if login_usuario=='' and login_senha=='':
        tela = 1
        hoje = datetime.now()
        hoje_date = hoje.date()
        hoje_hour = hoje.hour
        hoje_minute = hoje.minute
        abrir_conexao()
        cursor = conexao.cursor() #inicio do processo de envio de dados para o BD
        comando = f'INSERT INTO auditoria (tipo, quem, quando) VALUES ' \
                  f'("Login","{login_usuario}", "{hoje}")'
        cursor.execute(comando)
        conexao.commit()
        cursor.close() #fim do processo de envio de info para o BD
        conexao.close()
        tela_principal()
    else:
        messagebox.showerror('ERRO', 'Usuário ou senha incorretos!')
    return x_da_janela, y_da_janela

def tela_login():
    global x_da_janela, y_da_janela, entry_senha, entry_usuario, frame_login,bg, largura, altura
    x_da_janela = 0
    y_da_janela = 0
    janela.title('IBSYSTEMS SOFTWARE') #muda título
    janela.geometry('1063x385')

    frame_login = Frame(janela, bg='#000000')
    frame_login.place(x=0, width=1063, height=385)
    janela.configure(menu='')

    bg = PhotoImage(file='tela_login.png')
    Label(frame_login, image=bg).place(x=-2, y=-2)
    entry_usuario = Entry(frame_login, show='*')
    entry_senha = Entry(frame_login, show='*')

    entry_usuario.place(x=710, y=141)
    entry_senha.place(x=710, y=176)

    Button(frame_login,text='  Login  ', command=funcao_login).place(x=745, y=206)

def destroi_principal():
    painel_arvore.place_forget()
    left.place_forget()
    painel_principal.place_forget()
    print ('tela principal destruida')
    tela_login()
def semcomando():
    print ('sem comando')

def tela_principal():
    global painel_arvore, left, painel_principal
    janela.title(f'IBSYSTEMS SOFTWARE - {login_usuario} logado {hoje_date} às {hoje_hour}:{hoje_minute}') #muda título
    frame_login.place_forget()
    janela.resizable(1, 1)


    painel_arvore = PanedWindow()  
    painel_arvore.pack(fill = BOTH, expand = 1)
    left = Frame(painel_arvore, bg='#ffffff', bd='30', width=150)
    painel_arvore.add(left)
    painel_principal = Frame(painel_arvore, width=100, bg='#888888')
    painel_arvore.add(painel_principal)


    principal = Menu(janela)
    submenu_visualizar = Menu(principal)
    principal.add_command(label='Arquivos', command=semcomando)
    principal.add_command(label='Editar', command=semcomando)
    principal.add_cascade(label='Visualizar', menu=submenu_visualizar)
    principal.add_command(label='Ação', command=semcomando)
    principal.add_command(label='Inserir', command=semcomando)
    principal.add_command(label='Ferramentas', command=semcomando)
    principal.add_command(label='Consultas', command=semcomando)
    principal.add_command(label="Ajuda", command=semcomando)
    principal.add_separator()
    principal.add_command(label="DESLOGAR", command=destroi_principal)

    submenu_visualizar.add_command(label='Auditoria', command=auditoria)
    submenu_visualizar.add_command(label='Temp_amb_automacao', command=temp_amb_automacao)

    principal.add_cascade(menu=submenu_visualizar)
    janela.configure(menu=principal)

    Label(painel_principal, text='PROCURADORIA REGIONAL DA REPÚBLICA\n4° REGIÃO', font=('ARIAL', 20)).pack(side=TOP, pady=(20, 25))
    Button(painel_principal, text='ACESSO', command=semcomando, width=30, height=2).pack(side=TOP, pady=(0, 5))
    Button(painel_principal, text='AR CONDICIONADO', command=sala_automacao, width=30, height=2).pack(side=TOP, pady=(0,5))
    Button(painel_principal, text='ELÉTRICA', command=semcomando, width=30, height=2).pack(side=TOP, pady=(0,5))
    Button(painel_principal, text='HIDRÁULICA', command=semcomando, width=30, height=2).pack(side=TOP, pady=(0,5))
    Button(painel_principal, text='SDAI', command=semcomando, width=30, height=2).pack(side=TOP, pady=(0,5))

    x_da_janela = 1
    y_da_janela = 1
    return x_da_janela, y_da_janela

def atualiza_temp():
    try:
        arduino = serial.Serial('COM4', 9600)
        ard = arduino.read(5)
        print("temperatura é ", ard)
        arduino.close()
        my_str.set(ard)
    except:
        messagebox.showwarning('ERRO', 'Falha na conexão com arduino!')
        print('Falha na conexão com arduino')

def read_data(WordUsed):
    for row in c.execute(sql):
        x.append(conversor(row[0]))
        y.append(row[1])


def plotar_trend():
    try:
        abrir_conexao()
        cursor = conexao.cursor()
        cursor.execute("select temperatura from temp_amb_automacao")
        arry = cursor.fetchall()
        print (arry)
        lista = [i[0] for i in arry]
        lista_temp = []
        for i in range(len(lista)):
            lista_temp.append(float(lista[i]))
        print (lista_temp)

        cursor.execute("select data from temp_amb_automacao")
        arry = cursor.fetchall()
        print(arry)
        lista_data = [i[0] for i in arry]

    except:
        print('deu merda')
    finally:
        if (conexao.is_connected()):
            conexao.close()
            cursor.close()
            print('Conexão SQL encerrada')

    plt.rcParams['figure.figsize'] = (11, 7)  # pre-determina tamanho da janela do gráfico
    plt.title('Trend Temperatura Sala Automação')
    plt.xlabel('Data')  # Dá nome ao eixo X
    plt.ylabel('Temperatura')  # Dá nome ao eixo Y
    plt.scatter(lista_data, lista_temp, color='red')  # Coloca marcações bolinhas vermelhas nos pontos'''
    plt.plot(lista_data, lista_temp, label='Valores', linewidth=2)
    plt.show()



def sala_automacao():
    global my_str

    painel_arvore.remove(painel_principal)
    frame_sala_automacao = Frame(painel_arvore, bg='#dddddd')
    painel_arvore.add(frame_sala_automacao)

    my_str = StringVar()
    l2 = Label(frame_sala_automacao, textvariable=my_str, width=10)
    l2.pack(side=TOP, ipady=10, pady=(100, 0))
    atualiza_temp()

    b1 = Button(frame_sala_automacao, text='Trend', command=plotar_trend)
    b1.pack(side=TOP)
    b2 = Button(frame_sala_automacao, text='ATUALIZAR TELA', width=15, command=atualiza_temp)
    b2.pack(side=TOP, ipady=10, pady=10)

def temp_amb_automacao():
    painel_arvore.remove(painel_principal)
    frame_temp_amb_automacao = Frame(painel_arvore, bg='#dddddd')
    painel_arvore.add(frame_temp_amb_automacao)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Treeview',
                    background='#d3d3d3',
                    foreground='black',
                    rowheight=25,
                    fielbackground='#d3d3d3')
    style.configure('Treeview.Heading', font=('Verdana', 10, 'bold'),
                    foreground='#444', background='silver')
    style.map('Treeview',
              bg=[('selected', '#347083')])

    tree_scroll = ttk.Scrollbar(frame_temp_amb_automacao, orient="vertical")
    tree_scroll.pack(side=RIGHT, fill=Y)

    auditoria_treeview = ttk.Treeview(frame_temp_amb_automacao,
                                      columns=("a", "data", "temperatura", "b"),
                                      show="headings",
                                      yscrollcommand=tree_scroll.set,
                                      selectmode='browse')
    auditoria_treeview.pack(ipadx=150, ipady=50)
    auditoria_treeview.column("a", min=20, width=20)
    auditoria_treeview.column('data', minwidth=20, width=50, anchor=CENTER)
    auditoria_treeview.column('temperatura', minwidth=20, width=50, anchor=CENTER)
    auditoria_treeview.column("b", minwidth=20, width=400)
    auditoria_treeview.heading('data', text='Data')
    auditoria_treeview.heading('temperatura', text='Temperatura')

    tree_scroll.config(command=auditoria_treeview.yview)

    try:
        abrir_conexao()
        cursor = conexao.cursor()
        cursor.execute("select * from temp_amb_automacao")
        temp_amb_automacao_sql = cursor.fetchall()
        print('número total de linhas', cursor.rowcount)
        print(temp_amb_automacao_sql)
    except Error as e:
        print('Erro ao acessar SQL', e)
    finally:
        if (conexao.is_connected()):
            conexao.close()
            cursor.close()
            print('Conexão SQL encerrada')

    auditoria_treeview.tag_configure('branco', foreground='black', background='white')
    auditoria_treeview.tag_configure('azul', background='#ffffff')

    global count
    count = 0
    for (dt, temp) in temp_amb_automacao_sql:
        if count % 2 == 0:
            auditoria_treeview.insert("", index="end",
                                      values=("", dt, temp, ""), tags=('branco'))
        else:
            auditoria_treeview.insert("", index="end",
                                      values=("", dt, temp, ""), tags=('azul'))
        count += 1

def auditoria():
    painel_arvore.remove(painel_principal)
    frame_auditoria = Frame(painel_arvore, bg='#dddddd')
    painel_arvore.add(frame_auditoria)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Treeview',
                    background='#d3d3d3',
                    foreground='black',
                    rowheight=25,
                    fielbackground='#d3d3d3')
    style.configure('Treeview.Heading', font=('Verdana', 10, 'bold'),
                    foreground='#444', background='silver')
    style.map('Treeview',
              bg=[('selected', '#347083')])

    tree_scroll = ttk.Scrollbar(frame_auditoria, orient="vertical")
    tree_scroll.pack(side=RIGHT, fill=Y)

    auditoria_treeview = ttk.Treeview(frame_auditoria,
                                      columns=("a", "tipo", "quem", "quando", "b"),
                                      show="headings",
                                      yscrollcommand=tree_scroll.set,
                                      selectmode='browse')
    auditoria_treeview.pack(ipadx=150, ipady=50)
    auditoria_treeview.column("a", min=20, width=20)
    auditoria_treeview.column('tipo', minwidth=20, width=50, anchor=CENTER)
    auditoria_treeview.column('quem', minwidth=20, width=50, anchor=CENTER)
    auditoria_treeview.column('quando', minwidth=20, width=150, anchor=CENTER)
    auditoria_treeview.column("b", minwidth=20, width=400)
    auditoria_treeview.heading('tipo', text='Tipo')
    auditoria_treeview.heading('quem', text='Quem')
    auditoria_treeview.heading('quando', text='Quando')

    tree_scroll.config(command=auditoria_treeview.yview)

    try:
        conexao = mysql.connector.connect(  # gera os dados para poder conectar
            host='localhost',
            user='root',
            password='@dminPRR4',
            database='ibsystemssoftware'
        )
        cursor = conexao.cursor()
        cursor.execute("select * from auditoria")
        auditoria_sql = cursor.fetchall()
        print('número total de linhas', cursor.rowcount)
        print (auditoria_sql)
    except Error as e:
        print('Erro ao acessar SQL', e)
    finally:
        if (conexao.is_connected()):
            conexao.close()
            cursor.close()
            print ('Conexão SQL encerrada')

    auditoria_treeview.tag_configure('branco', foreground='black', background='white')
    auditoria_treeview.tag_configure('azul', background='#ffffff')

    global count
    count = 0
    auditoria_treeview.insert("", "end", values=("", "opa", "ola", "eai", ""),
                              tags=("azul",))
    for (t, qm, qd) in auditoria_sql:  # t=tipo, qm=quem, qd=quando para receber da lista auditoria_sql
        if count %2 == 0:
            auditoria_treeview.insert("", index="end",
                                      values=("",t,qm,qd,""), tags=('branco'))
        else:
            auditoria_treeview.insert("", index="end",
                                      values=("", t, qm, qd, ""), tags=('azul'))
        count += 1



janela = Tk() #cria janela
janela.iconbitmap('logoIbsystems.ico') #muda ícone
janela.geometry('1063x385') #define tamanho da janela quando abre
janela.resizable(width=x_da_janela, height=y_da_janela)  # proibe mexer na largura da janela

tela_login()

janela.mainloop()