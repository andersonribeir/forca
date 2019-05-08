import random
import socket
import time
import threading

host = socket.gethostname()
port = 9999
chutes = 1
palavra_sorteada = ""
i = 0

def resgatar(): #FUNÇÃO PARA RESGATAR AS PALAVRAS DO ARQUIVO DE TEXTO
    arqpt = open("palavras.txt", "r")  # abrindo o arquivo a ser lido
    p = arqpt.read().split()  # ao ler o arquivo, as palavras são armazenadas nessa variavel
    arqpt.close()
    return p

def sortear(): #FUNÇÃO PARA ESCOLHER ALEATORIAMENTE, USANDO A BIBLIOTECA "RANDOM"
    palavras = resgatar()
    palavra_sorteada = random.choice(palavras)
    tamanho = len(palavra_sorteada)
    print("A palavra sorteada foi: {}" .format(palavra_sorteada))
    return tamanho, palavra_sorteada


def checar_palavra(palavra, con, palavras_secret): #FUNÇÃO PARA COMPARAR A PALAVRA RECEBIDA COM A SORTEADA
    palavra_sorteada = palavras_secret
    if palavra == palavra_sorteada:
        ganha = "acertou a palavra"
        print(ganha)
        ganha = str(ganha).encode("utf8")
        con.send(ganha)
        palavra_sorteada = str(palavra_sorteada).encode("utf8")
        con.send(palavra_sorteada)
    else:
        perde = "Errou! A palavra era: %s" %palavra_sorteada
        print(perde)
        perde = str(perde).encode("utf8")
        con.send(perde)
        palavra_sorteada = str(palavra_sorteada).encode("utf8")
        con.send(palavra_sorteada)


def checar_chute(letra, con, palavra_secret, letras_chutadas, erros, acertos): #FUNÇÃO PARA COMPARAR A LETRA RECEBIDA COM A ENVIADA
    palavra_sorteada = palavra_secret
    if letra not in letras_chutadas:
        letras_chutadas.append(letra)
        letra_correta = False
        for i in range(0, len(palavra_sorteada)):
            if (letra == palavra_sorteada[i]):
                letra_correta = True
                acertos[i] = letra
        if (letra_correta):
            print(acertos)
        else:
            erros = int(erros) + 1
    else:
        erros = int(erros) + 1
    erros = str(erros)
    err = erros.encode("utf8")
    con.send(err)
    return erros


def fazer_jogo(con, letras_chutadas, erros, acertos):#DÁ INICIO AO JOGO
    del acertos[:]#ZERA OS VETORES
    del letras_chutadas[:]
    tamanho, palavra_sorteada = sortear()
    for x in range(0, tamanho):
        acertos.append("-")
    comp = str(tamanho).encode("utf8")
    con.send(comp)
    while True:
        op2 = con.recv(1204)
        op2 = op2.decode("utf8")

        if op2 == "1":
            rcv_chute = con.recv(1204)
            rcv_chute = rcv_chute.decode("utf8")
            print(rcv_chute)
            erros = checar_chute(rcv_chute, con, palavra_sorteada,letras_chutadas, erros, acertos)
            teste = str(acertos).encode("utf8")
            con.send(teste)
            if erros == "6":
                break
        elif op2 == "2":
            rcv_palavra = con.recv(1204)
            rcv_palavra = rcv_palavra.decode("utf8")
            checar_palavra(rcv_palavra, con, palavra_sorteada)
            break


def handle_client(con, addr):
    letras_chutadas = []
    erros = 0
    acertos = []
    while True:
        op = con.recv(1024)
        op = op.decode("utf8")
        if op == "1":
            fazer_jogo(con, letras_chutadas, erros, acertos)



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(10)

while True:
    con, addr = s.accept()
    t = threading.Thread(target=handle_client, args=(con, addr))
    t.start()

