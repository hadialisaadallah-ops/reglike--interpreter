import sys


def run_file(filepath):
    try:
        with open(filepath, 'r') as file:
            program = file.read().strip().split('\n')
    except FileNotFoundError:
        print(f"Error: Could not find {filepath}")
        return

    registers = {}
    pc = 0

    while pc < len(program):
        line = program[pc].strip()

        # Skip empty lines
        if not line:
            pc += 1
            continue

        if line.startswith("a"):
            reg_list = line[1:].split()
            message = ""
            for r_str in reg_list:
                reg_id = int(r_str)
                message += chr(registers.get(reg_id, 0))
            print(message)
            pc += 1

        elif "=" in line:
            parts = line.split("=")
            reg = int(parts[0].strip())
            val_str = parts[1].strip()

            if val_str == "i":
                user_val = input(f"Enter a number for Register {reg}: ")
                registers[reg] = int(user_val)
            else:
                registers[reg] = int(val_str)
            pc += 1


        else:
            args = [int(x) for x in line.split()]

            if len(args) == 1:  # INC
                reg = args[0]
                registers[reg] = registers.get(reg, 0) + 1
                pc += 1

            elif len(args) == 2:  # JZDEC
                reg = args[0]
                jump_target = args[1] - 1

                if registers.get(reg, 0) == 0:
                    pc = jump_target
                else:
                    registers[reg] = registers.get(reg, 0) - 1
                    pc += 1

    if registers:
        # Find the highest register used so we can print in order (0, 1, 2...)
        max_reg = max(registers.keys())
        final_numbers = []
        for i in range(max_reg + 1):
            final_numbers.append(str(registers.get(i, 0)))
        print(" ".join(final_numbers))
    else:
        print("0")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python reglike.py <filename.rglk>")
    else:
        run_file(sys.argv[1])
