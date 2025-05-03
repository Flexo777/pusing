from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

class CryptoManager:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.load_keys()

    def generate_keys(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
        self.save_keys()

    def save_keys(self):
        # Save private key
        with open('private_key.pem', 'wb') as f:
            f.write(self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        # Save public key
        with open('public_key.pem', 'wb') as f:
            f.write(self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    def load_keys(self):
        try:
            with open('private_key.pem', 'rb') as f:
                self.private_key = serialization.load_pem_private_key(
                    f.read(),
                    password=None,
                    backend=default_backend()
                )
            
            with open('public_key.pem', 'rb') as f:
                self.public_key = serialization.load_pem_public_key(
                    f.read(),
                    backend=default_backend()
                )
        except FileNotFoundError:
            self.generate_keys()

    def encrypt_message(self, message, public_key):
        # Generate random AES key
        aes_key = os.urandom(32)
        iv = os.urandom(16)
        
        # Encrypt message with AES
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padded_message = message + (16 - len(message) % 16) * b' '
        ciphertext = encryptor.update(padded_message) + encryptor.finalize()
        
        # Encrypt AES key with RSA
        encrypted_aes_key = public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Combine IV + encrypted AES key + ciphertext
        return iv + encrypted_aes_key + ciphertext

    def decrypt_message(self, encrypted_data):
        iv = encrypted_data[:16]
        encrypted_aes_key = encrypted_data[16:272]  # 2048-bit RSA = 256 bytes
        ciphertext = encrypted_data[272:]
        
        # Decrypt AES key with RSA
        aes_key = self.private_key.decrypt(
            encrypted_aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Decrypt message with AES
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext.strip()