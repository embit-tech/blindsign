from app import BaseApp, AppError
from gui.screens import Prompt
from .converter import sigs_to_message
from .serializer import parse
from io import BytesIO
from embit import bip32


class BlindSignApp(BaseApp):
    """
    This app can blindly sign a transaction hash with a private key.
    """

    prefixes = [b"blindsign"]
    name = "blindsign"

    def sign_hashes(self, payload):
        """
        Sign parsed hashes with root private key
        """
        sigs = []
        fgp = self.keystore.fingerprint
        for data in payload:
            der = data["derivation"]
            idx = data["input_index"]
            msg = data["message"]
            if fgp != der.fingerprint:
                raise ValueError("Not my key")
            sig = self.keystore.sign_hash(der.derivation, msg)
            sigs.append(dict(input_index=idx, derivation=der, signature=sig))
        return sigs

    async def process_host_command(self, stream, show_screen):
        """
        If command with one of the prefixes is received
        it will be passed to this method.
        Should return a tuple:
        - stream (file, BytesIO etc)
        - meta object with title and note
        """
        # reads prefix from the stream (until first space)
        prefix = self.get_prefix(stream)
        if prefix not in self.prefixes:
            # WTF? It's not our data...
            raise AppError("Prefix is not valid: %s" % prefix.decode())
        data = stream.read().strip().decode()
        hashes = parse(data)
        keys = {bip32.path_to_str(h["derivation"].derivation) for h in hashes}
        # try to decode with ascii characters
        msg = "\n\nSiging %d hashes\n" % len(hashes)
        msg += "with private keys using derivation paths:\n\n"
        msg += "\n".join(keys)

        scr = Prompt(
            "Sign hashes blindly?",
            msg,
            note="It could be a bitcoin transaction or anything else,\n"
            "and we don't know how much is being sent and where",
        )
        res = await show_screen(scr)
        if res is False:
            return None
        sigs = self.sign_hashes(hashes)
        if len(sigs) == 0:
            raise AppError("No signatures created!")
        result = sigs_to_message(sigs).encode()
        # for GUI we can also return an object with helpful data
        note = "Message with %d signatures" % len(sigs)
        obj = {
            "title": "Your signatures:",
            "note": note,
        }
        return BytesIO(result), obj
