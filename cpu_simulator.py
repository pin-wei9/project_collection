# 簡易 CPU 模擬器（含單步執行）
# 組譯器
def assemble(source_code):
    program = []
    labels = {}

    lines = source_code.strip().split('\n')

    for line_no, line in enumerate(lines, start=1):
        line = line.strip()

        if not line or line.startswith('#'):
            continue

        # Label
        if ':' in line:
            label, rest = line.split(':', 1)
            labels[label.strip()] = len(program)
            line = rest.strip()
            if not line:
                continue

        tokens = line.split()
        op = tokens[0].upper()
        args = [arg.strip(',') for arg in tokens[1:]]

        program.append((op, args, line_no))

    return program, labels


# CPU
class CPU:
    def __init__(self):
        self.registers = {f"R{i}": 0 for i in range(8)}
        self.flags = {"EQ": False}

    def get_value(self, val):
        if val in self.registers:
            return self.registers[val]
        try:
            return int(val)
        except ValueError:
            raise ValueError(f"無法解析的值: {val}")

    def dump_state(self, pc, op, args):
        regs = " ".join(f"{k}={v}" for k, v in self.registers.items())
        print(f"\nPC={pc}  指令={op} {' '.join(args)}")
        print(regs, f" EQ={self.flags['EQ']}")

    def run(self, program, labels, step=False):
        pc = 0
        self.flags["EQ"] = False

        while pc < len(program):
            op, args, line_no = program[pc]

            # ---- 單步模式 ----
            if step:
                self.dump_state(pc, op, args)
                cmd = input("按 Enter 繼續（q 離開）: ")
                if cmd.lower() == 'q':
                    print("中止執行")
                    break

            try:
                if op == 'MOV':
                    reg, val = args
                    self.registers[reg] = self.get_value(val)

                elif op == 'ADD':
                    reg, val = args
                    self.registers[reg] += self.get_value(val)

                elif op == 'SUB':
                    reg, val = args
                    self.registers[reg] -= self.get_value(val)

                elif op == 'CMP':
                    r1, r2 = args
                    self.flags["EQ"] = (self.get_value(r1) == self.get_value(r2))

                elif op == 'JMP':
                    label = args[0]
                    if label not in labels:
                        raise ValueError(f"未知標籤: {label}")
                    pc = labels[label]
                    continue

                elif op == 'JE':
                    label = args[0]
                    if self.flags["EQ"]:
                        if label not in labels:
                            raise ValueError(f"未知標籤: {label}")
                        pc = labels[label]
                        continue

                elif op == 'PRINT':
                    print(f"輸出: {self.get_value(args[0])}")

                elif op == 'HLT':
                    print("程式結束")
                    break

                else:
                    raise ValueError(f"未知指令: {op}")

            except Exception as e:
                print(f"\n錯誤（assembly 第 {line_no} 行）: {e}")
                break

            pc += 1

# 主程式
if __name__ == "__main__":
    source = """
    # 測試程式：比較兩個數字
    MOV R0, 3
    MOV R1, 5
    ADD R0, 2
    CMP R0, R1
    JE equal
    MOV R2, 0
    JMP end
    equal:
    MOV R2, 1
    end:
    PRINT R2
    HLT
    """

    program, labels = assemble(source)

    cpu = CPU()
    cpu.run(program, labels, step=True)
