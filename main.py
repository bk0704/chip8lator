import cpu

chip = cpu.CPU()

chip.V[2] = 0xA0
chip.V[3] = 0x55

chip.memory[0x200] = 0x82
chip.memory[0x201] = 0x31

opcode = chip.fetch_opcode()

chip.decode_and_execute(opcode)

print("V[2] = ", chip.V[2])
print("V[3] = ", chip.V[3])
