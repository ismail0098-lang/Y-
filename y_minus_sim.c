#include <stdio.h>
#include <string.h>

// Minimal "Y-" Compiler Simulator
// This script simulates the logic of a 256-byte machine code compiler.

void emit(const char* name, const char* hex) {
    printf("%-15s : %s\n", name, hex);
}

void compile(const char* source) {
    printf("Compiling: %s\n", source);
    printf("-----------------------------------\n");

    const char* p = source;
    while (*p) {
        if (*p == ' ' || *p == '\n' || *p == '\t') { p++; continue; }

        // Variable assignment: x = 5;
        if (p[1] == '=') {
            char var = p[0];
            int offset = (var - 'a') * 4;
            p += 2; // skip 'x='

            if (p[0] >= '0' && p[0] <= '9') {
                // Constant assignment: x = 5;
                // MOV [RCX + offset], val -> C7 41 offset val
                char hex[32];
                sprintf(hex, "C7 41 %02X %02X 00 00 00", offset, p[0] - '0');
                emit("MOV_CONST", hex);
                p++;
            }
            if (*p == ';') p++;
        }
        
        // Return: r x;
        else if (*p == 'r') {
            p++; // skip 'r'
            while (*p == ' ') p++;
            char var = *p;
            int offset = (var - 'a') * 4;
            
            // MOV EAX, [RCX + offset] -> 8B 41 offset
            char hex[32];
            sprintf(hex, "8B 41 %02X", offset);
            emit("LOAD_EAX", hex);
            
            // RET -> C3
            emit("RET", "C3");
            p++;
            if (*p == ';') p++;
        }
        else {
            p++;
        }
    }
}

int main() {
    compile("a=5; r a;");
    return 0;
}
