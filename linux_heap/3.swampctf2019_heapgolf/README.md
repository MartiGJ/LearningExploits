# SwampCTF 2019 - Heap Golf
We use heap grooming to get a desired value into a pointer. The objective is to call **win_func**.

## Binary
### Code
Decompiled with Binary Ninja HLIL.

```c
int32_t main(int32_t argc, char** argv, char** envp)

  void* fsbase
  int64_t canary = *(fsbase + 0x28)
  int64_t green_0 = malloc(0x20)
  write(0, 0x400975, 0x1a)  {"target green provisioned.\n"}
  int64_t green_array
  *(&green_array + 0) = green_0
  int32_t index = 1
  write(0, 0x400990, 0x30)  {"enter -1 to exit simulation, -2 …"}
  while (true)
      write(0, 0x4009c1, 0x1c)  {"Size of green to provision: "}
      void input
      read(1, &input, 4)
      int32_t size = atoi(&input):0.d
      if (size == -1)
          break
      if (size == -2)
          for (int32_t i = 0; i s< index; i = i + 1)
              free(*(&green_array + (sx.q(i) << 3)))
          green_array = malloc(0x20)
          write(0, 0x400975, 0x1a)  {"target green provisioned.\n"}
          index = 1
      else
          int32_t* green_n = malloc(sx.q(size))
          *green_n = index
          *(&green_array + (sx.q(index) << 3)) = green_n
          index = index + 1
          if (index == 0x30)
              write(0, 0x4009de, 0x19)  {"You're too far under par."}
              break
      if (*green_0 == 4)
          win_func()
  if ((canary ^ *(fsbase + 0x28)) == 0)
      return 0
  __stack_chk_fail()
  noreturn

```


### Security 
NX and stack canaries enabled.

```shell
$ checksec ./heap_golf1 
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

## Solution
Allocate a heap chunk of the same size of *green_0*, 0x20, and then free them. When it automatically allocates the first green in our *green_array* it will return a pointer to the heap chunk we allocated. Now we just need to allocate chunks of sizes far away from 0x20 until the index is equal to our desired value, 4. When we now allocate a chunk of size 0x20 it will return the same chunk used previously for *green_0* and call **win_func**.


### Heap chunks at the start
```
gef➤  heap chunks
Chunk(addr=0x602010, size=0x290, flags=PREV_INUSE)
    [0x0000000000602010     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
Chunk(addr=0x6022a0, size=0x30, flags=PREV_INUSE)
    [0x00000000006022a0     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
Chunk(addr=0x6022d0, size=0x20d40, flags=PREV_INUSE)  ←  top chunk
```
We have *green_0* at 0x6022a0.

### Heap chunks after first allocation
```
gef➤  heap chunks
Chunk(addr=0x602010, size=0x290, flags=PREV_INUSE)
    [0x0000000000602010     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
Chunk(addr=0x6022a0, size=0x30, flags=PREV_INUSE)
    [0x00000000006022a0     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
Chunk(addr=0x6022d0, size=0x30, flags=PREV_INUSE)
    [0x00000000006022d0     01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
Chunk(addr=0x602300, size=0x20d10, flags=PREV_INUSE)  ←  top chunk
```
We have another chunk with the same size and containing the value 1.

### Heap chunks after free and automatic allocation
```
gef➤  heap bins
─────────────────────────────────── Tcachebins for arena 0x7ffff7fb0b80 ───────────────────────────────────
Tcachebins[idx=9, size=0xb0] count=0  ←  Chunk(addr=0x6022a0, size=0x30, flags=PREV_INUSE) 

gef➤  heap chunks
Chunk(addr=0x602010, size=0x290, flags=PREV_INUSE)
    [0x0000000000602010     00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
Chunk(addr=0x6022a0, size=0x30, flags=PREV_INUSE)
    [0x00000000006022a0     00 00 00 00 00 00 00 00 10 20 60 00 00 00 00 00    ......... `.....]
Chunk(addr=0x6022d0, size=0x30, flags=PREV_INUSE)
    [0x00000000006022d0     a0 22 60 00 00 00 00 00 00 00 00 00 00 00 00 00    ."`.............]
Chunk(addr=0x602300, size=0x20d10, flags=PREV_INUSE)  ←  top chunk
```
The chunk that was *green_0*, 0x6022a0, is now in the Tcachebin and the chunk we created, 0x6022d0, is now allocated.

(The binary does not clean the data received from malloc so the chunk allocated automatically still contains a pointer to the next free chunk in the Tcachebin. I also believe that 0x6022a0 should not appear in the command *"heap chunks"* from gef and that it is a mistake.)

### Heap chunks after 3 allocations of sizes away from 0x20
```
gef➤  heap chunks
Chunk(addr=0x602010, size=0x290, flags=PREV_INUSE)
    [0x0000000000602010     00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
Chunk(addr=0x6022a0, size=0x30, flags=PREV_INUSE)
    [0x00000000006022a0     00 00 00 00 00 00 00 00 10 20 60 00 00 00 00 00    ......... `.....]
Chunk(addr=0x6022d0, size=0x30, flags=PREV_INUSE)
    [0x00000000006022d0     a0 22 60 00 00 00 00 00 00 00 00 00 00 00 00 00    ."`.............]
Chunk(addr=0x602300, size=0x70, flags=PREV_INUSE)
    [0x0000000000602300     01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
Chunk(addr=0x602370, size=0x70, flags=PREV_INUSE)
    [0x0000000000602370     02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
Chunk(addr=0x6023e0, size=0x70, flags=PREV_INUSE)
    [0x00000000006023e0     03 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
Chunk(addr=0x602450, size=0x20bc0, flags=PREV_INUSE)  ←  top chunk
```
We can see 3 more chunks containing values from 1, 2 and 3.

### Heap chunks after allocating chunk of size 0x20
```
gef➤  heap chunks
Chunk(addr=0x602010, size=0x290, flags=PREV_INUSE)
    [0x0000000000602010     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
Chunk(addr=0x6022a0, size=0x30, flags=PREV_INUSE)
    [0x00000000006022a0     04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
Chunk(addr=0x6022d0, size=0x30, flags=PREV_INUSE)
    [0x00000000006022d0     a0 22 60 00 00 00 00 00 00 00 00 00 00 00 00 00    ."`.............]
Chunk(addr=0x602300, size=0x70, flags=PREV_INUSE)
    [0x0000000000602300     01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
Chunk(addr=0x602370, size=0x70, flags=PREV_INUSE)
    [0x0000000000602370     02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
Chunk(addr=0x6023e0, size=0x70, flags=PREV_INUSE)
    [0x00000000006023e0     03 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
Chunk(addr=0x602450, size=0x20bc0, flags=PREV_INUSE)  ←  top chunk
```
We got served the chunk that was in the Tcachebin, 0x6022a0, and it now contains the value 4. So we finally get to the **win_func** and get our flag.
