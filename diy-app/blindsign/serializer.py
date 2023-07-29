from embit.psbt import DerivationPath, ser_string, read_string
from embit.ec import Signature
from io import BytesIO
from binascii import a2b_base64, hexlify

PREFIX = b"notpsbt"

# tags for encoding/decoding the data:
# notpsbt - prefix
# each message block is separated by 00
# fields are encoded like in psbt
# 00: separator
# 01: ecdsa message to sign (32-byte message)
# 02: derivation path as in psbt (4-byte fingerprint followed by indexes 4 bytes each)
# 03: input index (mostly used for reconstruction - 4 byte little endian)
# 04...: future extensions (i.e. schnorr sign message etc)


def serialize(stream, payload: list) -> int:
    stream.write(PREFIX)
    count = 0
    for data in payload:
        count += serialize_one(stream, **data)
    return count


def serialize_one(
    stream,
    message=None,
    derivation=None,
    input_index=None,
    signature=None,
) -> int:
    """
    Serialize message and derivation path to stream, returns number of bytes written
    """
    count = 0
    if message is not None:
        count += stream.write(b"\x01")
        count += ser_string(stream, message)
    if derivation is not None:
        count += stream.write(b"\x02")
        count += ser_string(stream, derivation.serialize())
    if input_index is not None:
        count += stream.write(b"\x03")
        count += ser_string(stream, input_index.to_bytes(4, "little"))
    if signature is not None:
        count += stream.write(b"\x04")
        count += ser_string(stream, signature.serialize())
    count += stream.write(b"\x00")
    return count


def parse_one(stream) -> dict:
    """
    Read one message and derivation path from stream
    """
    r = stream.read(1)
    if not r:
        return None
    obj = {}
    while r != b"\x00":
        if r == b"\x01":
            msg = read_string(stream)
            assert len(msg) == 32
            obj["message"] = msg
        elif r == b"\x02":
            derbytes = read_string(stream)
            obj["derivation"] = DerivationPath.parse(derbytes)
        elif r == b"\x03":
            obj["input_index"] = int.from_bytes(read_string(stream), "little")
        elif r == b"\x04":
            obj["signature"] = Signature.parse(read_string(stream))
        else:
            raise KeyError("Invlid key %s" % hexlify(r))
        r = stream.read(1)
    return obj


def parse(payload):
    """Read all messages+derivations from payload"""
    if isinstance(payload, str):
        payload = a2b_base64(payload)
    s = BytesIO(payload)
    assert s.read(len(PREFIX)) == PREFIX
    parsed = []
    while True:
        p = parse_one(s)
        if p is None:
            return parsed
        parsed.append(p)
