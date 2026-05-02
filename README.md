# Y-
# Y-Minus (Y-)

A 107-byte self-compiling language for DOS.

Y-Minus is an experiment in extreme code golfing and low-level architecture. The entire compiler fits into exactly 107 bytes of x86 16-bit machine code while supporting variables, memory pointers, while loops, and DOS interrupts[cite: 1]. Despite its microscopic size, the language is powerful enough to compile its own source code[cite: 2].

## What It Can Do

The language uses a simplified grammar designed specifically to minimize the compiler's instruction footprint:
*   **Variable Handling:** Supports single-letter variables mapped automatically to memory offsets[cite: 3, 5].
*   **Pointer Operations:** Allows direct memory writing using the `*d = v;` syntax[cite: 1, 2].
*   **Control Flow:** Implements basic `w(x){ ... }` while-loops, which can also be utilized for minimalist conditional logic[cite: 1, 2].
*   **I/O Operations:** Can trigger DOS interrupts for character output via the `p x;` command[cite: 1].
*   **Bootstrapping:** The compiler is capable of processing its own logic to generate a new functional binary[cite: 2].

## How It Is That Small

Hitting the 107-byte mark required aggressive optimization of x86 machine code and stripping away all standard compiler abstractions:
*   **Single-Byte Opcodes:** The main scanning loop relies heavily on the `LODSB` instruction, which fetches a byte and auto-increments the source pointer simultaneously[cite: 1].
*   **Stack-Based Jump Patching:** Instead of using memory structures or symbol tables to track loop bounds, the compiler pushes the current output location (`DI`) to the stack when a loop opens, and pops it to patch the jump distance when it encounters a closing brace[cite: 1].
*   **Single-Pass Execution:** The compiler reads characters directly from the DOS command-line argument buffer (`82h`) and emits hex straight into the output buffer (`1000h`), bypassing the need for an intermediate representation[cite: 1].
*   **Bare-Metal Address Resolution:** Variable memory offsets are calculated on the fly by subtracting the ASCII value of 'a' from the input character and bit-shifting the register[cite: 1].

## Repository Contents

*   `build_y_minus.py`: The Python builder script that contains the raw, commented hex assembly and generates the final `.com` binary[cite: 1].
*   `self_compile.y-`: The source code for the compiler, written entirely in Y-Minus[cite: 2].
*   `y_minus_sim.c` & `y_minus_sim.rs`: High-level simulators written in C and Rust to demonstrate the translation logic and machine code mapping without needing a DOS emulator[cite: 3, 4].
*   `y_minus_sketch.c`: The initial concept sketch outlining the grammar and memory mapping strategy[cite: 5].

- YSU @ismail0098@gmail.com to contact me
