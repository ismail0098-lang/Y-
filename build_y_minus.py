import sys

# Y- (Y-Minus) 256-Byte Hex Compiler
# Target: x86 16-bit DOS .COM
# SI=Source, DI=Output, BX=VarOffset

hex_data = [
    "BE 82 00",       # [0] MOV SI, 82h (DOS CmdLine)
    "BF 00 10",       # [3] MOV DI, 1000h (Output buffer)
    
    "main_loop:",
    "AC",             # [6] LODSB
    "3C 00", "74 60", # [7] CMP AL, 0; JZ exit
    
    # --- [=] Handle Assignment & Addition: a = b + 1; ---
    "3C 61", "72 20", # [11] CMP AL, 'a'; JB check_pointer
    "E8 40 00",       # [15] CALL get_offset (DX = target var)
    "89 DA",          # [18] MOV DX, BX
    "AC", "AC",       # [20] LODSB (=), LODSB (first operand)
    "E8 38 00",       # [22] CALL get_offset (Get value of b)
    "8A 07",          # [25] MOV AL, [BX]
    "AC",             # [27] Check for '+'
    "3C 2B", "75 04", # [28] CMP AL, '+'; JNZ store
    "AC", "02 07",    # [32] LODSB (second operand), ADD AL, [BX]
    
    "store:",
    "B0 88", "AA",    # [36] Emit: MOV [target], AL
    "89 D0", "AB",    # [40] Emit target address
    "EB CD",          # [42] JMP main_loop

    # --- [*] Pointer Write: *d = v; ---
    "check_pointer:",
    "3C 2A",          # [44] CMP AL, '*'
    "75 0E",          # [46] JNZ check_print
    "AC", "E8 20 00", # [48] LODSB (d), CALL get_offset
    "8B 1F",          # [51] MOV BX, [BX] (Get address)
    "AC", "AC",       # [53] LODSB (=), LODSB (v)
    "E8 18 00",       # [55] CALL get_offset
    "B0 88", "AA",    # [58] Emit: MOV [BX], AL
    "B0 07", "AA",    # [62]
    "EB C0",          # [64] JMP main_loop

    # --- [p] Handle Print: p x; ---
    "check_print:",
    "3C 70",          # [66] CMP AL, 'p'
    "75 0C",          # [68] JNZ check_while
    "AC", "AC",       # [70] LODSB (space), LODSB (var)
    "E8 0C 00",       # [72] CALL get_offset
    "B0 B4", "AA",    # [75] Emit: MOV AH, 02
    "B0 02", "AA",    # [79]
    "B0 8A", "AA",    # [81] Emit: MOV DL, [BX]
    "B0 17", "AA",    # [85]
    "B0 CD", "AA",    # [87] Emit: INT 21h
    "B0 21", "AA",    # [91]
    "EB A3",          # [93] JMP main_loop

    # --- [w] Handle While: w(x){ ---
    "check_while:",
    "3C 77",          # [95] CMP AL, 'w'
    "75 0C",          # [97] JNZ exit
    "AC", "AC",       # [99] LODSB (skip '('), LODSB (get var)
    "E8 F0 FF",       # [101] CALL get_offset (Relative back)
    "57",             # [104] PUSH DI
    "B0 83", "AA",    # [105] Emit: CMP [BX], 0
    "B0 3E", "AA",    # [109]
    "B0 74", "AA",    # [111] Emit: JZ
    "47",             # [115] INC DI
    "EB 86",          # [116] JMP main_loop

    # --- [get_offset] Helper ---
    "get_offset:",
    "2C 61",          # [118] SUB AL, 'a'
    "D1 E0",          # [120] SHL AX, 1
    "8B D8",          # [122] MOV BX, AX
    "C3",             # [124] RET

    "exit:",
    "CD 20"           # [125] INT 20h
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
