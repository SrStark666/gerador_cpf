from ctypes import windll
import random
from colorama import Fore
import requests
import re
import time


class Request:
    def __init__(self) -> None:
        self.win = windll.kernel32.SetConsoleMode(windll.kernel32.GetStdHandle(-11),7)
        self.cpf_dict = {}
        self.api_gen = "https://www.4devs.com.br/ferramentas_online.php"
        self.api_verify = "https://seaborne-reconfigur.000webhostapp.com/api.php?consulta="
        self.invalid = 0
        self.cpf = ""


    def menu(self) -> None:
        print(f"""
    {Fore.MAGENTA}Panel Crawler{Fore.RESET}
    [{Fore.CYAN}1{Fore.RESET}]Coletar dados
    [{Fore.CYAN}2{Fore.RESET}]Consulta Cpf
    [{Fore.CYAN}3{Fore.RESET}]Sair
        """)
        try:
            choice = int(input("==> "))
        except:
            print(f"{Fore.RED}Erro na entrada de dados{Fore.RESET}")

        match choice:
            case 1:
                self.generate()
            case 2:
                cpf = str(input(f"{Fore.YELLOW}Cpf: {Fore.RESET}")).replace(".-", "")
                self.cpf_dict["Consulta"] = cpf
                self.verify()
            case 3:
                exit


    def generate(self) -> None:
        while True:
            num = int(input(f"{Fore.YELLOW}Quantidade: {Fore.RESET}"))
            point = str(input(f"{Fore.YELLOW}Gerar com pontuação? S/n {Fore.RESET}")).lower()

            for quant in range(1, num+1):
                with open("states.txt", "r") as est:
                    estados = [i for i in est.readlines()]
                    data = {"acao": "gerar_cpf", "pontuacao": point, "cpf_estado": random.choice(estados).rstrip("\n")}
                    data_state = data["cpf_estado"]
                    with open("user-agents.txt", "r") as ag:
                        agents = [i for i in ag.readlines()]
                        try:
                            post = requests.post(self.api_gen, headers={"User-Agent": random.choice(agents).rstrip("\n")}, data=data)
                            self.cpf_dict[post.text] = data_state
                        except requests.exceptions.ConnectionError:
                            print(f"{Fore.RED}Desconectado da rede{Fore.RESET}")

            for i in self.cpf_dict:
                print(f"{Fore.GREEN}{i}  | {self.cpf_dict[i]}{Fore.RESET}")

            print(f"\n{Fore.GREEN}Iniciando a validação dos dados{Fore.RESET}")
            self.verify()

            print(f"{Fore.YELLOW}Deseja salvar os dados coletados? {Fore.RESET}")
            try:
                choice = str(input(f"{Fore.YELLOW}==> {Fore.RESET}")).lower().replace("sim", "s").replace("não", "n").replace("nao", "n")
            except:
                print(f"{Fore.RED}Erro na entrada de dados{Fore.RESET}")

            if choice == "s":
                self.archive()
                break

        self.menu()
        
    def verify(self) -> None:
        for i in list(self.cpf_dict):
            try:
                get = requests.get(self.api_verify+self.cpf_dict[i], timeout=5)
                time.sleep(3)
                if get.status_code == 200:
                    valid = get.json()
                    if i == "Consulta":
                        if valid["cpfValido"] != 0:
                            print(f"{Fore.RED}{self.cpf_dict[i]} - Inválido{Fore.RESET}")
                            self.invalid += 1
                            self.cpf_dict.pop(i)
                        else:
                            print(f"""Cpf: {i}\n
                            Nome: {valid['nomeCompleto']}\n
                            Nascimento: {valid['dtNascimento']}\n
                            Mãe: {valid['nomeMae']}
                            Cns: {valid['cns']}""")

            except requests.exceptions.ConnectionError:
                print("Erro")
                pass


    def archive(self) -> None:
        check = str(input(f"{Fore.CYAN}Nome do arquivo: {Fore.RESET}"))
        if re.search(check, ".txt"):
            nome = open(check, "w+")
        else:
            check += ".txt"
            nome = open(check, "w+")
    
        for i in self.cpf_dict:
            nome.write(f"{i} | {self.cpf_dict[i]}\n")

        nome.close()


obj = Request()
obj.menu()
