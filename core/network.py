import json
import logging
import requests
import time
import base64
import re
from cryptography.hazmat.primitives import serialization


def _clean_text(text: str) -> str:
    """
    Applies the Technocore single-line sweep:
    Replaces control characters and newlines with spaces, then strips the ends.
    """
    # A simple approximation of replacing Cc, Cf, Cs, Co, Zl, Zp with space
    # \x00-\x1f \x7f-\x9f are control chars (including \n)
    cleaned = re.sub(r"[\x00-\x1f\x7f-\x9f\u2028\u2029]", " ", text)
    # Replace multiple spaces with a single space
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def sign_message(
    private_key_pem: bytes, passphrase: str, room: str, text: str
) -> tuple[str, str, str]:
    """
    Cleans the text, generates a nonce, signs `<room>|<nonce>|<text>`,
    and returns (nonce, cleaned_text, base64url_signature).
    """
    password = passphrase.encode() if passphrase else None

    private_key = serialization.load_pem_private_key(private_key_pem, password=password)

    cleaned_text = _clean_text(text)
    nonce = str(int(time.time() * 1000))

    # Signature covers exactly `<room>|<nonce>|<text>`
    sig_payload = f"{room}|{nonce}|{cleaned_text}".encode("utf-8")
    signature_bytes = private_key.sign(sig_payload)

    # Technocore requires 86 base64url characters, unpadded
    sig_b64url = base64.urlsafe_b64encode(signature_bytes).decode("ascii").rstrip("=")

    return nonce, cleaned_text, sig_b64url


def post_to_technocore(
    did: str,
    room_path: str,
    original_text: str,
    private_key_pem: bytes,
    passphrase: str,
):
    """
    Posts a signed message to a Technocore room (e.g. room_path = '/r/flopii').
    """
    # The room name used in the signature is just 'flopii' or 'lobby', not the full '/r/...'
    # Wait, the spec says `GET /r/<room>` and signature covers `<room>|<nonce>|<text>`.
    # Let's strip the '/r/' for the signature.
    room_name = room_path.replace("/r/", "")

    nonce, text, sig = sign_message(
        private_key_pem, passphrase, room_name, original_text
    )

    payload = {"did": did, "sig": sig, "nonce": nonce, "text": text}

    api_url = f"https://technocore.chat/r/{room_name}"
    logging.info(f"Posting to {api_url}")

    try:
        # We must send JSON body as per llms.txt: POST /r/<room> {"did":..,"sig":..,"nonce":..,"text":..}
        response = requests.post(api_url, json=payload, timeout=10)
        # 422 means duplicate filter, 429 means rate limit, etc.
        try:
            resp_json = response.json()
        except:
            resp_json = {"text": response.text}

        response.raise_for_status()
        return True, resp_json
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to post to Technocore: {e}")
        try:
            error_data = e.response.json()
        except:
            error_data = {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }
        return False, error_data


def fetch_room(room_path: str) -> list:
    """
    Fetches messages from a Technocore room via GET.
    Returns a list of message strings/objects.
    """
    room_name = room_path.replace("/r/", "")
    api_url = f"https://technocore.chat/r/{room_name}"
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        # Technocore returns plain text lines. Each line is a JSON object.
        lines = response.text.strip().split("\n")
        messages = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                # Valid room messages are always JSON objects
                msg_obj = json.loads(line)
                if isinstance(msg_obj, dict):
                    messages.append(msg_obj)
            except json.JSONDecodeError:
                # Ignore protocol headers like "say:", "next:", "(no new messages)", etc.
                continue
        return messages
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch room {room_path}: {e}")
        return []
