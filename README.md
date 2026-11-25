

# Demonstrações de compressão de dados repetitivos

Este projeto contém duas demonstrações independentes: uma usa ZIP com DEFLATE e a outra representa repetições usando RLE. Ambas trabalham com sequências do caractere `A`, mas usam formatos diferentes.

## Dependências Python

O arquivo `requirements.txt` lista as bibliotecas externas usadas pelo projeto. No Windows, instale-as a partir da raiz do projeto com:

```shell
python -m pip install -r requirements.txt
```

`winshell` e `pywin32` são usadas pelo descompactador para criar o atalho na pasta Inicializar do Windows. `pyinstaller` só é necessário para gerar `decompressor.exe`; não é necessário para executar os scripts Python. Os módulos padrão do Python, como `json`, `os`, `subprocess` e `zipfile`, não precisam ser instalados separadamente.

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

A segunda versão usa *Run-Length Encoding* (RLE): em vez de armazenar cada repetição do caractere `A`, o arquivo `repeated_text.rle` guarda o caractere e a quantidade de repetições. Esse arquivo é JSON, não um arquivo ZIP.

### Como o compressor funciona

O script `RLETextExpansion/compressor.py`:

* Define `ARQUIVO_SAIDA` como `RLETextExpansion/saida/repeated_text.rle`.
* Define o tamanho representado em `TAMANHO_FINAL_YTB`.
* Calcula a quantidade de bytes usando `TAMANHO_FINAL_YTB * (1024 ** 8)`.
* Grava no JSON os campos `caractere` e `quantidade`, sem espaços extras.
* Exibe o tamanho do descritor criado e o tamanho representado.

Como o JSON guarda apenas uma descrição da sequência, ele permanece minúsculo mesmo quando representa uma quantidade enorme de dados. No valor padrão, `TAMANHO_FINAL_YTB = 1`, a quantidade corresponde a `1024 ** 8` bytes, um volume impraticável para materializar em um computador comum. A pasta `RLETextExpansion/saida` precisa existir antes de executar o compressor.

### Como executar o descompressor

O script `RLETextExpansion/decompressor.py` lê `repeated_text.rle` e cria `repeated_text.txt` no diretório de trabalho atual. Ele verifica se o caractere é `A` e se a quantidade é um inteiro não negativo; em seguida, grava em blocos de 1 MiB e atualiza o progresso. Para usar os arquivos de `saida`, execute o script a partir dessa pasta:

```powershell
cd RLETextExpansion\saida
python ..\decompressor.py
```

O arquivo de entrada esperado é `RLETextExpansion/saida/repeated_text.rle`, e a saída seria `RLETextExpansion/saida/repeated_text.txt`.

### Efeitos colaterais do descompactador

Ao ser executado, `decompressor.py` tenta criar o atalho `RLETextExpansion.lnk` na pasta Inicializar do usuário atual do Windows, normalmente `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`. Se o atalho for criado e o Windows conseguir abrir arquivos `.py`, o script será iniciado novamente a cada entrada na conta do Windows.

O arquivo `repeated_text.txt` também recebe o atributo de oculto no Windows. Isso não reduz o espaço que ele ocupa: a quantidade indicada em `repeated_text.rle` ainda será gravada no disco. Como essa quantidade pode ser extrema, não execute o script sem antes verificar o valor e garantir que há espaço suficiente.

### Gerar o executável

Com o PyInstaller instalado no ambiente Python ativo, execute os comandos a partir de `RLETextExpansion/saida`. O comando abaixo usa o descompactador da pasta acima, gera `decompressor.exe` dentro de `saida` e remove os arquivos temporários após a compilação:

```powershell
python -m PyInstaller --onefile --noconsole --clean --distpath . --workpath .\build --specpath . ..\decompressor.py; if ($LASTEXITCODE -eq 0) { Remove-Item .\build, .\decompressor.spec -Recurse -Force }
```

Execute `decompressor.exe` com `saida` como diretório de trabalho para que ele encontre `repeated_text.rle` nessa pasta.

Gravar em blocos reduz o uso de memória, mas não reduz o espaço em disco nem o tempo necessários para produzir o arquivo completo. **Não execute o descompactador com a configuração padrão:** ele tentará criar um arquivo de tamanho extremo e pode esgotar o armazenamento ou tornar o sistema indisponível.

### Relação entre as versões

As duas versões representam grandes sequências de dados repetidos e podem resultar em um arquivo de saída muito menor que o conteúdo reconstruído. A diferença está na representação:

* **DEFLATE (`ZipBomb/`):** grava os dados repetidos dentro de um membro ZIP e usa DEFLATE no nível 9. O resultado é `ZipBomb.zip`, que contém `ZipBomb.txt`.
* **RLE (`RLETextExpansion/`):** registra apenas o caractere e sua quantidade em `repeated_text.rle`. Um script separado lê essa descrição e escreve `repeated_text.txt` em blocos; não há ZIP nem algoritmo DEFLATE nessa versão.

Portanto, as versões demonstram duas formas distintas de representar sequências repetitivas: compressão de propósito geral (DEFLATE) e codificação por repetição (RLE). Em ambas, o tamanho pequeno da representação não significa que seja seguro expandi-la: a saída pode exigir recursos muito além dos disponíveis.

## Arquivos ZIP e Git

A regra `*.zip` no `.gitignore` ignora arquivos ZIP em qualquer pasta do projeto. Ela não remove do controle de versão arquivos que já tenham sido adicionados ao Git.
