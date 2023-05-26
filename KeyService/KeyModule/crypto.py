from KeyModule import hashlib, hashes, rsa, padding, ec, serialization, base64, file_path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import BestAvailableEncryption
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

with open(file_path, 'r') as f:
    # Write the connection string to the file
    first_line = f.readline()

def SignWithPrivateKey(private_key_pem, message):
    # Load the private key from the PEM string
    if is_private_key_unencrypted(private_key_pem):
        private_key = serialization.load_pem_private_key(
            private_key_pem, password=None, backend=default_backend())
    else:
        private_key = serialization.load_pem_private_key(
            private_key_pem, password=first_line.encode('utf-8'), backend=default_backend())

    # Convert message to bytes
    messageBytes = message.encode('utf-8')

    # Sign the message using the private key
    signature = private_key.sign(
        messageBytes, ec.ECDSA(hashes.SHA256()))

    # Convert the signature to a hexadecimal string
    hex_signature = signature.hex()

    # Return the signature as a string
    return f"{message}#{hex_signature}"

def is_private_key_unencrypted(private_key_pem):
    try:
        serialization.load_pem_private_key(private_key_pem, password=None)
        return True  # Private key is not password-protected
    except ValueError as e:
        if str(e) == "Private key is encrypted.":
            return False  # Private key is password-protected
        else:
            raise  # Reraise other ValueError exceptions

from cryptography.fernet import Fernet

def ECCKeyGenerator():
    try:
        # Generate key pair
        private_key = ec.generate_private_key(ec.SECP256R1())
        public_key = private_key.public_key()

        passphrase = first_line  # Replace with your desired passphrase
        encryption_algorithm = BestAvailableEncryption(passphrase.encode('utf-8'))
        # Serialize private key to PEM format
        private_key_pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                    format=serialization.PrivateFormat.PKCS8,
                                                    encryption_algorithm=encryption_algorithm)

        # Serialize public key to DER format
        public_key_der = public_key.public_bytes(encoding=serialization.Encoding.DER,
                                                 format=serialization.PublicFormat.SubjectPublicKeyInfo)

        # Trim the public key to 64 bytes
        public_key_64_bytes = public_key_der[-64:]

        # Convert the public key to PEM format
        public_key_pem = b'-----BEGIN PUBLIC KEY-----\n' + base64.b64encode(public_key_64_bytes).replace(b'\n', b'') + b'\n-----END PUBLIC KEY-----\n'

        # Return the encrypted private and public keys
        return private_key_pem, public_key_pem
    except ValueError as ve:
        print("Error while generating ECC key pair: " + str(ve))
    except Exception as error:
        print("Error while generating ECC key pair: " + str(error))


    # Return None values if an error occurs
    return None, None

def RSAKeyGenerator():
    try:
        # Generate key pair with a key size of 512 bits (64 bytes)
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=512)
        public_key = private_key.public_key()

        # Validate keys
        if not private_key:
            raise ValueError("Private key is empty")
        if not public_key:
            raise ValueError("Public key is empty")

        # Serialize keys to PEM format
        private_key_pem = private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())
        public_key_pem = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

        # Return keys
        return private_key_pem, public_key_pem
    except ValueError as ve:
        print("Error while generating RSA key pair: " + str(ve))
    except Exception as error:
        print("Error while generating RSA key pair: " + str(error))

    # Return None values if an error occurs
    return None, None

def PemToHash(object):     
    sha256_hash = hashlib.sha256(object)
    return sha256_hash.digest()

def HashToPem(value, type):
    key_bytes = value
    pem_key = "-----BEGIN {} KEY-----\n{}\n-----END {} KEY-----\n".format(type, base64.b64encode(key_bytes).decode(), type)
    return pem_key