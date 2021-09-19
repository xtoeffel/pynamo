# Installation and Execution

Two options for installation are available. 
Download of the _Windows_ executable package or run the code directly 
with the _Python_ interpreter.
Ladder works with any operating system that supports _Python_.

## Command Line
_Pynamo_ is a console program. 
That means it must be executed from the command line like a shell or terminal.

## Windows Executable
The tool can be downloaded as _Windows_ executable at
[pynamo_1_0_0.zip](pynamo_1_0_0.zip). 
This does not require the installation of _Python_ and should work as is.

To execute the tool change into the folder where `pynamo.exe` is located
and call
```bash
pynamo -h
```
This will print the help message.

## Python Interpreter
Clone or download the repo under 
[https://github.com/xtoeffel/pynamo](https://github.com/xtoeffel/pynamo).
Make sure to download the _master_ branch. 
Other branches are likely under development and should not be used for 
computations.

_Python_ must be installed on your system. 
[Anaconda Individual](https://www.anaconda.com/products/individual-d) is a good choice.
Build the required environment named `pynamo` by:
```bash
conda env create -f environment.yml
```
The file `environment.yml` is located in the root folder of the repository.

Before you start the tool make sure that this environment is activated.
```bash
conda activate pynamo
```
Now you are ready to start the tool by:
```bash
python pynamo -h
```
This will print the help message.
