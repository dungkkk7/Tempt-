from Crypto.Util.number import long_to_bytes

N = 20458249107558484820216545706896249757905561045291495508525940172856922433923496943969041717181454400698171565340718039793745892946219879991687337579840278
e = 65537
c = 227961835385147686950614455546966739282916340691276460084611342294548757968592394619708238422044017136396706229325817648858306706040807296846858939744037

# Factor N into p=2 and q=N//2
q = N // 2
phi = q - 1

# Compute the private exponent d
d = pow(e, -1, phi)

# Decrypt the ciphertext
m = pow(c, d, N)

# Convert the plaintext to bytes and print
print(long_to_bytes(m).decode('utf-8'))


from Crypto.Util.number import long_to_bytes

N = 20458249107558484820216545706896249757905561045291495508525940172856922433923496943969041717181454400698171565340718039793745892946219879991687337579840278
e = 65537
c = 227961835385147686950614455546966739282916340691276460084611342294548757968592394619708238422044017136396706229325817648858306706040807296846858939744037

# Factor N into p=2 and q=N//2
q = N // 2
phi = q - 1

# Compute the private exponent d
d = pow(e, -1, phi)

# Decrypt the ciphertext
m = pow(c, d, N)

# Convert the plaintext to bytes and print
print(long_to_bytes(m).decode('utf-8'))



# Explanation
# Factorization: By recognizing that N is even, we immediately know one of the primes (p) is 2. The other prime (q) is found by dividing N by 2.

# Euler's Totient Function: With p=2 and q=N/2, φ(N) is calculated as q-1 because φ(N) = (p-1)*(q-1).

# Modular Inverse: The private exponent d is computed using Python's built-in pow function with three arguments to efficiently find the modular inverse of e modulo φ(N).

# Decryption: The ciphertext is decrypted using modular exponentiation, converting the resulting long integer back to bytes to reveal the flag.

# This approach leverages the weakness in the RSA modulus being even, allowing us to factorize it quickly and decrypt the message efficiently.