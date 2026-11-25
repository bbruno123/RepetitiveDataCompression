

# Demonstrações de compressão de dados repetitivos

Este projeto contém duas demonstrações independentes: uma usa ZIP com DEFLATE e a outra representa repetições usando RLE. Ambas trabalham com sequências do caractere `A`, mas usam formatos diferentes.

## Dependências Python

O arquivo `requirements.txt` lista as bibliotecas externas usadas pelo projeto. No Windows, instale-as a partir da raiz do projeto com:

```shell
python -m pip install -r requirements.txt
```

No `RLETextExpansion`, `pywin32` fornece `win32com.client`, usado para criar o atalho na pasta Inicializar do Windows. `pyinstaller` só é necessário para gerar `compress_decompress.exe`; não é necessário para executar o script Python. Os módulos padrão do Python, como `os`, `subprocess`, `time` e `zipfile`, não precisam ser instalados separadamente.

## ZipBomb (DEFLATE)

Este script gera um arquivo chamado `ZipBomb.zip` contendo um único arquivo interno chamado `ZipBomb.txt`.

O arquivo interno é preenchido com dados altamente repetidos (letras `A`) e comprimido usando o método DEFLATE com nível máximo de compressão. Como os dados são repetitivos, o arquivo ZIP final fica muito pequeno em relação ao tamanho original dos dados.

### Como o script funciona

* O script está em `ZipBomb/ZipBomb.py`.
* Define o tamanho original em `tamanho_total` e o tamanho dos blocos em `tamanho_bloco`.
* Cria `ZipBomb.zip` com compressão DEFLATE no nível 9 e inclui o arquivo `ZipBomb.txt`.
* Escreve os dados em blocos de 64 MiB para não carregar todo o conteúdo na memória.
* Exibe o progresso da geração.
* Ao finalizar, mostra o tamanho compactado, o tamanho original, a taxa de compressão e o tempo gasto.

### Requisitos

* Python 3
* Biblioteca padrão `zipfile`, `os` e `time`

### Como executar

Execute a partir da raiz do projeto:

```shell
python ZipBomb/ZipBomb.py
```

O arquivo `ZipBomb.zip` será criado no diretório de trabalho atual. Ele contém `ZipBomb.txt`.

### Alterar o tamanho do arquivo descompactado

Para alterar o tamanho original contido no ZIP, modifique `tamanho_total` em `ZipBomb/ZipBomb.py`.

O valor padrão gera um conteúdo original de aproximadamente 10 GB:

```python
tamanho_total = 10 * (1024 ** 3)
```

Exemplo para aproximadamente 1 GB:

```python
tamanho_total = 1 * (1024 ** 3)
```

Os valores são calculados em bytes. Exemplos:

* `1 * (1024 ** 3)` — aproximadamente 1 GB
* `2 * (1024 ** 2)` — aproximadamente 2 MB
* `100 * (1024 ** 2)` — aproximadamente 100 MB

> **Aviso:** a extração pode consumir muito espaço em disco e tempo. Use apenas em um ambiente controlado e com recursos suficientes.

## RLETextExpansion (RLE)

`RLETextExpansion/compress_decompress.py` combina a criação da representação e sua expansão em um único script. Ele **não cria nem lê um arquivo `.rle`**: `compactar()` monta em memória um dicionário com o caractere `A` e a quantidade de bytes; em seguida, `descompactar()` valida esses valores e grava `repeated_text.txt` em blocos de 1 MiB.

O tamanho é controlado por `TAMANHO_FINAL_YTB`, calculado como `TAMANHO_FINAL_YTB * (1024 ** 8)`. O valor padrão é `1`, portanto o script tenta materializar `1024 ** 8` bytes, um volume impraticável em um computador comum. Se o disco ficar sem espaço, ele informa o problema e tenta novamente a cada cinco segundos. O arquivo de saída é criado junto ao script Python ou, quando empacotado, junto ao executável; no Windows, o script tenta marcá-lo como oculto. O atributo oculto não reduz o tamanho nem o espaço ocupado.

> **Uso somente em laboratório:** este script serve para testes controlados de representação RLE e expansão de dados. Não o execute com o tamanho padrão em uma máquina ou disco com dados importantes. A gravação pode consumir todo o espaço disponível e comprometer o funcionamento do sistema. Reduza `TAMANHO_FINAL_YTB` para um valor adequado antes de testar.

### Inicialização do Windows

No início da execução, a função `iniciar_com_windows()` cria ou atualiza o atalho `RLETextExpansion.lnk` em `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`. O atalho aponta para o próprio `compress_decompress.py` quando executado como script Python ou para o `.exe` quando executado como programa empacotado, e usa a pasta do programa como diretório de trabalho. Assim, se o atalho for criado, o programa será iniciado automaticamente quando o usuário entrar no Windows. A falha ao criar o atalho é exibida, mas não impede a continuação do script.

### Gerar e executar o `.exe`

Com Python, `pywin32` e PyInstaller instalados, execute a partir de `RLETextExpansion` para gerar `saida/compress_decompress.exe`:

```powershell
python -m PyInstaller --onefile --noconsole --clean --distpath .\saida --workpath .\build --specpath . compress_decompress.py
```

O executável é uma versão empacotada do mesmo script: também tenta criar o atalho de inicialização e grava `repeated_text.txt` em `RLETextExpansion/saida`, ao lado do `.exe`. O modo sem console não altera o tamanho gerado nem o consumo de armazenamento. Revise `TAMANHO_FINAL_YTB` antes de compilar e executar.

### Relação entre as versões

As duas versões demonstram maneiras de representar ou comprimir sequências de dados repetidos. A diferença está na representação e no resultado persistido:

* **DEFLATE (`ZipBomb/`):** grava os dados repetidos dentro de um membro ZIP e usa DEFLATE no nível 9. O resultado é `ZipBomb.zip`, que contém `ZipBomb.txt`.
* **RLE (`RLETextExpansion/`):** representa em memória o caractere e sua quantidade e grava `repeated_text.txt` em blocos, sem gerar arquivo `.rle`, ZIP ou usar DEFLATE.

Portanto, DEFLATE produz um arquivo comprimido, enquanto este exemplo RLE mantém apenas um descritor em memória antes de escrever a saída expandida. A expansão pode exigir recursos muito além dos disponíveis.

## Arquivos ZIP e Git

A regra `*.zip` no `.gitignore` ignora arquivos ZIP em qualquer pasta do projeto. Ela não remove do controle de versão arquivos que já tenham sido adicionados ao Git.
