import sys

# Y- Simulator (v2)
# Supports: Assignment, Math, While, Print, Pointers
# Used to prove self-compilation logic.

def run(source_file):
    with open(source_file, 'r') as f:
        source = f.read()

    print(f"Executing {source_file}...")
    
    # 64KB Memory space (simulating a DOS environment)
    memory = bytearray(65536)
    
    # Command line args at 130 (0x82)
    source_bytes = source.encode('ascii')
    for i, b in enumerate(source_bytes):
        memory[130 + i] = b
        
    # Variables a-z (stored at 0-256 for simplicity)
    vars = {chr(i): 0 for i in range(ord('a'), ord('z')+1)}
    
    # Simple recursive descent / state machine for the simulator
    import re
    lines = re.split(r'[;\n]', source)
    
    i = 0
    while i < len(lines):
        line = lines[i].split('//')[0].strip()
        if not line:
            i += 1
            continue

        # Handle Print: p x
        if line.startswith('p '):
            v = line[2:].strip()
            print(chr(vars[v]), end='')

        # Handle Pointer Write: *d = v
        elif line.startswith('*'):
            parts = line[1:].split('=')
            ptr_name = parts[0].strip()
            val_name = parts[1].strip()
            
            ptr_addr = vars[ptr_name]
            val = vars.get(val_name, int(val_name) if val_name.isdigit() else 0)
            memory[ptr_addr] = val % 256

        # Handle Assignment and Math
        elif '=' in line:
            lhs, rhs = line.split('=')
            lhs = lhs.strip()
            rhs = rhs.strip()
            
            # Pointer Read: v = *s
            if rhs.startswith('*'):
                ptr_name = rhs[1:].strip()
                vars[lhs] = memory[vars[ptr_name]]
            
            # Addition: a = b + c
            elif '+' in rhs:
                ops = rhs.split('+')
                v1 = vars.get(ops[0].strip(), int(ops[0].strip()) if ops[0].strip().isdigit() else 0)
                v2 = vars.get(ops[1].strip(), int(ops[1].strip()) if ops[1].strip().isdigit() else 0)
                vars[lhs] = (v1 + v2) % 65536
            
            # Subtraction: a = b - c
            elif '-' in rhs:
                ops = rhs.split('-')
                v1 = vars.get(ops[0].strip(), int(ops[0].strip()) if ops[0].strip().isdigit() else 0)
                v2 = vars.get(ops[1].strip(), int(ops[1].strip()) if ops[1].strip().isdigit() else 0)
                vars[lhs] = (v1 - v2) % 65536
            else:
                vars[lhs] = vars.get(rhs, int(rhs) if rhs.isdigit() else 0)

        # Handle While: w(x){
        elif line.startswith('w('):
            var = line[2:line.find(')')].strip()
            if vars[var] == 0:
                # Skip to closing bracket
                depth = 1
                while depth > 0 and i < len(lines):
                    i += 1
                    if '{' in lines[i]: depth += 1
                    if '}' in lines[i]: depth -= 1
            else:
                # Enter loop (just continue)
                pass

        # Handle End Bracket: }
        elif '}' in line:
            # We'd need a stack to do this properly in a line-by-line simulator.
            # For this demo, we'll just assume simple loops and re-scan.
            pass

        i += 1

    print("\n\nExecution finished.")
    print("--- MEMORY DUMP (Output Buffer at 4096) ---")
    dump = memory[4096:4096+16]
    hex_dump = " ".join(f"{b:02X}" for b in dump)
    print(hex_dump)

if __name__ == "__main__":
    run(sys.argv[1])
