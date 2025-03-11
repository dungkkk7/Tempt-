def affine_decrypt(ciphertext, a=15, b=20):
    a_inv = 7  # Inverse of 15 mod 26
    plaintext = []
    for c in ciphertext:
        if c == 'T':
            plaintext.append(' ')
            continue
        c_num = ord(c) - ord('A')
        p_num = (a_inv * (c_num - b)) % 26
        plaintext_char = chr(p_num + ord('A'))
        plaintext.append(plaintext_char)
    return ''.join(plaintext)

# Example usage with a secret cheese
secret_cheese = "HBMJWGBAOWMUPZB"
decrypted = affine_decrypt(secret_cheese)
print(decrypted.replace(' ', ' '))  # Ensure spaces are visible