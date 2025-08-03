import cpu

chip = cpu.CPU()

chip.V[3] = 10

chip.memory[0x200] = 0x12
chip.memory[0x201] = 0x34

opcode = chip.fetch_opcode()

chip.decode_and_execute(opcode)

print("PC = ", hex(chip.PC))
