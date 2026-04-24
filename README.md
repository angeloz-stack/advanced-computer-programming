# Advanced Computer Programming

Docente: [Raffaele Della Corte](https://www.docenti.unina.it/raffaele.dellacorte2)

Lingua del corso: Italiano

Anno accademico: 2025/2026

## 🇮🇹 Italiano

## Configurazione

### Requisiti
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Java 11 o versione successiva](https://www.java.com/en/download/help/download_options.html)

### Creazione dell'ambiente virtuale Python
```bash
# Assicurarsi di avere Python 3.13 installato (ad esempio tramite pyenv o uv)
uv sync
```

### Installazione del kernel Java per Jupyter Notebook

1. Scaricare [JJava](https://github.com/dflib/jjava): andare alla pagina delle [release su GitHub](https://github.com/dflib/jjava/releases), scegliere la versione più recente (o una specifica, se necessario) e nella sezione "Assets" scaricare il file `jjava-${version}-kernelspec.zip`
2. Estrarre il file in una posizione temporanea
3. Eseguire i seguenti comandi dalla directory padre che contiene la cartella del kernel decompressa

```bash
uv run jupyter kernelspec install jjava-${version}-kernelspec --user --name=java
```

### Verifica dell'installazione
```bash
uv run jupyter kernelspec list
```

L'output dovrebbe essere simile a questo:
```
Available kernels:
  python3    path/to/advanced-computer-programming/.venv/share/jupyter/kernels/python3
  java       /home/angelo/.local/share/jupyter/kernels/java
```

## 🇬🇧 English

## Setup

### Requirements
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Java 11 or newer](https://www.java.com/en/download/help/download_options.html)

### Creating the Python virtual environment
```bash
# Make sure to have Python 3.13 installed (e.g. via pyenv or uv)
uv sync
```

### Installing the Java kernel for Jupyter Notebook

1. Download [JJava](https://github.com/dflib/jjava): go to [GitHub releases](https://github.com/dflib/jjava/releases), pick the latest version (or a specific one that you need) and under the "Assets" section download a file called `jjava-${version}-kernelspec.zip`
2. Unzip the file into a temporary location
3. Run the following commands from the parent directory that contains the unzipped kernel folder

```bash
uv run jupyter kernelspec install jjava-${version}-kernelspec --user --name=java
```

### Verify installation
```bash
uv run jupyter kernelspec list
```

The output should be something like this:
```
Available kernels:
  python3    path/to/advanced-computer-programming/.venv/share/jupyter/kernels/python3
  java       /home/angelo/.local/share/jupyter/kernels/java
```