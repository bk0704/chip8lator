import cpu

chip = cpu.CPU()

chip.memory[0x300] = 0xF0
chip.memory[0x301] = 0x90
chip.memory[0x302] = 0xF0
chip.V[1] = 5
chip.V[2] = 10
chip.i = 0x300
chip.memory[0x200] = 0xD1
chip.memory[0x201] = 0x23


opcode = chip.fetch_opcode()


chip.decode_and_execute(opcode)

for row in chip.display:
    print(row)

