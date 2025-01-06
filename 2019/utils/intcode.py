def run(code):
    i = 0
    base = 0
    while True:
        try:
            opcode = code[i] % 100
            modes = str(code[i] // 100).zfill(3)[::-1]
            op1 = code[code[i + 1]] if modes[0] == "0" else code[i + 1] if modes[0] == "1" else code[code[i + 1] + base]
            op2 = code[code[i + 2]] if modes[1] == "0" else code[i + 2] if modes[1] == "1" else code[code[i + 2] + base]
            op3 = code[i + 3] + base if modes[2] == "2" else code[i + 3]
            match opcode:
                case 1:
                    code[op3] = op1 + op2
                    i += 4
                case 2:
                    code[op3] = op1 * op2
                    i += 4
                case 3:
                    code[code[i + 1] + base if modes[0] == "2" else code[i + 1]] = yield "input"
                    i += 2
                case 4:
                    yield op1
                    i += 2
                case 5:
                    if op1 != 0:
                        i = op2
                    else:
                        i += 3
                case 6:
                    if op1 == 0:
                        i = op2
                    else:
                        i += 3
                case 7:
                    num = 1 if op1 < op2 else 0
                    code[op3] = num
                    i += 4
                case 8:
                    num = 1 if op1 == op2 else 0
                    code[op3] = num
                    i += 4
                case 9:
                    base += op1
                    i += 2
                case 99:
                    break
                case _:
                    raise StopIteration("Incorrect opcode")
        except IndexError:
            code.extend([0, 0, 0])