import os
import pytest
from core.identity import generate_identity


def test_generate_identity(tmp_path):
    test_pem = str(tmp_path / "test_identity.pem")

    # Test generation with no passphrase
    did = generate_identity(passphrase="", filepath=test_pem)

    assert os.path.exists(test_pem)
    assert did.startswith("did:key:z")

    # Test generation with a passphrase
    test_pem_encrypted = str(tmp_path / "test_identity_encrypted.pem")
    did_encrypted = generate_identity(
        passphrase="securepassword", filepath=test_pem_encrypted
    )

    assert os.path.exists(test_pem_encrypted)
    assert did_encrypted.startswith("did:key:z")
