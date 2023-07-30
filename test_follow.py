# https://github.com/timmot/activity-pub-tutorial
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from urllib.parse import urlparse
import base64
import datetime
import requests

import json
import hashlib


recipient_url = "https://otherserver.tld/users/nonbanana"
recipient_inbox = "https://otherserver.tld/inbox"
sender_url = "https://example.com/users/nonbanana"
sender_key = "https://example.com/users/nonbanana#main-key"

activity_id = "https://example.com/users/nonbanana/follows/test"


# The following is to sign the HTTP request as defined in HTTP Signatures.\
with open('private.pem', 'rb') as f:
    private_key_text = f.read() # load from file

private_key = crypto_serialization.load_pem_private_key(
    private_key_text,
    password=None,
    backend=crypto_default_backend()
)

current_date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

recipient_parsed = urlparse(recipient_inbox)
recipient_host = recipient_parsed.netloc
recipient_path = recipient_parsed.path

# Now that the header is set up, we will construct the message
follow_request_message = {
    "@context": "https://www.w3.org/ns/activitystreams",
    "id": activity_id,
    "type": "Follow",
    "actor": sender_url,
    "object": recipient_url
}

# follow_request_message = { ... } # as above
follow_request_json = json.dumps(follow_request_message)
digest = base64.b64encode(hashlib.sha256(follow_request_json.encode('utf-8')).digest())

# signature information is now
signature_text = (
    f'(request-target): post {recipient_path.encode("utf-8")}\n'
    f'digest: SHA-256={digest}\n'
    f'host: {recipient_host.encode("utf-8")}\n'
    f'date: {current_date.encode("utf-8")}'
)

raw_signature = private_key.sign(
    signature_text.encode('utf-8'),
    padding.PKCS1v15(),
    hashes.SHA256()
)

signature_header = (
    f'keyId="{sender_key}",algorithm="rsa-sha256",'
    f'headers="(request-target) digest host date",'
    f'signature="{base64.b64encode(raw_signature).decode("utf-8")}"'
)

headers = {
    'Date': current_date,
    'Content-Type': 'application/activity+json',
    'Host': recipient_host,
    'Digest': "SHA-256="+digest.decode('utf-8'),
    'Signature': signature_header
}

r = requests.post(recipient_inbox, headers=headers, json=follow_request_message)
print(r.status_code)
print(r.text)

