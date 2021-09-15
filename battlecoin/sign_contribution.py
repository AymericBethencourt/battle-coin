from blspy import PrivateKey, AugSchemeMPL

from chia.util.hash import std_hash

from clvm.casts import int_to_bytes

SK = PrivateKey.from_bytes(bytes.fromhex("3d4237d9383a7b6e60d1bfe551139ec2d6e5468205bf179ed381e66bed7b9788"))
COIN_ID = bytes.fromhex("a590af19c2e7cf0ae93de4bc2d29c39140a4cb2f7adc5d5ec7d26f19b7e717fd")
NEW_AMOUNT = int_to_bytes(1000)

signature = AugSchemeMPL.sign(SK, std_hash(COIN_ID + NEW_AMOUNT))

print(str(signature))