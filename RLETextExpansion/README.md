# RLETextExpansion

Programa em Python que cria uma representação compacta de dados repetitivos em memória e, ao executá-lo, expande um caractere `A` em um arquivo chamado `repeated_text.txt`.

## Início com o Windows

O método de atalho foi restaurado. Ao executar o script ou o arquivo `.exe`, o programa tenta criar o atalho:

- `RLETextExpansion.lnk`
- Na pasta de Inicialização do usuário do Windows

Esse atalho faz com que o programa seja iniciado automaticamente ao entrar no Windows. Se o script estiver em execução, o atalho aponta para o próprio arquivo Python; no executável gerado pelo PyInstaller, ele aponta para o `.exe` correspondente.

## Como funciona

O programa representa em memória 1 YTB com o seguinte padrão:

- Caracterize: `A`
- Quantidade: `1 * 1024^8` bytes

Na descompactação, ele escreve o caractere em blocos de 1 MB no arquivo `repeated_text.txt`. O arquivo fica oculto no Windows após a gravação. Caso o Windows recupere ou libere espaço em disco, o programa continua tentando ocupar esse espaço novamente enquanto não atingir a quantidade configurada.

> Atenção: o volume configurado é extremamente grande e pode preencher o disco, travar o sistema ou causar erros dependendo dos recursos disponíveis. O programa aguarda e tenta continuar quando detecta falta de espaço, mas não garante que ele possa ser interrompido sem consequências.

## Executar com Python

```powershell
python compress_decompress.py
```

## Gerar o executável

As instruções de build estão no arquivo `gerar_exe.txt`.

O executável será produzido em:

```text
saida/compress_decompress.exe
```

## Arquivos

- `compress_decompress.py`: implementação principal
- `gerar_exe.txt`: instruções para gerar o executável
- `saida/`: diretório do executável
- `repeated_text.txt`: arquivo criado na descompactação
