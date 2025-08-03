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
            # 0x6XNN
            X = (opcode & 0x0F00) >> 8
            NN = opcode & 0x00FF
            self.V[X] = NN
            self.PC += 2
        elif (opcode & 0xF000) >> 12 == 7:
            # 0x7XNN
            X = (opcode & 0x0F00) >> 8
            NN = opcode & 0x00FF
            self.V[X] += NN
            self.PC += 2

        elif (opcode & 0xF000) >> 12 == 0xA:
            # 0xANNN
            NNN = opcode & 0x0FFF
            self.i = NNN
            self.PC += 2

        elif (opcode & 0xF000) >> 12 == 1:
            # 0x1NNN
            NNN = opcode & 0x0FFF
            self.PC = NNN


        elif (opcode & 0xF000) >> 12 == 3:
            # 0x3XNN
            X = (opcode & 0x0f00) >> 8
            NN = opcode & 0x00ff
            if self.V[X] == NN:
                self.PC += 4
            else:
                self.PC += 2

        elif (opcode & 0xF000) >> 12 == 4:
            # 0x4XNN
            X = (opcode & 0x0f00) >> 8
            NN = opcode & 0x00ff
            if self.V[X] != NN:
                self.PC += 4
            else:
                self.PC += 2

        elif (opcode & 0xF000) >> 12 == 5:
            # 0x5XY0
            X = (opcode & 0x0f00) >> 8
            Y = (opcode & 0x00f0) >> 4
            if self.V[X] == self.V[Y]:
                self.PC += 4
            else:
                self.PC += 2

        elif (opcode & 0xF000) >> 12 == 9:
            # 0x9XY0
            X = (opcode & 0x0f00) >> 8
            Y = (opcode & 0x00f0) >> 4
            if self.V[X] != self.V[Y]:
                self.PC += 4
            else:
                self.PC += 2

        elif (opcode & 0xF000) >> 12 == 2:
            # 0x2NNN
            NNN = opcode & 0x0FFF
            self.stack.append(self.PC)
            self.PC = NNN

        elif opcode == 0x00EE:
            popped_value = self.stack[-1]
            self.stack.pop(-1)
            self.PC = popped_value + 2

        elif ((opcode & 0xF000) >> 12 == 8) and  (opcode & 0x000F) == 0x0:
            # 0x8XY0
            X = (opcode & 0x0f00) >> 8
            Y = (opcode & 0x00f0) >> 4
            self.V[X] = self.V[Y]
            self.PC += 2

        elif ((opcode & 0xF000) >> 12 == 8) and  (opcode & 0x000F) == 0x1:
            # 0x8XY1
            X = (opcode & 0x0f00) >> 8
            Y = (opcode & 0x00f0) >> 4
            self.V[X] = self.V[X] | self.V[Y]
            self.PC += 2

        elif ((opcode & 0xF000) >> 12 == 8) and  (opcode & 0x000F) == 0x2:
            # 0x8XY2
            X = (opcode & 0x0f00) >> 8
            Y = (opcode & 0x00f0) >> 4
            self.V[X] = self.V[X] & self.V[Y]
            self.PC += 2

        elif ((opcode & 0xF000) >> 12 == 8) and  (opcode & 0x000F) == 0x3:
            # 0x8XY3
            X = (opcode & 0x0f00) >> 8
            Y = (opcode & 0x00f0) >> 4
            self.V[X] = self.V[X] ^ self.V[Y]
            self.PC += 2

        elif ((opcode & 0xF000) >> 12 == 8) and  (opcode & 0x000F) == 0x4:
            # 0x8XY4
            X = (opcode & 0x0f00) >> 8
            Y = (opcode & 0x00f0) >> 4
            self.V[X] += self.V[Y]
            if self.V[X] > 0xFF:
                self.V[15] = 1
            self.PC += 2

        elif ((opcode & 0xF000) >> 12 == 8) and  (opcode & 0x000F) == 0x5:
            # 0x8XY5
            X = (opcode & 0x0f00) >> 8
            Y = (opcode & 0x00f0) >> 4
            if self.V[X] >= self.V[Y]:
                self.V[15] = 1
            else:
                self.V[15] = 0
            self.V[X] -= self.V[Y]
            self.PC += 2

        elif ((opcode & 0xF000) >> 12 == 8) and  (opcode & 0x000F) == 0x7:
            # 0x8XY7
            X = (opcode & 0x0f00) >> 8
            Y = (opcode & 0x00f0) >> 4
            if self.V[Y] >= self.V[X]:
                self.V[15] = 1
            else:
                self.V[15] = 0
            self.V[X] = self.V[Y] - self.V[X]
            self.PC += 2

        elif ((opcode & 0xF000) >> 12 == 8) and (opcode & 0x000F) == 0x6:
            X = (opcode & 0x0f00) >> 8
            self.V[15] = self.V[X] & 0x1
            self.V[X] = self.V[X] >> 1
            self.PC += 2

        elif ((opcode & 0xF000) >> 12 == 8) and (opcode & 0x000F) == 0xE:
            X = (opcode & 0x0f00) >> 8
            self.V[15] = (self.V[X] & 0x80) >> 7
            self.V[X] = (self.V[X] << 1) & 0xFF
            self.PC += 2













