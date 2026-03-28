# Advanced Computer Programming

## Setup

### Requirements
- [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
- [Java 11 or newer](https://www.java.com/en/download/help/download_options.html)

### Creating the python virtual enviroment
```
conda create -n advanced-computer-programming python=3.11
conda activate advanced-computer-programming
pip install notebook ipykernel jupyter-client 
```

### Installing the Java kernel for jupyter notebook
1. Download [JJava](https://github.com/dflib/jjava): go to [GitHub releases](https://github.com/dflib/jjava/releases), pick the latest version (or a specific one that you need) and under the "Assets" section download a file called `jjava-${version}-kernelspec.zip`
2. Unzip the file into a temporary location
3. Run the following commands from the parent directory that contains the unzipped kernel folder

```bash
jupyter kernelspec install jjava-${version}-kernelspec --user --name=java
```

### Verify installation

```bash
jupyter kernelspec list
```
The output should be something like this:
```
Available kernels:
  python3    /home/angelo/miniconda3/envs/advanced-computer-programming/share/jupyter/kernels/python3
  java       /home/angelo/.local/share/jupyter/kernels/java
```
