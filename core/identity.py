import os
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import base58


def generate_identity(passphrase: str, filepath: str = "identity.pem") -> str:
    """Generates a new Ed25519 keypair, saves it to an encrypted PEM file, and returns the DID."""
    private_key = ed25519.Ed25519PrivateKey.generate()

    # Encrypt the PEM if passphrase is provided
    encryption_algo = (
        serialization.BestAvailableEncryption(passphrase.encode())
        if passphrase
        else serialization.NoEncryption()
    )

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption_algo,
    )

    with open(filepath, "wb") as f:
        f.write(pem)

    return derive_did(private_key)


def import_identity(
    pem_bytes: bytes, passphrase: str, filepath: str = "identity.pem"
) -> str:
    """Imports an existing PEM, verifies it, saves it locally, and returns the DID."""
    password = passphrase.encode() if passphrase else None

    # This will raise an exception if the passphrase is wrong or the PEM is invalid
    private_key = serialization.load_pem_private_key(pem_bytes, password=password)

    # Save the imported PEM to our local filepath
    with open(filepath, "wb") as f:
        f.write(pem_bytes)

    return derive_did(private_key)


def derive_did(private_key) -> str:
    """Derives a did:key:z6Mk... string from an Ed25519 private key."""
    public_key = private_key.public_key()
    pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
    )
    # Multicodec for ed25519 pub is 0xed01
    payload = b"\xed\x01" + pub_bytes
    encoded = base58.b58encode(payload).decode("utf-8")
    return f"did:key:z{encoded}"
