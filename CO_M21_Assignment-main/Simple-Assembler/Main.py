# 2020050 - Deepam Sarmah
# 2020162 - Yatish Garg
# 2020003 - Aaryansh Agarwal

import sys
import re

inp = []
V = {} # Dict of variables key = variable name, value = int value
M = {} # Dict of variables key = variable name, value = 8-bit binary number
label = {} # Dict of labels key = binary string, value = [instruction string, line #]

def karna(x, l, s):
  i = SS.index(x)
  e = EE[i]
  f = FF[i]
  e(s, l)
  f(s, l)

def run(s, l):
  A = s.split()
  if (A[0][-1] == ":" and A[0][0:-1].isalnum()):
    new_s = ' '.join(A[1:])
    run(new_s, l)
    return
  if (A[0] in SS):
    karna(A[0], l, s)
    return
  yoo = ["XOR", "OR", "AND", "NOT"]
  if (A[0].upper() in yoo):
    karna(A[0].upper(), l, s)
    return
  if (A[0] == "mov"):
    if (len(A) == 3):
      if (A[2][0] == "$" and A[2][1:].isdecimal()):
        karna("movI", l, s)
        return
      else:
        karna("movR", l, s)
        return
  print("No such instruction! Line # = ", l)
  sys.exit()

def hlt (s, l):
  A = s.split()
  print("1001100000000000", end ="")
  sys.exit()

def err_A (s, l):
  A = s.split()
  if (len(A) != 4):
    err_syntax(l)
  for i in range(1, 4):
    flag_reg_check(A[i], l)

def err_B (s, l):
  A = s.split()
  if (len(A) != 3):
    syntax_error(l)
  flag_reg_check(A[1], l)
  imm_check(A[2], l)

def err_C (s, l):
  A = s.split()
  if (len(A) != 3):
    syntax_error(l)
  for i in range(1, 3):
    flag_reg_check(A[i], l)

def err_D (s, l):
  A = s.split()
  if (len(A) != 3):
    syntax_error(l)
  flag_reg_check(A[1], l)
  var_check(A[2], l)

def err_E (s, l):
  A = s.split()
  if (len(A) != 2):
    err_syntax(l)
  if (chk_in_label(A[1]) == False):
    err_no_label(l)

def err_F (s, l):
  if (s != 'hlt'):
    err_syntax(l)

def err_syntax (l):
  print("Incorrect syntax! Line # = ", l)
  sys.exit()

def err_flag (l):
  print("Illegal use of FLAGS register! Line # = ", l)
  sys.exit()

def err_reg (l):
  print("No such register! Line # = ", l)
  sys.exit()

def err_no_variable (l):
  print("No such variable! Line # = ", l)
  sys.exit()

def err_imm (l):
  print("Error in immutable value! Line # = ", l)
  sys.exit()

def err_label_mem_add (l):
  print("Typos in memory address! Line # = ", l)
  sys.exit()

def err_no_label (l):
  print("No such label with given memory address! Line # = ", l)
  sys.exit()

def jmp (s, l):
  A = s.split()
  print("01111" + ("0" * 3) + label[A[1]])

def jlt (s, l):
  A = s.split()
  print("10000" + ("0" * 3) + label[A[1]])

def jgt (s, l):
  A = s.split()
  print("10001" + ("0" * 3) + label[A[1]])

def je (s, l):
  A = s.split()
  print("10010" + ("0" * 3) + label[A[1]])

def ld (s, l):
  A = s.split()
  r1 = int(A[1][1:])
  mem = A[2]
  R[r1] = V[mem]
  print("00100" + R_bin[r1] + M[mem])

def st (s, l):
  A = s.split()
  r1 = int(A[1][1:])
  mem = A[2]
  V[mem] = R[r1]
  print("00101" + R_bin[r1] + M[mem])

def flag_reg_check (x, l):
  if (x == "FLAGS"):
    err_flag(l)
  if ((x[0] == "R" and x[1] >= "0" and x[1] <= "6") == False):
    err_reg(l)

def imm_check (x, l):
  if (False == (x[0] == '$' and x[1:].isdecimal() and int(x[1:]) in range(0, 256))):
    err_imm(l)

# Code for regex checking of alphanumerical characters and underscores taken from : https://stackoverflow.com/a/16982669
def alpha_score_check (s, l):
  if (None == re.match(r'^\w+$', s)):
    err_syntax(l)

def var_check (s, l):
  alpha_score_check(s, l)
  if (s not in V):
    err_no_variable(l)

def chk_valid_label_mem_add (mem_add):
  return all(c in "10" for c in mem_add) and len(mem_add) == 8

def chk_in_label (s):
  return s in label

def movR (s, l):
  A = s.split()
  r1 = int(A[1][1:])
  r2 = (7 if A[2] == "FLAGS" else int(A[2][1:]))
  R[r1] = R[r2]
  print("00011" + "0" * 5 + R_bin[r1] + R_bin[r2])

def div (s, l):
  A = s.split()
  r3 = int(A[1][1:])
  r4 = int(A[2][1:])
  print("00111" + "0" * 5 + R_bin[r3] + R_bin[r4])
  r3 = R[r3]
  r4 = R[r4]
  R[0] = r3 // r4
  R[1] = r3 % r4

def NOT (s, l):
  A = s.split()
  r1 = int(A[1][1:])
  r2 = int(A[2][1:])
  R[r1] = ~R[r2]
  print("01101" + "0" * 5 + R_bin[r1] + R_bin[r2])

def cmp (s, l):
  A = s.split()
  R[7] = 0
  r1 = int(A[1][1:])
  r2 = int(A[2][1:])
  print("01110" + ("0" * 5) + R_bin[r1] + R_bin[r2])
  r1 = R[r1]
  r2 = R[r2]
  if (r1 == r2):
    R[7] |= 1
  elif (r1 > r2):
    R[7] |= 1 << 1
  elif (r1 < r2):
    R[7] |= 1 << 2

def err_hlt():
  print("Incorrect usage of halt statement!")
  sys.exit()

def hlt_check():
  hlts = 0
  for i in inp:
    A = i.split()
    if len(A) == 1 and i == "hlt":
      hlts += 1
    if (A[0][-1] == ":" and A[0][0:-1].isalnum()):
      if (len(A) == 2 and A[1] == "hlt"):
        hlts += 1;
  if (hlts != 1):
    err_hlt()
  A = inp[-1].split()
  if (len(A) == 2 and A[0][-1] == ":" and A[0][0:-1].isalnum()):
    if (A[1] == "hlt"):
      return
  if (False == (len(A) == 1 and A[0] == "hlt")):
    err_hlt()

def _input():
  for line in sys.stdin:
    line = line.rstrip()
    if (len(line) > 0):
      inp.append(line)
  hlt_check()

def _dicts():
  n = len(inp)
  i = 0
  while (i < n):
    A = inp[i].split()
    if (A[0] != "var"):
      break
    V[A[1]] = 0
    i += 1
  j = 0
  while (i < n):
    A = inp[i].split()
    if (A[0] == "var"):
      err_var()
    if (A[0][-1] == ":" and A[0][0:-1].isalnum()):
      label[A[0][:-1]] = format(j, '08b')
    i += 1
    j += 1
  i = 0
  while (i < n):
    A = inp[i].split()
    if (A[0] != "var"):
      break
    M[A[1]] = format(j, '08b')
    i += 1
    j += 1

def movI (s, l):
  A = s.split()
  r = int(A[1][1:])
  im = int(A[2][1:])
  R[r] = im
  print("00010" + R_bin[r] + format(im, '08b'))

def rs (s, l):
  A = s.split()
  r = int(A[1][1:])
  im = int(A[2][1:])
  R[r] >>= im
  print("01000" + R_bin[r] + format(im, '08b'))

def ls (s, l):
  A = s.split()
  r = int(A[1][1:])
  im = int(A[2][1:])
  R[r] <<= im
  print("01001" + R_bin[r] + format(im, '08b'))

def add (s, l):
  A = s.split()
  r1 = int(A[1][1:])
  r2 = int(A[2][1:])
  r3 = int(A[3][1:])
  R[r1] = R[r2] + R[r3]
  R[7] = 0
  if (R[r1] > 255):
    R[7] |= 1 << 3
  print("00000" + "00" + R_bin[r1] + R_bin[r2] + R_bin[r3])

def sub (s, l):
  A = s.split()
  r1 = int(A[1][1:])
  r2 = int(A[2][1:])
  r3 = int(A[3][1:])
  R[r1] = R[r2] - R[r3]
  R[7] = 0
  if (R[r1] < 0):
    R[r1] = 0
    R[7] |= 1 << 3
  print("00001" + "00" + R_bin[r1] + R_bin[r2] + R_bin[r3])

def mul (s, l):
  A = s.split()
  r1 = int(A[1][1:])
  r2 = int(A[2][1:])
  r3 = int(A[3][1:])
  R[r1] = R[r2] * R[r3]
  R[7] = 0
  if (R[r1] > 255):
    R[7] |= 1 << 3
  print("00110" + "00" + R_bin[r1] + R_bin[r2] + R_bin[r3])

def XOR (s, l):
  A = s.split()
  r1 = int(A[1][1:])
  r2 = int(A[2][1:])
  r3 = int(A[3][1:])
  R[r1] = R[r2] ^ R[r3]
  R[7] = 0
  print("01010" + "00" + R_bin[r1] + R_bin[r2] + R_bin[r3])

def OR (s, l):
  A = s.split()
  r1 = int(A[1][1:])
  r2 = int(A[2][1:])
  r3 = int(A[3][1:])
  R[r1] = R[r2] | R[r3]
  R[7] = 0
  print("01011" + "00" + R_bin[r1] + R_bin[r2] + R_bin[r3])

def AND (s, l):
  A = s.split()
  r1 = int(A[1][1:])
  r2 = int(A[2][1:])
  r3 = int(A[3][1:])
  R[r1] = R[r2] & R[r3]
  R[7] = 0
  print("01100" + "00" + R_bin[r1] + R_bin[r2] + R_bin[r3])

def err_special (s, l):
  A = s.split()
  if (len(A) != 3):
    err_syntax(l)
  flag_reg_check(A[1], l)
  if (False == (A[2] == "FLAGS" or (A[2][0] == "R" and A[2][1] >= "0" and A[2][1] <= "6"))):
    err_syntax(l)

FF = [add, sub, movI, movR, ld, st, mul, div, rs, ls, XOR, OR, AND, NOT, cmp, jmp, jlt, jgt, je, hlt]
EE = [err_A, err_A, err_B, err_special, err_D, err_D, err_A, err_C, err_B, err_B, err_A, err_A, err_A, err_C, err_C, err_E, err_E, err_E, err_E, err_F]
SS = ["add", "sub", "movI", "movR", "ld", "st", "mul", "div", "rs", "ls", "XOR", "OR", "AND", "NOT", "cmp", "jmp", "jlt", "jgt", "je", "hlt"]
R_bin = [format(i, '03b') for i in range(0, 8)]
R = 10 * [0]

if __name__=="__main__":
  _input()
  _dicts()
  l = 1
  for s in inp:
    A = s.split()
    if (A[0] != "var"):
      run(s, l)
    l += 1