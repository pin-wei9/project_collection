# CPU 模擬器
# 初始化
registers = {f"R{i}": 0 for i in range(8)}
flags = {"EQ": False}

def get_value(val):
    """取得暫存器或數字的實際值"""
    return registers[val] if val in registers else int(val)

def execute_program(program, labels):
    pc = 0
    while pc < len(program):
        op, args = program[pc]
        
        if op == 'MOV':
            reg, val = args
            registers[reg] = get_value(val)
            
        elif op == 'ADD':
            reg, val = args
            registers[reg] += get_value(val)
            
        elif op == 'SUB':
            reg, val = args
            registers[reg] -= get_value(val)
            
        elif op == 'JMP':
            label = args[0]
            pc = labels[label]
            continue
            
        elif op == 'CMP':
            r1, r2 = args
            flags["EQ"] = (get_value(r1) == get_value(r2))
            
        elif op == 'JE':
            label = args[0]
            if flags["EQ"]:
                pc = labels[label]
                continue
                
        elif op == 'PRINT':
            print(f"{args[0]} = {registers[args[0]]}")
            
        elif op == 'HLT':
            break
            
        else:
            print(f"未知指令: {op}")
            
        pc += 1

def assemble(source_code):
    program = []
    labels = {}
    lines = source_code.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        if ':' in line:
            label, rest = line.split(':', 1)
            labels[label.strip()] = len(program)
            line = rest.strip()
            if not line:
                continue
                
        tokens = line.split()
        op = tokens[0].upper()
        args = [arg.strip(',') for arg in tokens[1:]]
        program.append((op, args))
        
    return program, labels
