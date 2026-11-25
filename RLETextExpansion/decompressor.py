import json
import os

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

        while restante > 0:

            tamanho = min(restante, TAMANHO_BLOCO)

            arquivo.write(bloco[:tamanho])

            restante -= tamanho

            progresso = ((quantidade - restante) / quantidade) * 100

            print(f"Progresso: {progresso:.2f}%", end="\r")

    print("\nDescompactação concluída!")
    print(f"Tamanho reconstruído: {quantidade / (1024 ** 3):.2f} GB")
    print(f"Tamanho no disco: {os.path.getsize(ARQUIVO_SAIDA)} bytes")


if __name__ == "__main__":
    descompactar()
