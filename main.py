import requests
from random import choice
from colorama import Fore
import re
import sys
import time


cpf = {}
users = {}
url = "https://www.4devs.com.br/ferramentas_online.php"
estados = ["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", 
            "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE",
            "PI", "PR", "RJ", "RN", "RS", "RO", "RR", "SC",
            "SE", "SP", "TO"]


def arquivo():
    choice = str(input("\rDeseja salvar os dados gerados?(S/n) ")).lower()
    if choice == "s":
        check = input("Nome do arquivo: ")
        if re.search(check, ".txt"):
            nome = open(check, "w+")
        else:
            check += ".txt"
            nome = open(check, "w+")
    
        for i in cpf:
            nome.write(f"{i} | {cpf[i]}\n")
        nome.close()

    elif choice == "n":
        exit


while True:
    try:
        qt = int(input(f"{Fore.YELLOW}Quantidade{Fore.RESET}: "))
        if qt > 30: #limitador do webcrawler (opcional)
            print(f"{Fore.RED}O seu máximo de coleta é 30")
            continue

        elif qt == 0 or qt < 0: #tratamento de erros
            print(f"{Fore.RED}Quantidade Inválida!!")
            continue

        pt = str(input(f"{Fore.YELLOW}Deseja gerar com pontuação?(S/n) ")).lower()
    except KeyboardInterrupt: #tratamento de erros para CTRL+C
        ys = str(input(f"\n{Fore.RED}Deseja sair?(N/s) ")).lower()
        if ys == "s":
            exit(0)
        else:
            continue
    
    for i in range(1, qt+1):
        data = {"acao": "gerar_cpf", "pontuacao": pt, "cpf_estado": choice(estados)} #requisitos para a requisição

        with open("user-agents.txt", "r+") as agents:
            ag = agents.readlines()
            ag = choice(ag) #Escolhendo um agent aleatorio para cada passagem

            users["User-Agent"] = ag.rstrip("\n")
            get = data["cpf_estado"]

            try:
                r = requests.post(url, headers=users, data=data)
                #print(f"{Fore.GREEN}[{i}] >>> {r.text} | {get}") Formatação (Opcional)
                sys.stdout.write(f"\rDados Coletados: {i}") #formatação com cursor
                time.sleep(0.1) #opcional
                cpf[f"{r.text}"] = get
            
                agents.close()

            except requests.exceptions.ConnectionError:
                print(f"{Fore.RED}Desconectado da rede!")

            except KeyboardInterrupt:
                ys = str(input(f"\n{Fore.RED}Deseja sair?(N/s) ")).lower()
                if ys == "s":
                    exit(0)
                else:
                    continue

    exibir = str(input("\rLer os dados coletados?(S/n) {Fore.RESET}")).lower()
    try:
        if exibir == "s":
            for i in cpf:
                print(f"{Fore.GREEN}{i} | {cpf[i]}")
        else:
            break
    except:
        print(f"{Fore.RED}Erro na entrada de dados!!")
        exit(0)

    break


arquivo()



