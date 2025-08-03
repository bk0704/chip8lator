import cpu

chip = cpu.CPU()

chip.V[2] = 15
chip.V[3] = 13

chip.memory[0x200] = 0x52
chip.memory[0x201] = 0x30

opcode = chip.fetch_opcode()

chip.decode_and_execute(opcode)

print("PC = ", hex(chip.PC))
