from tkinter import *
import tkinter
import tkinter as tk


import socket
host = socket.gethostname()
port = 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

i = 1
def play(): #FUNÇÃO QUE DÁ INICIO O JOGO PARA O CLIENTE

    def letra(): #RECEBE A LETRA DIGITADA PELO CLIENTE E ENVIA PARA O SERVIDOR
        if len(entrada.get())>1:
            erro = Tk()
            erro.geometry("180x100+200+200")
            erro.title("ERRO")
            msgerro = Label(erro, text = "Insira a letra")
            msgerro.place(x = "50", y = "50")
        else:
            op = str(1).encode("utf8")
            s.send(op)

            pegaletra = str(entrada.get()).lower().strip().encode("utf8")
            s.send(pegaletra)

            entrada.delete(0, END)

            msg = s.recv(1024).decode("utf8")

            forca = s.recv(1024)
            forca = forca.decode("utf8")
            lblforca["text"] = forca

            if msg == "0":
                lblmsg["image"] = erro0
            elif msg == "1":
                lblmsg["image"] = erro1
            elif msg == "2":
                lblmsg["image"] = erro2
            elif msg == "3":
                 lblmsg["image"] = erro3
            elif msg == "4":
                lblmsg["image"] = erro4
            elif msg == "5":
                lblmsg["image"] = erro5
            elif msg == "6":
                lblmsg["image"] = erro6
                btnpalavra.place(x="160", y="215")
                btnreinicia = Button(janela2, text="Reiniciar jogada", command=playagain)
                btnreinicia.place(x="260", y="215")


    def palavra(): #RECEBE A LETRA DIGITADA PELO CLIENTE E ENVIA PARA O SERVIDOR
        if len(entrada.get())<=1:
            erro = Tk()
            erro.geometry("180x100+200+200")
            erro.title("ERRO")
            msgerro = Label(erro, text = "Insira a palavra")
            msgerro.place(x = "50", y = "50")

        else:
            op = str(2).encode("utf8")
            s.send(op)
            pegapalavra = str(entrada.get()).lower().strip().encode("utf8")
            if pegapalavra.isalpha():
                s.send(pegapalavra)

                entrada.delete(0, END)

                msg = s.recv(1024).decode("utf8")
                forca = s.recv(1024).decode("utf8")
                if msg == "acertou a palavra":
                    lblforca["text"] = "Acertou a palavra era: %s" % forca
                elif "Errou" in msg:

                    lblmsg["image"] = erro6
                    lblforca["text"] = "Errou! A palavra era: %s" %forca

                lblforca.place(x="180", y="150")
                btnpalavra.place(x="155", y="215")

                btnreinicia = Button(janela2, text="Reiniciar jogada", command=playagain)
                btnreinicia.place(x="255", y="215")

            else:
                erro = Tk()
                erro.geometry("180x100+200+200")
                erro.title("ERRO")
                msgerro = Label(erro, text="Insira apenas palavra")
                msgerro.place(x="50", y="50")

    def playagain(): #REINICIA A JOGADA
        op = str(1).encode("utf8")
        s.send(op)

        rcv = s.recv(1024)
        rcv = rcv.decode("utf8")
        lblforca["text"] = "A palavra tem %s letras" %rcv
        lblmsg["image"] = erro0


    janela2 = Tk()
    janela2.geometry("500x335+200+200")
    janela2.title("Enforcado")
    erro0 = PhotoImage(file="erro0.png")
    erro1 = PhotoImage(file="errofinal-5.png")
    erro2 = PhotoImage(file="errofinal-4.png")
    erro3 = PhotoImage(file="errofinal-3.png")
    erro4 = PhotoImage(file="errofinal-2.png")
    erro5 = PhotoImage(file="errofinal-1.png")
    erro6 = PhotoImage(file="errofinal.png")

    lblmsg = Label(janela2, text="mensagem")
    lblmsg.place(x="-3", y="0")
    lblmsg["image"] = erro0
    entrada = Entry(janela2, text="")
    entrada.place(x="160", y="190")
    lblforca = Label(janela2, text = "forca aqui")
    lblforca.place(x = "195", y = "140")


    btnletra = Button(janela2, text = "Chutar letra", command = letra)
    btnletra.place(x = "290", y = "187")
    btnpalavra = Button(janela2, text="Chutar palavra", command = palavra)
    btnpalavra.place(x="190", y="215")

    op = str(1).encode("utf8")
    s.send(op)

    r = s.recv(1024)
    r = r.decode("utf8")

    lblforca["text"] = "A palavra tem %s letras" %r
    lblforca["bg"] = "#d4d4d4"

    janela2.mainloop()


def mudajanela(): #TRANSIÇÃO
    janela.destroy()
    play()


def howtoplay():

    janela2 = Tk()
    janela2.geometry("500x350+200+200")
    janela2.title("Enforcado")
    janela2["bg"] = "DARKRED"
    btn = Label(janela2, text="O jogo da forca consiste no chute de letras\n"
                              "para a construção de uma palavra específica.\n"
                              "Caso a letra escolhida não esteja contida na palavra,\n"
                              "será acarretado no enforcamento de um boneco imaginário")
    btn["font"] = "Constantia"
    btn["bg"] = "DARKRED"
    btn["fg"] = "WHITE"
    btn.place(x="35", y="130")
    def voltarmain():
        janela2.destroy()


    btnvoltar = Button(janela2,text="Sair" ,width = "3",command = voltarmain)
    btnvoltar["bg"] = "DARKRED"
    btnvoltar.place(x="-1", y="5")
    btnvoltar["fg"] = "WHITE"
    btnvoltar["border"] = 1
    janela2.mainloop()



janela = Tk()
janela.geometry("500x340+200+200")
janela.title("Enforcado")
main = PhotoImage(file="main.png")
lblmain = Label(janela)
lblmain.place(x="-3",y="-2")
lblmain["image"] = main
lblenfor = Label(janela,text = "ENFORCADO")
lblenfor.place(x="90",y="15")
lblenfor["font"] = "Constantia" , 40
lblenfor["fg"] = "WHITE"
lblenfor["bg"] = "DARKRED"

btn = Button(janela, text = "START", command = mudajanela)
btn.place(x = "240", y = "130")
btn["fg"] = "DARKRED"
btnsobre = Button(janela, text = "Como jogar?",command = howtoplay)
btnsobre.place(x = "220", y = "165")
btnsobre["fg"]="DARKRED"


janela.mainloop()