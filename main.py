import cpu

chip = cpu.CPU()

chip.V[2] = 0x10

chip.memory[0x200] = 0x42
chip.memory[0x201] = 0x12

opcode = chip.fetch_opcode()

chip.decode_and_execute(opcode)

print("PC = ", hex(chip.PC))
