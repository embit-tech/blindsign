from .serializer import serialize_one, serialize
from io import BytesIO
from binascii import b2a_base64


def sigs_to_message(sigs):
    """
    Encode signatures into message
    """
    s = BytesIO()
    serialize(s, [])
    for data in sigs:
        serialize_one(s, **data)
    return b2a_base64(s.getvalue()).decode().strip()
