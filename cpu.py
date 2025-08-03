class CPU:
    def __init__(self):
        self.memory = [0] * 4096
        self.V = [0] * 16
        self.i = 0
        self.PC = 0x200
        self.stack = []
        self.stackPointer = 0
        self.delay = 0
        self.sound = 0

    def fetch_opcode(self):
        #Get the first byte from the memory,
        #self.PC holds the memory information of the current instruction
        high_byte = self.memory[self.PC]

        #Get the second byte from the memory
        low_byte = self.memory[self.PC + 1]

        #Combine the 2 bytes
        opcode = (high_byte << 8) | low_byte

        return opcode

    def decode_and_execute(self, opcode):
        if (opcode & 0xF000) >> 12 == 6:
            X = (opcode & 0x0F00) >> 8
            NN = opcode & 0x00FF
            self.V[X] = NN
            self.PC += 2
        elif (opcode & 0xF000) >> 12 == 7:
            X = (opcode & 0x0F00) >> 8
            NN = opcode & 0x00FF
            self.V[X] += NN
            self.PC += 2

        elif (opcode & 0xF000) >> 12 == 10:
            NNN = opcode & 0x0FFF
            self.i = NNN
            self.PC += 2

        elif (opcode & 0xF000) >> 12 == 1:
            NNN = opcode & 0x0FFF
            self.PC = NNN

        elif (opcode & 0xF000) >> 12 == 3:
            X = (opcode & 0x0f00) >> 8
            NN = opcode & 0x00ff





