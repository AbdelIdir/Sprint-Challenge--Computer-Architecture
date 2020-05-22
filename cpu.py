"""CPU functionality."""
import sys

binary_op = {
    0b00000001: 'HLT',
    0b10000010: 'LDI',
    0b01000111: 'PRN',
    0b01000101: 'PUSH',
    0b01000110: 'POP',
    0b01010000: 'CALL',
    0b00010001: 'RET',
    0b01010100: 'JMP',
    0b01010101: 'JEQ',
    0b01010110: 'JNE',
}
math_op = {
    "ADD": 0b10100000,
    "SUB": 0b10100001,
    "MUL": 0b10100010,
    'CMP': 0b10100111,
    'SHL': 0b10101100,
    'SHR': 0b10101101,
    'MOD': 0b10100100,
    'AND': 0b10101000,
    'OR': 0b10101010,
    'XOR': 0b10101011,
    'NOT': 0b01101001
}
# Stack Pointer
SP = 7


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #memory allocation will be 256
        self.ram = [0] * 0xFF * 256
        # Program Counter 
        self.PC = 0
        # Memory Address Register
        self.MAR = None
        # Memory Data Register
        self.MDR = None
        # This register holds value between 0-255 (total of 256) for 8bites/registers
        self.register = [0] * 8
        self.register[SP] = 0xF4
        self.operand_a = None
        self.operand_b = None
        # Flags
        self.FL = 0b00000000
        # Branch Table
        self.instructions = {}
        self.instructions['HLT'] = self.HALT
        self.instructions['LDI'] = self.LOAD
        self.instructions['PRN'] = self.PRINT
        self.instructions['PUSH'] = self.PUSH
        self.instructions['POP'] = self.POP
        self.instructions['CALL'] = self.CALL
        self.instructions['RET'] = self.RET
        self.instructions['JMP'] = self.JMP
        self.instructions['JEQ'] = self.JEQ
        self.instructions['JNE'] = self.JNE

    def CALL(self):
        """Calls a subroutine (function) at the address stored in the register."""
        self.reg[SP] -= 1
        # assign the address to the instructions
        instruction_address = self.PC + 2
        # push ontu the stack the instructions
        self.ram[self.register[SP]] = instruction_address
        # Assign to Program Counter the address in register
        self.PC = self.register[self.operand_a]

    def RET(self):
        self.PC = self.ram[self.register[SP]]
        self.register[SP] += 1

    def JMP(self):
        """Jump to the address stored in the given register."""
        self.PC = self.register[self.operand_a]

    def JEQ(self):
        """If `equal` flag is set (true), jump to the address stored in the given register."""
        if self.FL & 0b00000001 == 1:
            self.PC = self.register[self.operand_a]
        else:
            self.PC += 2

    def JNE(self):
        """If `E` flag is clear (false, 0), jump to the address stored in the given register."""
        if self.FL & 0b00000001 == 0:
            self.PC = self.register[self.operand_a]
        else:
            self.PC += 2

    def HALT(self):
        """Exit the current program"""
        sys.exit()

    def LOAD(self):
        """Load value to register"""
        self.register[self.operand_a] = self.operand_b

    def PRINT(self):
        """Print the value in a register"""
        print(self.register[self.operand_a])

    def PUSH(self):
        """Push the value in the given register to the top of the stack"""
        # get the Stack Pointer in the local scope
        global SP
        # decrement the Stack Pointer count
        self.register[SP] -= 1
        # pass to register the value at the Stack Pointer address
        self.ram[self.reg[SP]] = self.register[self.operand_a]

    def POP(self):
        """Pop the value at the top of the stack into the given register"""
        # get the Stack Pointer in the local scope
        global SP
        # pass to the register the value at the address pointed by the Stack Pointer
        self.register[self.operand_a] = self.ram[self.register[SP]]
        # increment Stack Pointer count
        self.register[SP] += 1

    def ram_read(self, address):
        """Accepts an address to read and returns the value stored there"""
        self.MAR = address
        self.MDR = self.ram[address]
        return self.ram[address]

    def ram_write(self, value, address):
        """Accepts a value to write, and the address to write it to"""
        self.MAR = address
        self.MDR = value
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""
        if len(sys.argv) != 2:
            print("File name must by included!")
            sys.exit(1)
        filename = sys.argv[1]
        try:
            address = 0
            # open file passed within arguments
            with open(filename) as program:
                # for each instruction in program
                for instruction in program:
                    # remove comments
                    splitted_comment = instruction.strip().split("#")
                    value = splitted_comment[0].strip()
                    if value == "":
                        continue
                    # mutate numbers from string to integers
                    num = int(value, 2)
                    self.ram[address] = num
                    address += 1
        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

 