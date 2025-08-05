import cpu

chip = cpu.CPU()

chip.V[4] = 7
chip.keys[7] = 0

chip.memory[0x200] = 0xE4
chip.memory[0x201] = 0xA1

opcode = chip.fetch_opcode()


chip.decode_and_execute(opcode)

print(hex(chip.PC))

chip.memory[0x202] = 0x60
chip.memory[0x203] = 0x00

opcode = chip.fetch_opcode()


chip.decode_and_execute(opcode)

print(hex(chip.PC))

