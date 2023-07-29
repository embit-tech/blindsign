from embit.psbt import PSBT
from embit.descriptor.arguments import Key
from .serializer import serialize_one, serialize, parse
from io import BytesIO
from binascii import b2a_base64


def psbt_to_message(psbt: PSBT, xpub: Key) -> str:
    """
    Calculate hashes required to sign tx from psbt and xpub key
    and encode them for Specter-DIY
    """
    fgp = xpub.fingerprint
    s = BytesIO()
    # write prefix
    serialize(s, [])
    for i, inp in enumerate(psbt.inputs):
        msg = psbt.sighash(i)
        for _, der in inp.bip32_derivations.items():
            if der.fingerprint == fgp:
                serialize_one(s, message=msg, derivation=der, input_index=i)
                break
    return b2a_base64(s.getvalue()).decode().strip()


def sign_hashes(xprv, payload):
    """
    Sign parsed hashes with root private key
    """
    sigs = []
    fgp = xprv.my_fingerprint
    for data in payload:
        der = data["derivation"]
        idx = data["input_index"]
        msg = data["message"]
        if fgp != der.fingerprint:
            raise ValueError("Not my key")
        prv = xprv.derive(der.derivation)
        sigs.append(dict(input_index=idx, derivation=der, signature=prv.sign(msg)))
    return sigs


def sigs_to_message(sigs):
    """
    Encode signatures into message
    """
    s = BytesIO()
    serialize(s, [])
    for data in sigs:
        serialize_one(s, **data)
    return b2a_base64(s.getvalue()).decode().strip()


def fill_psbt(psbt, sigdata):
    """Fill psbt with signatures"""
    # copy
    psbt = PSBT.parse(psbt.serialize())
    for data in sigdata:
        der = data["derivation"]
        idx = data["input_index"]
        sig = data["signature"]
        inp = psbt.inputs[idx]
        for pub, inpder in inp.bip32_derivations.items():
            if inpder == der:
                inp.partial_sigs[pub] = sig.serialize() + b"\x01"
    return psbt


if __name__ == "__main__":
    from embit.bip32 import HDKey

    # private key
    root = HDKey.from_string(
        "tprv8ZgxMBicQKsPewTDnPnf9XDJg1FSb8GjD9MvmGY2f2sa5ZuenvRVQQQq3vhyxwXkyFd2xZba4Hihj28TpaQSBoJ4W4sxk17meWSEdBcsigd"
    )
    # public key with origin derivation (optional if it's a root key)
    xpub = Key.from_string(
        "[c1684a69/86h/1h/0h]tpubDDYXEiMd73p3d3JhGa3QFKwDhHrcj6C1UYWEHJ9WVZbKZodqkoki"
        "1SQ4ynn9T7ceV9cZQZFqpJtQK3GUwQrBFC8HCNqC3DRDWbjADaceow1"
    )
    # two input transaction
    psbt = PSBT.from_string(
        "cHNidP8BAJoCAAAAAs8n0LXgwM1IwKiH98QteYe9r08meoH7X7HDIw++AWlsAAAAAAD9////+"
        "j6cZgmoRCQNUpSruGRuKjNZuA6IWDwrW7t4j2b4o4UAAAAAAP3///8CqlwuEgEAAAAWABSHeW"
        "4ZxFjKu6HW4dZf7ofEyNTVOQDT+y8BAAAAFgAUtwYkM0N5IkV32qjRNFwa2cuH2Z0AAAAAAAE"
        "AcQIAAAABagAPm0JCffffn3ij8mgP2oEOvha4t5ArdUcEFEOTlu4BAAAAAP3///8Cej4kGAEA"
        "AAAWABSa/YqqtkrflaYxf3vxzInlcSwv9gDh9QUAAAAAFgAUes38dt0/alDlUnu+dFS47oWBp"
        "WdYAAAAAQEfej4kGAEAAAAWABSa/YqqtkrflaYxf3vxzInlcSwv9iIGAqnoqakHfBnMADeL2c"
        "0phstVVgDiM/1EgsBS55GSqR+cGMFoSmlUAACAAQAAgAAAAIABAAAAAgAAAAABAIMCAAAAAQA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/////wJVAP////8CAPIFKgEAAAAWABRu"
        "ToJAF27p16aAFW4IuY8UIo8+MgAAAAAAAAAAJmokqiGp7eL2HD9x0d79P6mZ36NpU3VcaQaJe"
        "ZlitIvr2DaXToz5AAAAAAEBHwDyBSoBAAAAFgAUbk6CQBdu6demgBVuCLmPFCKPPjIiBgOto2"
        "8FEep5r6mjyimA7pS9nhptSoImOJN18qL7+fitJxjBaEppVAAAgAEAAIAAAACAAAAAAAAAAAA"
        "AIgIDx7vLztV8DXIjpGEffyPadYi8D0pMMDG3TH6ZqtZ+Vr8YwWhKaVQAAIABAACAAAAAgAEA"
        "AAAEAAAAACICAqz0P6IH34PR5ryZg26hO1nZHktmJ+5WwS4KoEI/ko/8GMFoSmlUAACAAQAAg"
        "AAAAIAAAAAACwAAAAA="
    )
    print("\n=== Message for Specter-DIY ===\n")
    msg = psbt_to_message(psbt, xpub)
    print("blindsign", msg)
    parsed = parse(msg)
    result = sign_hashes(root, parsed)
    print("\n=== Signatures from Specter-DIY ===\n")
    print(sigs_to_message(result))
    print("\n=== PSBT with signatures ===\n")
    combined = fill_psbt(psbt, result)
    print(combined)
