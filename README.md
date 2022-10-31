A python based assembler and simulator for course [CSE112 - Computer Organization](http://techtree.iiitd.edu.in/viewDescription/filename?=CSE112)

Code for testing from [GitHub Link](https://github.com/Setu-Gupta/CO_M21_Assignment)

# Instruction Set Architecture

| Opcode |     Instruction      | Semantics                                                                                                     | Syntax             |
| ------ | :------------------: | :------------------------------------------------------------------------------------------------------------ | :----------------- |
| 00000  |       Addition       | Performs reg1 = reg2 + reg3. If the computation overflows, then the overflow flag is set                      | add reg1 reg2 reg3 |
| 00001  |     Subtraction      | Performs reg1 = reg2 - reg3. In case reg3 > reg2, 0 is written to reg1 and overflow flag is set.              | sub reg1 reg2 reg3 |
| 00010  |  Move    Immediate   | Performs reg1 = $Imm where Imm is a 8 bit value.                                                              | mov reg1 $Imm      |
| 00011  |    Move Register     | Performs reg1 = reg2.                                                                                         | mov reg1 reg2      |
| 00100  |         Load         | Loads data from mem_addr into reg1.                                                                           | ld reg1 mem_addr   |
| 00101  |        Store         | Stores data from reg1 to mem_addr.                                                                            | st reg1 mem_addr   |
| 00110  |       Multiply       | Performs reg1 = reg2 x reg3. If the computation overflows, then the overflow flag is set.                     | mul reg1 reg2 reg3 |
| 00111  |        Divide        | Performs reg3/reg4. Stores the quotient in R0 and the remainder in R1.                                        | div reg3 reg4      |
| 01000  |     Right Shift      | Right shifts reg1 by $Imm, where $Imm is an 8 bit value.                                                      | rs reg1 $Imm       |
| 01001  |      Left Shift      | Left shifts reg1 by $Imm, where $Imm is an 8 bit value.                                                       | ls reg1 $Imm       |
| 01010  |     Exclusive OR     | Performs bitwise XOR of reg2 and reg3. Stores the result in reg1.                                             | xor reg1 reg2 reg3 |
| 01011  |          Or          | Performs bitwise OR of reg2 and reg3. Stores the result in reg1.                                              | or reg1 reg2 reg3  |
| 01100  |         And          | Performs bitwise AND of reg2 and reg3. Stores the result in reg1.                                             | and reg1 reg2 reg3 |
| 01101  |        Invert        | Performs bitwise NOT of reg2. Stores the result in reg1.                                                      | not reg1 reg2      |
| 01110  |       Compare        | Compares reg1 and reg2 and sets up the FLAGS register.                                                        | cmp reg1 reg2      |
| 01111  |  Unconditional Jump  | Jump to mem_addr if the less than flag is set (less than flag = 1), where mem_addr is a memory address        | jlt mem_addr       |
| 10001  | Jump If Greater Than | Jump to mem_addr if the greater than flag is set (greater than flag = 1), where mem_addr is a memory address. | jgt mem_addr       |
| 10010  |    Jump If Equal     | Jump to mem_addr if the equal flag is set (equal flag = 1), where mem_addr is a memory address.               | je mem_addr        |
| 10011 |     Halt                 |   Stops the machine from executing until reset                                                                                                            |         hlt           |


Done by:

1. [Deepam Sarmah](mailto:deepam20050@iiitd.ac.in)
2. [Yatish Garg](mailto:yatish20162@iiitd.ac.in)
3. [Aaryansh Agarwal](mailto:aaryaansh20003@iiitd.ac.in)
