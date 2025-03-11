bytes = [0xE1, 0xA7, 0x1E, 0xF8, 0x75, 0x23, 0x7B, 0x61, 0xB9, 0x9D,
         0xFC, 0x5A, 0x5B, 0xDF, 0x69, 0xD2, 0xFE, 0x1B, 0xED, 0xF4,
         0xED, 0x67, 0xF4]
flag = [0] * 27
k = 0
currentChar = 0

for i in range(23):
    for j in range(8):
        if k == 0:
            k = 1
        bit = (bytes[i] >> (7 - j)) & 1
        flag[currentChar] |= bit << (7 - k)
        k += 1
        if k == 8:
            k = 0
            currentChar += 1

flag_str = ''.join(chr(b) for b in flag)
print(flag_str)