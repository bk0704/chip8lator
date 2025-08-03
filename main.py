import cpu

chip = cpu.CPU()

chip.V[2] = 0xAA
chip.V[3] = 0xCC

chip.memory[0x200] = 0x82
chip.memory[0x201] = 0x33

opcode = chip.fetch_opcode()

chip.decode_and_execute(opcode)

print("V[2] = ", bin(chip.V[2]))
print("V[3] = ", bin(chip.V[3]))
