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

O diretório `RLETextExpansion` contém uma demonstração em Python que representa dados repetitivos em memória e expande um caractere `A` no arquivo `repeated_text.txt`. Ele **não cria nem lê um arquivo `.rle`**: `compactar()` monta um dicionário com o caractere e a quantidade de bytes; `descompactar()` valida esses valores e grava o resultado em blocos de 1 MiB.

O programa representa em memória 1 YTB com o seguinte padrão:

- Caractere: `A`
- Quantidade: `1 * 1024^8` bytes

Na descompactação, ele escreve o caractere em blocos de 1 MiB no arquivo `repeated_text.txt`. No Windows, o arquivo fica oculto após a gravação. Caso o Windows recupere ou libere espaço em disco, o programa continua tentando ocupar esse espaço novamente enquanto não atingir a quantidade configurada.

> **Uso somente em laboratório:** o volume configurado é extremamente grande e pode preencher o disco, travar o sistema ou causar erros. Não o execute com o tamanho padrão em uma máquina ou disco com dados importantes. Antes de testar, reduza `TAMANHO_FINAL_YTB` em `RLETextExpansion/compress_decompress.py` para um valor adequado.

### Como funciona

O tamanho é controlado por `TAMANHO_FINAL_YTB`, calculado como `TAMANHO_FINAL_YTB * (1024 ** 8)`. O valor padrão é `1`, portanto o script tenta materializar `1024 ** 8` bytes.

- `RLETextExpansion/compress_decompress.py`: implementação principal.
- `RLETextExpansion/gerar_exe.txt`: procedimento automatizado para gerar o executável no Windows.
- `RLETextExpansion/saida/`: diretório do executável gerado.
- `repeated_text.txt`: arquivo expandido criado junto ao script ou ao executável.

Se o disco ficar sem espaço, o script informa o problema e tenta novamente a cada cinco segundos.

### Executar com Python

A partir da raiz do projeto:

```powershell
python RLETextExpansion/compress_decompress.py
```

A partir da própria pasta `RLETextExpansion`:

```powershell
python compress_decompress.py
```

### Inicialização automática no Windows

No início da execução, a função `iniciar_com_windows()` cria ou atualiza o atalho `RLETextExpansion.lnk` em:

```text
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
```

O atalho aponta para `compress_decompress.py` quando executado como script ou para `compress_decompress.exe` quando empacotado. A pasta do programa é usada como diretório de trabalho. Assim, o programa pode ser iniciado automaticamente ao entrar no Windows. Uma falha ao criar o atalho é exibida, mas não impede a continuação do script.

### Gerar o executável

Com Python, `pywin32` e PyInstaller instalados, execute a partir de `RLETextExpansion`:

```powershell
python -m PyInstaller --onefile --noconsole --clean --distpath .\saida --workpath .\build --specpath . compress_decompress.py
```

O executável será criado em `RLETextExpansion/saida/compress_decompress.exe`. Ele tenta criar o atalho de inicialização e grava `repeated_text.txt` na própria pasta `saida`. O modo sem console não altera o tamanho dos dados gerados nem o consumo de armazenamento.

O arquivo `RLETextExpansion/gerar_exe.txt` contém uma versão automatizada para o Prompt de Comando do Windows. Copie e execute esta única linha a partir da pasta `RLETextExpansion`:

```bat
if not exist saida mkdir saida & set "python=" & for %D in (C D E F G H I J K L M N O P Q R S T U V W X Y Z) do @if not defined python if exist "%D:\Projects\PortableApps\Python\python.exe" (set "python=%D:\Projects\PortableApps\Python\python.exe" & "%D:\Projects\PortableApps\Python\python.exe" -m PyInstaller --onefile --noconsole --clean --distpath .\saida --workpath .\build --specpath . compress_decompress.py & if not errorlevel 1 (rmdir /s /q build & del /q compress_decompress.spec)) & if not defined python echo Python nao encontrado em nenhuma unidade.
```

Esse comando procura uma instalação portátil em `X:\Projects\PortableApps\Python\python.exe`, testando as unidades locais de `C` até `Z`. Quando encontra o Python, usa o PyInstaller para gerar o executável e remove `build` e `compress_decompress.spec` em caso de sucesso. Se não encontrar o Python nessa localização, ele informa `Python nao encontrado em nenhuma unidade`.

Antes de gerar ou executar o `.exe`, revise `TAMANHO_FINAL_YTB = 1` em `compress_decompress.py`. O atributo oculto não reduz o tamanho nem o espaço ocupado pelo arquivo.

### Relação entre as versões

As duas versões demonstram maneiras de representar ou comprimir sequências de dados repetidos. A diferença está na representação e no resultado persistido:

* **DEFLATE (`ZipBomb/`):** grava os dados repetidos dentro de um membro ZIP e usa DEFLATE no nível 9. O resultado é `ZipBomb.zip`, que contém `ZipBomb.txt`.
* **RLE (`RLETextExpansion/`):** representa em memória o caractere e sua quantidade e grava `repeated_text.txt` em blocos, sem gerar arquivo `.rle`, ZIP ou usar DEFLATE.

Portanto, DEFLATE produz um arquivo comprimido, enquanto este exemplo RLE mantém apenas um descritor em memória antes de escrever a saída expandida. A expansão pode exigir recursos muito além dos disponíveis.

## Arquivos ZIP e Git

A regra `*.zip` no `.gitignore` ignora arquivos ZIP em qualquer pasta do projeto. Ela não remove do controle de versão arquivos que já tenham sido adicionados ao Git.
