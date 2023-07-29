from embit.psbt import PSBT
from embit.descriptor.arguments import Key
from blindsign.converter import psbt_to_message
from blindsign.serializer import parse

XPUB = Key.from_string(
    "[c1684a69/86h/1h/0h]tpubDDYXEiMd73p3d3JhGa3QFKwDhHrcj6C1UYWEHJ9WVZbKZodqkoki"
    "1SQ4ynn9T7ceV9cZQZFqpJtQK3GUwQrBFC8HCNqC3DRDWbjADaceow1"
)


def test_psbt_two_inputs():
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
    msg = psbt_to_message(psbt, XPUB)
    parsed = parse(msg)
    assert len(parsed) == 2
    assert [x["input_index"] for x in parsed] == [0, 1]


def test_psbt_one_input():
    psbt = PSBT.from_string(
        "cHNidP8BAHECAAAAAc8n0LXgwM1IwKiH98QteYe9r08meoH7X7HDIw++AWlsAAAAAAD9////AqCGAQAAAAAAFgAUtwYkM0N5IkV32qjRNFwa2cuH2Z1NtyIYAQAAABYAFNVP+ApLD0gZzWPVBo7888rczslmAAAAAAABAHECAAAAAWoAD5tCQn333594o/JoD9qBDr4WuLeQK3VHBBRDk5buAQAAAAD9////Ano+JBgBAAAAFgAUmv2KqrZK35WmMX978cyJ5XEsL/YA4fUFAAAAABYAFHrN/HbdP2pQ5VJ7vnRUuO6FgaVnWAAAAAEBH3o+JBgBAAAAFgAUmv2KqrZK35WmMX978cyJ5XEsL/YiBgKp6KmpB3wZzAA3i9nNKYbLVVYA4jP9RILAUueRkqkfnBjBaEppVAAAgAEAAIAAAACAAQAAAAIAAAAAIgICrPQ/ogffg9HmvJmDbqE7WdkeS2Yn7lbBLgqgQj+Sj/wYwWhKaVQAAIABAACAAAAAgAAAAAALAAAAACICAurZ8vf2SrRM1n8CZaGF/6Z3A3OGrPYFfRP+pIew6VLkGMFoSmlUAACAAQAAgAAAAIABAAAAAwAAAAA="
    )
    msg = psbt_to_message(psbt, XPUB)
    parsed = parse(msg)
    assert len(parsed) == 1
    assert [x["input_index"] for x in parsed] == [0]


def test_psbt_wrong_xpub():
    psbt = PSBT.from_string(
        "cHNidP8BAHECAAAAAc8n0LXgwM1IwKiH98QteYe9r08meoH7X7HDIw++AWlsAAAAAAD9////AqCGAQAAAAAAFgAUtwYkM0N5IkV32qjRNFwa2cuH2Z1NtyIYAQAAABYAFNVP+ApLD0gZzWPVBo7888rczslmAAAAAAABAHECAAAAAWoAD5tCQn333594o/JoD9qBDr4WuLeQK3VHBBRDk5buAQAAAAD9////Ano+JBgBAAAAFgAUmv2KqrZK35WmMX978cyJ5XEsL/YA4fUFAAAAABYAFHrN/HbdP2pQ5VJ7vnRUuO6FgaVnWAAAAAEBH3o+JBgBAAAAFgAUmv2KqrZK35WmMX978cyJ5XEsL/YiBgKp6KmpB3wZzAA3i9nNKYbLVVYA4jP9RILAUueRkqkfnBjBaEppVAAAgAEAAIAAAACAAQAAAAIAAAAAIgICrPQ/ogffg9HmvJmDbqE7WdkeS2Yn7lbBLgqgQj+Sj/wYwWhKaVQAAIABAACAAAAAgAAAAAALAAAAACICAurZ8vf2SrRM1n8CZaGF/6Z3A3OGrPYFfRP+pIew6VLkGMFoSmlUAACAAQAAgAAAAIABAAAAAwAAAAA="
    )
    wrong_xpub = Key.from_string(
        "[c1694a69/86h/1h/0h]tpubDDYXEiMd73p3d3JhGa3QFKwDhHrcj6C1UYWEHJ9WVZbKZodqkoki"
        "1SQ4ynn9T7ceV9cZQZFqpJtQK3GUwQrBFC8HCNqC3DRDWbjADaceow1"
    )
    msg = psbt_to_message(psbt, wrong_xpub)
    assert len(parse(msg)) == 0
