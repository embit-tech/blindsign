# blindsign

Specter-DIY app and python cli tool to sign any bitcoin transaction
using it's hashes, without tx verification

## Adding app to Specter-DIY

1. Copy the `blindsign` folder from [`diy-app`](./diy-app/) folder to the
`src/apps/` folder in [Specter-DIY repo](https://github.com/cryptoadvance/specter-diy/tree/master/src/apps)
2. Add `blindsign` app into `__all__` list in [`src/apps/__init__.py`](https://github.com/cryptoadvance/specter-diy/blob/master/src/apps/__init__.py) file in Specter-DIY
3. Build the firmware and flash it to Specter-DIY as usual

## Installation

Install command line tool by running in the repo folder:

```sh
pip install .
```

## Usage of the CLI tool

### Message generation

To generate a message for Specter-DIY using PSBT transaction and master xpub:

```sh
python3 -m blindsign message <psbt> <xpub>
```

If you want to encode it as qrcode in terminal,
install `qrencode` (`sudo apt install qrencode`) and run:

```sh
python3 -m blindsign message <psbt> <xpub> | qrencode -t UTF8
```

To save QR code as an image:

```sh
python3 -m blindsign message <psbt> <xpub> | qrencode -o "message.png"
```

To save to a file for SD card transfer:

```sh
python3 -m blindsign message <psbt> <xpub> > /path/to/sd/blindsign.txt
```

### Adding signatures to PSBT

To include signatures from the message into existing transaction:

```sh
python3 -m blindsign combine <psbt> <signedmessage>
```
