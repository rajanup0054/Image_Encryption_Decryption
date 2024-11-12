from Crypto.Cipher import AES
from ecdsa import SigningKey, NIST192p
from hashlib import sha256
import os

def generate_ecc_key_pair():
    """Generate ECC key pair."""
    sk = SigningKey.generate(curve=NIST192p)
    vk = sk.verifying_key
    return sk, vk

def encrypt_image(image, key, encrypted_path):
    """Encrypt the image using AES with ECC-derived key."""
    ecc_private_key, _ = generate_ecc_key_pair()
    derived_key = sha256(key.encode()).digest()[:16]  # Using SHA-256 and truncating to 16 bytes
    aes_cipher = AES.new(derived_key, AES.MODE_EAX)
    image_data = image.read()
    ciphertext, tag = aes_cipher.encrypt_and_digest(image_data)
    
    with open(encrypted_path, 'wb') as f:
        f.write(aes_cipher.nonce + tag + ciphertext)

def verify_encrypted_file(encrypted_file, key, decrypted_image_path):
    """Verify and decrypt the image if the file matches."""
    derived_key = sha256(key.encode()).digest()[:16]
    encrypted_data = encrypted_file.read()
    
    nonce = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]
    aes_cipher = AES.new(derived_key, AES.MODE_EAX, nonce=nonce)

    try:
        image_data = aes_cipher.decrypt_and_verify(ciphertext, tag)
        with open(decrypted_image_path, 'wb') as f:
            f.write(image_data)
        return True
    except (ValueError, KeyError):
        return False
