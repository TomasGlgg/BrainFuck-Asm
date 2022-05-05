global _start

section .bss
buffer: resb {MEMORY_SIZE}

section .text
_start:
    MOV rbp, rsp
    MOV rsi, buffer

{CODE}
    MOV rax, 60  ; exit
    syscall

putchar:
    MOV rax, 1   ; syscall number
    MOV rdi, 1   ; fd
    MOV rdx, 1   ; message length
    syscall
    ret