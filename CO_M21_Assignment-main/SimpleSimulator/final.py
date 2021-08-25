import matplotlib.pyplot as plt
import numpy as np
import sys

X = []
Y = []
inp = []
R = 8 * [0]
label = {}
M = 270 * [0]
var = {}
cycle = 0

# Build functions
def calc (s):
  return str(int(s, 2)) 

def build_A (s, l):
  return "nvm" + " R" + calc(s[7:10]) + " R" + calc(s[10:13]) + " R" + calc(s[13:16])

def build_B (s, l):
  return "nvm" + " R" + calc(s[5:8]) + " $" + calc(s[8:])

def build_C(s, l):
  return "nvm" + " R" + calc(s[10:13]) + " R" + calc(s[13:])

def build_D(s, l):
  return "nvm" + " R" + calc(s[5:8]) + " " + s[8:]

def build_E(s, l):
  return s

def build_F(s, l):
  return "hlt"

# Printing functions
def line_print (prg_counter):
  global cycle
  print(format(prg_counter, '08b'), end = " ")
  for i in R:
    print(format(i, '016b'), end = " ")
  print(end = "\n")
  Y.append(format(prg_counter, '08b'))
  X.append(cycle)
  cycle += 1

def mem_print ():
  for i in range(0, 256):
    print(format(M[i], '016b'))

# A functions
def add (s, pc):
  R[7] = 0
  A = s.split()
  r1 = int(A[1][1:])
  r2 = int(A[2][1:])
  r3 = int(A[3][1:])
  R[r1] = R[r2] + R[r3]
  if (R[r1] > 255):
    R[7] |= 1 << 3
  line_print(pc)

def sub (s, l):
  R[7] = 0
  A = s.split()
  r1 = int(A[1][1:])
  r2 = int(A[2][1:])
  r3 = int(A[3][1:])
  R[r1] = R[r2] - R[r3]
  if (R[r1] < 0):
    R[r1] = 0
    R[7] |= 1 << 3
  line_print(pc)

def mul (s, pc):
  R[7] = 0
  A = s.split()
  r1 = int(A[1][1:])
  r2 = int(A[2][1:])
  r3 = int(A[3][1:])
  R[r1] = R[r2] * R[r3]
  if (R[r1] > 255):
    R[7] |= 1 << 3
  line_print(pc)

def XOR (s, pc):
  R[7] = 0
  A = s.split()
  r1 = int(A[1][1:])
  r2 = int(A[2][1:])
  r3 = int(A[3][1:])
  R[r1] = R[r2] ^ R[r3]
  line_print(pc)

def OR (s, pc):
  R[7] = 0
  A = s.split()
  r1 = int(A[1][1:])
  r2 = int(A[2][1:])
  r3 = int(A[3][1:])
  R[r1] = R[r2] | R[r3]
  line_print(pc)

def AND (s, pc):
  R[7] = 0
  A = s.split()
  r1 = int(A[1][1:])
  r2 = int(A[2][1:])
  r3 = int(A[3][1:])
  R[r1] = R[r2] & R[r3]
  line_print(pc)

# B functions
def movI (s, pc):
  R[7] = 0
  A = s.split()
  r = int(A[1][1:])
  im = int(A[2][1:])
  R[r] = im
  line_print(pc)

def rs (s, pc):
  R[7] = 0
  A = s.split()
  r = int(A[1][1:])
  im = int(A[2][1:])
  R[r] >>= im
  line_print(pc)

def ls (s, pc):
  R[7] = 0
  A = s.split()
  r = int(A[1][1:])
  im = int(A[2][1:])
  R[r] <<= im
  line_print(pc)

# C functions
def movR (s, pc):
  A = s.split()
  r1 = int(A[1][1:])
  r2 = int(A[2][1:])
  R[r1] = R[r2]
  R[7] = 0
  line_print(pc)

def div (s, pc):
  R[7] = 0
  A = s.split()
  r3 = int(A[1][1:])
  r4 = int(A[2][1:])
  r3 = R[r3]
  r4 = R[r4]
  R[0] = r3 // r4
  R[1] = r3 % r4
  line_print(pc)

def cmp (s, pc):
  A = s.split()
  r1 = int(A[1][1:])
  r2 = int(A[2][1:])
  r1 = R[r1]
  r2 = R[r2]
  R[7] = 0
  if (r1 == r2):
    R[7] |= 1
  elif (r1 > r2):
    R[7] |= 2
  elif (r1 < r2):
    R[7] |= 4
  line_print(pc)

def NOT (s, pc):
  R[7] = 0
  A = s.split()
  r1 = int(A[1][1:])
  r2 = int(A[2][1:])
  R[r1] = ((1 << 16) - 1) ^ R[r2]
  line_print(pc)

# D functions
def ld (s, pc):
  R[7] = 0
  A = s.split()
  r1 = int(A[1][1:])
  mem = A[2]
  R[r1] = M[int(mem, 2)]
  line_print(pc)

def st (s, pc):
  R[7] = 0
  A = s.split()
  r1 = int(A[1][1:])
  mem = A[2]
  M[int(mem, 2)] = R[r1]
  line_print(pc)

# E F functions
def hlt (s, pc):
  R[7] = 0
  line_print(pc)
  mem_print()

def jmp (s, pc):
  R[7] = 0
  line_print(pc)
  nxt = s[8:]
  run(label[nxt][0], label[nxt][1])

def jlt (s, pc):
  b = R[7] >> 2 & 1
  R[7] = 0
  line_print(pc)
  if (b == 1):
    nxt = s[8:]
    run(label[nxt][0], label[nxt][1])

def jgt (s, pc):
  b = R[7] >> 1 & 1
  R[7] = 0
  line_print(pc)
  if (b == 1):
    nxt = s[8:]
    run(label[nxt][0], label[nxt][1])

def je (s, pc):
  b = R[7] & 1
  R[7] = 0
  line_print(pc)
  if (b == 1):
    nxt = s[8:]
    run(label[nxt][0], label[nxt][1])

# Code execution functions
def get_input():
  pc = 0
  for line in sys.stdin:
    line = line.rstrip()
    inp.append([line, pc])
    label[format(pc, '08b')] = [line, pc]
    M[pc] = int(line, 2)
    if (line[:5] == "00100" or line[:5] == "00101"):
      var[line[8:]] = 0
      M[int(line[8:], 2)] = 0
    pc += 1


def run(s, pc):
  op_code = s[:5]
  b = op_dict[op_code][0]
  f = op_dict[op_code][1]
  result = b(s, pc)
  f(result, pc)

op_dict = {
  "00000" : [build_A, add],
  "00001" : [build_A, sub],
  "00010" : [build_B, movI],
  "00011" : [build_C, movR],
  "00100" : [build_D, ld],
  "00101" : [build_D, st],
  "00110" : [build_A, mul],
  "00111" : [build_C, div],
  "01000" : [build_B, rs],
  "01001" : [build_B, ls],
  "01010" : [build_A, XOR],
  "01011" : [build_A, OR],
  "01100" : [build_A, AND],
  "01101" : [build_C, NOT],
  "01110" : [build_C, cmp],
  "01111" : [build_E, jmp],
  "10000" : [build_E, jlt],
  "10001" : [build_E, jgt],
  "10010" : [build_E, je],
  "10011" : [build_F, hlt]
}

def bonus ():
  x = np.array(X)
  y = np.array(Y)
  plt.xticks(range(0, len(y)))
  plt.scatter(x, y)
  plt.xlabel('Cycle Number')
  plt.ylabel('Memory address accessed')
  plt.title('Scatter plot for Bonus question')
  plt.show()

if __name__ == "__main__":
  get_input()
  for x in inp:
    line = x[0]
    pc = x[1]
    run(line, pc)
  bonus()