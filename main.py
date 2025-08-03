import cpu

chip = cpu.CPU()

chip.memory[0x200] = 0x00
chip.memory[0x201] = 0xE0
chip.display[5][10] = 1

opcode = chip.fetch_opcode()

chip.decode_and_execute(opcode)

print(chip.display)
