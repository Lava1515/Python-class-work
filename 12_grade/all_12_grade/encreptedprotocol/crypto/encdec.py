from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, data):
        # Generate a random IV (Initialization Vector)
        iv = get_random_bytes(16)

        # Create AES cipher
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        # Pad the data to be a multiple of block size
        padded_data = pad(data, AES.block_size)

        # Encrypt the data
        encrypted_data = cipher.encrypt(padded_data)

        # Return the IV and encrypted data
        return iv + encrypted_data

    def decrypt(self, encrypted_data):
        # Extract the IV from the beginning of the encrypted data
        iv = encrypted_data[:16]

        # Extract the actual encrypted data
        actual_encrypted_data = encrypted_data[16:]

        # Create AES cipher
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        # Decrypt the data
        decrypted_data = cipher.decrypt(actual_encrypted_data)

        # Unpad the data
        original_data = unpad(decrypted_data, AES.block_size)

        # Return the original data
        return original_data


# Example usage:
key = get_random_bytes(16)
data_to_encrypt = b'Hello, world!'
cipher = AESCipher(key)
encrypted_result = cipher.encrypt(data_to_encrypt)
decrypted_result = cipher.decrypt(encrypted_result)

print(f"Original data: {data_to_encrypt}")
print(f"Encrypted data: {encrypted_result}")
print(f"Decrypted data: {decrypted_result.decode('utf-8')}")
