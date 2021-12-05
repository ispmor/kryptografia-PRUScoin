from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


class User:
    def __init__(self, name, public_key, private_key):
        self.name = name
        self.hash = None  # wartość przypisujemy dopiero potem
        self.wallet = dict()
        self.cm = None  # przypisujemy dopiero w konstruktorze cm
        self.public_key = RSA.importKey(public_key.encode())
        self._private_key = RSA.importKey(private_key.encode())

    def checkout(self):
        sum = 0
        for coin_id, value in self.wallet.items():
            sum += value
        return sum

    def validate_blockchain(self):
        return self.hash == self.cm._get_header_hash()

    def sign(self, data):
        signer = pkcs1_15.new(self._private_key)
        hashed = SHA256.new(data.encode())
        return signer.sign(hashed)

    def __str__(self):
        return self.name