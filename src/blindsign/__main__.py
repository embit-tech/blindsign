import argparse
from embit.psbt import PSBT
from embit.descriptor.arguments import Key
from . import psbt_to_message, parse, fill_psbt


def create_message(args):
    psbt = PSBT.from_string(args.psbt)
    xpub = Key.from_string(args.xpub)
    msg = psbt_to_message(psbt, xpub)
    print("blindsign", msg)


def combine_psbt(args):
    psbt = PSBT.from_string(args.psbt)
    sigs = parse(args.signatures)
    combined = fill_psbt(psbt, sigs)
    print(combined)


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subparser for the "message" command
    parser_message = subparsers.add_parser(
        "message",
        help="Create a message for blindly signing the " "transaction on Specter-DIY",
    )
    parser_message.add_argument("psbt", type=str, help="PSBT transaction to sign")
    parser_message.add_argument(
        "xpub",
        type=str,
        help="Public key with or without derivation. "
        "If xpub is a root key, derivation is optional, "
        "otherwise it must have derivation in the form "
        "[fingperint/derivation]xpub",
    )
    parser_message.set_defaults(func=create_message)

    # Subparser for the "combine" command
    parser_combine = subparsers.add_parser(
        "combine", help="Combine PSBT with signatures " "received from Specter-DIY"
    )
    parser_combine.add_argument(
        "psbt", type=str, help="PSBT transaction to add signatures to"
    )
    parser_combine.add_argument(
        "signatures", type=str, help="The signatures received from Specter-DIY"
    )
    parser_combine.set_defaults(func=combine_psbt)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
