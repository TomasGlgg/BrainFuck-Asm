from os import system
import tempfile
import argparse
import pathlib


MEMORY_SIZE = 0x1000
TEMPLATE_FILENAME = 'template.asm'


def compile(inputfile, outputfile):
    with tempfile.NamedTemporaryFile(suffix='.o') as tmp_file:
        compile_commands = (
            f'nasm -f elf64 {inputfile} -o {tmp_file.name}',
            f'ld -m elf_x86_64 -s -o {outputfile} {tmp_file.name}'
        )
        for command in compile_commands:
            system(command)


PTR_INCREMENT = '\tINC rsi\n'
PTR_DECREMENT = '\tDEC rsi\n'
INCREMENT = '\tINC byte [rsi]\n'
DECREMENT = '\tDEC byte [rsi]\n'
PUTCHAR = '\tCALL putchar\n'
LOOP_START = '''\n\tmov al, [rsi]
\ttest rax, rax
\tjz end_loop_{0}
start_loop_{0}:\n'''
LOOP_END = '''\n\tmov al, [rsi]
\ttest rax, rax
\tjnz start_loop_{0}
end_loop_{0}:\n'''


class Translator:
    bf_code = str()
    asm_code = str()
    template = str()
    loop_index = -1
    loop_stack = list()

    def load_bf_code(self, bf_fd):
        self.bf_code = bf_fd.read().strip()

    def _add_asm_opcode(self, opcode):
        self.asm_code += opcode

    def translate(self):
        for opcode in self.bf_code:
            match opcode:
                case '>':
                    self._add_asm_opcode(PTR_INCREMENT)
                case '<':
                    self._add_asm_opcode(PTR_DECREMENT)
                case '+':
                    self._add_asm_opcode(INCREMENT)
                case '-':
                    self._add_asm_opcode(DECREMENT)
                case '.':
                    self._add_asm_opcode(PUTCHAR)
                case '[':
                    self.loop_index += 1
                    self.loop_stack.append(self.loop_index)
                    self._add_asm_opcode(LOOP_START.format(self.loop_index))
                case ']':
                    self._add_asm_opcode(LOOP_END.format(self.loop_stack.pop()))
        assert not self.loop_stack

    def load_template(self):
        with open(TEMPLATE_FILENAME) as temp_fd:
            self.template = temp_fd.read()

    def save(self, fd):
        result = self.template.format(
            MEMORY_SIZE=hex(MEMORY_SIZE),
            CODE=self.asm_code
        )
        fd.write(result)


if __name__ == '__main__':
    import sys

    parser = argparse.ArgumentParser(description='BrainFuck to amd64 assembler translator')
    parser.add_argument('-i', '--in',
                        dest='brainfuck_input',
                        type=argparse.FileType('r'),
                        help='Input brainfuck source filename',
                        required=True
                        )
    parser.add_argument('-o', '--out',
                        dest='asm_output',
                        nargs='?',
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='Output asm file (default stdout)'
                        )
    parser.add_argument('-c', '--compile',
                        dest='bin_output',
                        type=pathlib.Path,
                        help='Compile asm (required nasm)'
                        )
    args = parser.parse_args()

    translator = Translator()
    translator.load_bf_code(args.brainfuck_input)
    translator.translate()
    translator.load_template()
    if not (args.bin_output and args.asm_output == sys.stdout):
        translator.save(args.asm_output)
    if args.bin_output:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.asm') as tmp_file:
            translator.save(tmp_file)
            tmp_file.flush()
            compile(tmp_file.name, args.bin_output)
