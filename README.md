# BrainFuck to amd64 assembler translator


## Reference:
```
usage: main.py [-h] -i BRAINFUCK_INPUT [-o [ASM_OUTPUT]] [-c BIN_OUTPUT]

BrainFuck to amd64 assembler translator

options:
  -h, --help            show this help message and exit
  -i BRAINFUCK_INPUT, --in BRAINFUCK_INPUT
                        Input brainfuck source filename
  -o [ASM_OUTPUT], --out [ASM_OUTPUT]
                        Output asm file (default stdout)
  -c BIN_OUTPUT, --compile BIN_OUTPUT
                        Compile asm (required nasm)
```

## Usage

### Translate brainfuck to ASM:
```
$ python3 main.py -i fibonacci.bf -o fibonacci.asm
```

### Compile brainfuck to ELF (nasm required):
```
$ python3 main.py -i fibonacci.bf -c result
```