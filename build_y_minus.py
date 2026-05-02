import sys

# Y- (Y-Minus) 256-Byte Hex Compiler
# Target: x86 16-bit DOS .COM
# SI=Source, DI=Output, BX=VarOffset

hex_data = [
    "BE 82 00",       # [0] MOV SI, 82h (DOS CmdLine)
    "BF 00 10",       # [3] MOV DI, 1000h (Output buffer)
    
    # --- [main_loop] ---
    "AC",             # [6] LODSB
    "3C 00", "74 54", # [7] CMP AL, 0; JZ exit
    
    # --- [*] Pointer Write: *d = v; ---
    "3C 2A",          # [11] CMP AL, '*'
    "75 0E",          # [13] JNZ check_print
    "AC", "E8 34 00", # [15] LODSB (d), CALL get_offset (Offset: 17+34=4B/75)
    "8B 1F",          # [18] MOV BX, [BX] (Get address)
    "AC", "AC",       # [20] LODSB (=), LODSB (v)
    "E8 2C 00",       # [22] CALL get_offset
    "B0 88", "AA",    # [25] Emit: MOV [BX], AL (88 07)
    "B0 07", "AA",    # [29]
    "EB D2",          # [31] JMP main_loop

    # --- [p] Handle Print: p x; ---
    "check_print:",
    "3C 70",          # [33] CMP AL, 'p'
    "75 0C",          # [35] JNZ check_while
    "AC", "AC",       # [37] LODSB (space), LODSB (var)
    "E8 20 00",       # [39] CALL get_offset
    "B0 B4", "AA",    # [42] Emit: MOV AH, 02
    "B0 02", "AA",    # [46]
    "B0 8A", "AA",    # [48] Emit: MOV DL, [BX]
    "B0 17", "AA",    # [52]
    "B0 CD", "AA",    # [54] Emit: INT 21h
    "B0 21", "AA",    # [58]
    "EB BC",          # [60] JMP main_loop

    # --- [w] Handle While: w(x){ ---
    "check_while:",
    "3C 77",          # [62] CMP AL, 'w'
    "75 0C",          # [64] JNZ check_exit
    "AC", "AC",       # [66] LODSB (skip '('), LODSB (get var)
    "E8 07 00",       # [68] CALL get_offset
    "57",             # [71] PUSH DI (Save for patch)
    "B0 83", "AA",    # [72] Emit: CMP [BX], 0
    "B0 3E", "AA",    # [76]
    "B0 74", "AA",    # [78] Emit: JZ
    "47",             # [82] INC DI
    "EB A7",          # [83] JMP main_loop

    # --- [get_offset] Helper ---
    "get_offset:",
    "2C 61",          # [85] SUB AL, 'a'
    "D1 E0",          # [87] SHL AX, 1
    "8B D8",          # [89] MOV BX, AX
    "C3",             # [91] RET

    "check_exit:",
    "3C 7D",          # [92] CMP AL, '}'
    "75 08",          # [94] JNZ done
    "5B",             # [96] POP BX (Get JZ location)
    "89 F8",          # [97] MOV AX, DI
    "29 D8",          # [99] SUB AX, BX
    "88 07",          # [101] MOV [BX], AL (PATCH!)
    "EB 95",          # [103] JMP main_loop
    
    "exit:",
    "CD 20"           # [105] INT 20h
]

def build():
    raw_bytes = bytearray()
    for entry in hex_data:
        parts = entry.split('#')[0].strip().split()
        for p in parts:
            if p.endswith(':'): continue
            raw_bytes.append(int(p, 16))
    with open("Y_minus.com", "wb") as f:
        f.write(raw_bytes)
    print(f"DONE! 'Y_minus.com' is {len(raw_bytes)} bytes.")

if __name__ == "__main__":
    build()
