// Y- (Y-Minus) 256-byte Compiler Sketch
// A "C-like" language that fits in 256 bytes of machine code.

/*
Language Grammar:
  var = value;
  var = var op var;
  r var; (return)

Example:
  a = 1;
  b = 2;
  c = a + b;
  r c;

Machine Code Mapping (x86_64):
- RAX: Accumulator
- RBX: Temporary / Second Operand
- RCX: Variable base pointer (points to a 26-element array)
- Variables a-z: [RCX + (char - 'a')*8]
*/

#include <stdio.h>

void sketch() {
    // A 256-byte compiler loop might look like this in hex:
    // 1. Read char (LHS variable)
    // 2. Skip '='
    // 3. Read char/int (RHS 1) -> MOV RAX, [RCX + offset]
    // 4. Read op ('+', '-', '*', '/')
    // 5. Read char/int (RHS 2) -> ADD RAX, [RCX + offset]
    // 6. Skip ';'
    // 7. Store result -> MOV [RCX + LHS_offset], RAX
    
    // Each of these steps is ~3-5 bytes of machine code.
    // Total for one assignment: ~20 bytes.
    // The "Loop" and "Lexer" logic: ~50 bytes.
    // Total: ~70 bytes.
    
    // We still have ~180 bytes for:
    // - Function headers
    // - Return statements
    // - Basic 'if' (CMP + JZ)
}
