import cpu

chip = cpu.CPU()

chip.V[2] = 15
chip.V[3] = 15

chip.memory[0x200] = 0x24
chip.memory[0x201] = 0x50

opcode = chip.fetch_opcode()

chip.decode_and_execute(opcode)

print("PC = ", hex(chip.PC))
print("Stack[-1] = ", hex(chip.stack[-1]))

chip.memory[0x450] = 0x00
chip.memory[0x451] = 0xEE

opcode = chip.fetch_opcode()

chip.decode_and_execute(opcode)

print("PC = ", hex(chip.PC))
