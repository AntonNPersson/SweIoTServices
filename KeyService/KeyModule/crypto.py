from KeyModule import hashlib, hashes, rsa, padding, ec, serialization, base64, file_path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
from ecdsa import SigningKey, VerifyingKey
from ecdsa.curves import NIST256p
from ecdsa.keys import sigencode_string
from hashlib import sha256

with open(file_path, 'r') as f:
    # Write the connection string to the file
    first_line = f.readline()

def checkIfKeyIsHex(key):
    try:
        int(key, 16)
        return True
    except ValueError:
        return False
    
def VerifyWithPublicKey(public_key_pem, message, signature):
    # Load the public key from the PEM string
    # Remove leading/trailing whitespace and newlines
    public_key_pem = public_key_pem.strip()

# Load the PEM format public key
    public_key = serialization.load_pem_public_key(public_key_pem.encode())

    # Convert message to bytes
    messageBytes = message.encode('utf-8')

    # Convert the signature to bytes
    signatureBytes = bytes.fromhex(signature)

    # Verify the signature
    try:
        public_key.verify(signatureBytes, messageBytes, ec.ECDSA(hashes.SHA256()))
        return True
    except Exception as e:
        return False
    
def SignWithPrivateKey(private_key_pem, message):
    # Load the private key from the PEM string
    private_key = SigningKey.from_pem(private_key_pem)

    # Convert message to bytes
    messageBytes = message.encode('utf-8')

    # Sign the message using the private key
    signature = private_key.sign(
        messageBytes, hashfunc=sha256, sigencode=sigencode_string)

    # Convert the signature to a hexadecimal string
    hex_signature = signature.hex()
        # Convert the public key to hex format
    public_key_to_pem = convert_to_pem('MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEdELKx2f0XWrjf84hm4kx/45uha3gAf06eNQX2qiFEHfqF3RT4zbwlrl/1fY7wTiad6DodCfnIvYusyPGQMUUlA==')
    print(public_key_to_pem)
    pem = public_key_to_hex(public_key_to_pem)
    print(pem)
    hex = hex_to_public_key(pem)
    print(hex)

        # Convert the hex format back to a public key

    print(str(verify_signature(hex, messageBytes, signature)))

    # Return the signature as a string
    return f"{message}#{hex_signature}"

from cryptography.fernet import Fernet

def verify_signature(public_key, message, signature):
    # Verify the signature using the public key
    try:
        public_key.verify(
            signature,
            message,
            ec.ECDSA(hashes.SHA256())
        )
        return True  # Signature is valid
    except InvalidSignature:
        return False  # Signature is invalid

def ECCKeyGenerator():
    try:
        # Generate private key
        private_key = SigningKey.generate(curve=NIST256p)

        # Validate private key
        if not private_key:
            raise ValueError("Private key is empty")

        # Generate public key
        public_key = private_key.get_verifying_key()

        # Serialize keys to PEM format
        private_key_pem = private_key.to_pem()
        public_key_hex = public_key.to_string().hex()

        # Return keys
        return private_key_pem, public_key_hex

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

def public_key_to_hex(public_key_pem):
    # Deserialize the PEM public key
    public_key_obj = serialization.load_pem_public_key(
        public_key_pem.encode('utf-8'),
        backend=default_backend()
    )

    # Serialize the public key in the desired format
    public_key_bytes = public_key_obj.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )

    # Convert the public key bytes to hex string
    public_key_hex = public_key_bytes.hex()
    return public_key_hex


def convert_to_pem(public_key):
    # Remove the leading 'b' and single quotes from the key string
    key_string = public_key

    # Add the necessary PEM headers and footers
    pem = "-----BEGIN PUBLIC KEY-----\n"
    pem += key_string + "\n"
    pem += "-----END PUBLIC KEY-----"

    return pem

def hex_to_public_key(public_key_hex):
    # Convert the hex string back to bytes
    public_key_bytes = bytes.fromhex(public_key_hex)

    # Create an Elliptic Curve instance using the desired curve
    curve = ec.SECP256R1()  # Replace with your desired curve, such as ec.SECP256K1()

    # Create a public key object from the bytes and the curve
    public_key = ec.EllipticCurvePublicKey.from_encoded_point(curve, public_key_bytes)

    return public_key

