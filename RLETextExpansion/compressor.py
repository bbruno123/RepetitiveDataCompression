import json
import os

# CONFIGURAÇÕES
PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_SAIDA = os.path.join(PASTA_ATUAL, "saida", "repeated_text.rle")

TAMANHO_FINAL_YTB = 1

def compactar():

    quantidade = TAMANHO_FINAL_YTB * (1024 ** 8)

    dados = {
        "caractere": "A",
        "quantidade": quantidade
    }

    print("Compactando...")

    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, separators=(",", ":"))

    tamanho = os.path.getsize(ARQUIVO_SAIDA)

    progresso = 100.0
    print(f"Progresso: {progresso:.2f}%", end="\r")

    print("\nRepresentação criada!")
    print(f"Tamanho original representado: {TAMANHO_FINAL_YTB} YTB")
    print(f"Tamanho do arquivo gerado: {tamanho} bytes")


if __name__ == "__main__":
    compactar()
