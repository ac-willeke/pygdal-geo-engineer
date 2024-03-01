# Unix Shell Cheatsheet

Source: [Datacamp | Introduction to shell](https://learn.datacamp.com/courses/introduction-to-shell)

## 0. Configuring your shell

- Configure your shell to bash
 ```shell
    # Check your shell configuration
    echo $0
    # Change your shell configuration
    chsh -s /bin/bash
    # Check your shell configuration
    echo $0
```
- Make changes to your bash configuration and execute them
```shell
    # Add a new/path/to/your/tool to your PATH variable
    echo 'export PATH="$PATH:/new/path/to/your/tool"' >> ~/.bashrc
    # Execute your bash configuration
    source ~/.bashrc
```

- Disable automatic conda base activation in shell
```shell
    # Check your shell configuration
    conda config --show | grep auto_activate_base
    # Disable automatic conda base activation in shell
    conda config --set auto_activate_base false
    # Check your shell configuration
    conda config --show | grep auto_activate_base
```


## 1. Manipulating files and directories

| Command | Description | Output example |
|---------|-------------|----------------|
|clear|clear the terminal| |
|pwd|print working directory| /home/willeke.acampo
|ls|listing|Desktop Documents Downloads Music Pictures Public Templates Videos|
|ls Documents|listing of a specific directory|file1.txt file2.txt file3.txt|
|/absolute/path|absolute path starts with / |/home/willeke.acampo/Documents|
|relative/path|relative path starts without / |Documents|
|cd|change directory|cd Documents|
|cd ..|change directory to parent directory|cd ..|
|cd ~|change directory to home directory|cd ~|
|cd -|change directory to previous directory|cd -|
|cp|copy file-name new-file-name|cp file1.txt file2.txt|
|cp -r|copy directory-name new-directory-name|cp -r Documents Documents2|
|mv|move file-name new-file-name|mv home/file1.txt backup/file1.txt|
|  |rename file using move|mv file1.txt file2.txt|
|rm|remove file-name *! file is removed for good !*|rm file1.txt|
|rmdir|remove directory-name *! directory is removed for good, only works on empty dirs !*|rmdir Documents|
|mkdir|make directory-name|mkdir Documents|
|mkdir -p|make directory-name *! also creates parent directories if they don't exist !*|mkdir -p Documents/2019/01|

## 2. Manipulating data

## 3. Combining tools

## 4. Batch processing

## 5. Creating new tools
