import cpu

chip = cpu.CPU()

chip.V[2] = 0xB7
chip.V[3] = 0xCC

print("V[2] before = ", bin(chip.V[2]))

chip.memory[0x200] = 0x82
chip.memory[0x201] = 0x36

opcode = chip.fetch_opcode()

chip.decode_and_execute(opcode)

print("V[2] = ", bin(chip.V[2]))
print("V[3] = ", hex(chip.V[3]))
print("V[15] = ", hex(chip.V[15]))
