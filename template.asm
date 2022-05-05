global _start

section .bss
buffer: resb {MEMORY_SIZE}

section .text
_start:
    MOV rbp, rsp
    MOV rsi, buffer
    MOV rdx, 1   ; message length (getchar, putchar)

{CODE}
    MOV rax, 60  ; exit
    syscall

putchar:
    MOV rax, 1   ; syscall number
    MOV rdi, 1   ; fd
    syscall
    RET

getchar:
    XOR rax, rax ; syscall number
    XOR rdi, rdi ; fd
    syscall
    RET
