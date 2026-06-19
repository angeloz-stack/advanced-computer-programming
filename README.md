# Advanced Computer Programming

- Docente: [Raffaele Della Corte](https://www.docenti.unina.it/raffaele.dellacorte2)
- [Repository ufficiale del corso](https://github.com/ACP-unina/acp_materiale/tree/main)
- Lingua del corso: Italiano
- Anno accademico: 2025/2026

## Struttura della repository

```text
.
├── notebooks/
│   ├── 01_concurrency/
│   ├── 02_networking/
│   └── 03_middleware/
└── projects/
    ├── java/
    ├── python/
    └── java-python/
```

- `notebooks/` — appunti e teoria organizzati per argomento
- `projects/` — esercizi svolti, suddivisi per linguaggio (Java, Python, misti Java-Python)

## Configurazione

### Requisiti
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Java 11 o versione successiva](https://www.java.com/en/download/help/download_options.html)
- [Estensione VSCode](https://marketplace.visualstudio.com/items?itemName=purocean.drawio-preview) per visualizzare gli schemi drawio; in alternativa, possono essere aperti nella [webapp](https://www.drawio.com/).

### Creazione dell'ambiente virtuale Python
```bash
# Assicurarsi di avere Python 3.13 installato (ad esempio tramite pyenv o uv)
uv sync
```

### Installazione del kernel Java per Jupyter Notebook

1. Scaricare [JJava](https://github.com/dflib/jjava): andare alla pagina delle [release su GitHub](https://github.com/dflib/jjava/releases), scegliere la versione più recente (o una specifica, se necessario) e nella sezione "Assets" scaricare il file `jjava-${version}-kernelspec.zip`
2. Estrarre il file in una posizione temporanea (ad esempio, `path/to/tmp_folder/`)
3. Eseguire i seguenti comandi dalla directory della repository

```bash
cd path/to/advanced-computer-programming

uv run jupyter kernelspec install path/to/tmp_foder/jjava-${version}-kernelspec --user --name=java
```

#### Verifica dell'installazione
```bash
uv run jupyter kernelspec list
```

L'output dovrebbe essere simile a questo:
```
Available kernels:
  python3    path/to/advanced-computer-programming/.venv/share/jupyter/kernels/python3
  java       /home/angelo/.local/share/jupyter/kernels/java
```
### Installazione di ActiveMQ
È necessario installare per gli esercizi che fanno usi di messaggi il middleware MOM ActiveMQ, in particolare la versione 5.16.6.

Il necessario per l'installazione si trova [qui](https://activemq.apache.org/components/classic/download/classic-05-16-06)

### Utilizzo di JMS
1. Individuare `activemq-all-{version}.jar` dai binaries di ActiveMQ (nel nostro caso `activemq-all-5.16.6.jar`)
2. In un progetto Java con la seguente struttura:

```text
src/
bin/
lib/
```

3. Copiare il file in `lib/`

Dalla cartella del progetto, compilare con:
```bash
javac -cp "lib/activemq-all-5.16.6.jar:" -d out $(find src -name "*.java")
```

> Nota sul separator `:` finale in `lib/activemq-all-5.16.6.jar:` — su Mac/Unix i due punti separano le entry del classpath e vanno mantenuti.

Per eseguire:
```bash
java -cp "lib/activemq-all-5.16.6.jar:out" nome_package.nome_file *args
```
