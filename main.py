from os import system, remove

MEMORY_START_ADDRESS = 0x402000
MEMORY_SIZE = 0x1000
TEMP_ASM_FILENAME = '.code.asm'
TEMP_OBJ_FILENAME = '.code.o'
TEMPLATE_FILENAME = 'template.asm'


def compile(bin_filename):
    compile_commands = (
        f'nasm -f elf64 {TEMP_ASM_FILENAME} -o {TEMP_OBJ_FILENAME}',
        f'ld -m elf_x86_64 -s -o {bin_filename} {TEMP_OBJ_FILENAME}'
    )
    for command in compile_commands:
        system(command)
    remove(TEMP_ASM_FILENAME)
    remove(TEMP_OBJ_FILENAME)


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

    def load_bf_code(self, filename):
        with open(filename) as bf_fd:
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

    def save(self, filename):
        result = self.template.format(
            MEMORY_SIZE=hex(MEMORY_SIZE),
            MEMORY_START_ADDRESS=hex(MEMORY_START_ADDRESS),
            CODE=self.asm_code
        )
        with open(TEMP_ASM_FILENAME, 'w') as result_fd:
            result_fd.write(result)
        print(result)
        compile(filename)


if __name__ == '__main__':
    from sys import argv
    if len(argv) != 3:
        print('Usage: python3 {} IN_BRAINFUCK OUT_BIN'.format(argv[0]))
        exit(1)
    translator = Translator()
    translator.load_bf_code(argv[1])
    translator.translate()
    translator.load_template()
    translator.save(argv[2])
