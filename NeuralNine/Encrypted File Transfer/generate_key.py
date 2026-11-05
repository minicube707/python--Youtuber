from Crypto.Cipher import AES

# Define the encryption key and nonce
# Both must be 16 bytes long for this example
key = b"TheNeuralNineKey"
nonce = b"TheNeuralNineNce"

# Create a new AES cipher using EAX mode
cipher = AES.new(key, AES.MODE_EAX, nonce)

# Encrypt the plaintext message
cyphertext = cipher.encrypt(b"Hello World!")


# Display the original plaintext
print("\nText: Hello World!")

# Display the encrypted message
print(f"Encrypted text: {cyphertext}")


# Create a new AES cipher with the same key, nonce and encryption mode
cipher = AES.new(key, AES.MODE_EAX, nonce)

# Decrypt the ciphertext to recover the original message
print(f"Decrypted text: {cipher.decrypt(cyphertext)}")