import rsa

class User:
    def __init__(self, name):
        self.name = name
        self.hash = None  # wartość przypisujemy dopiero potem
        self.wallet = dict()
        self.cm = None  # przypisujemy dopiero w konstruktorze cm
        public, private = rsa.newkeys(1024)
        self.public_key = public
        self._private_key = private
        self.other_public_keys = {}

    def checkout(self):
        sum = 0
        for coin_id, value in self.wallet.items():
            sum += value
        return sum

    def validate_blockchain(self):
        return self.hash == self.cm._get_header_hash()

    def validate_genesis_signature(self):
        genesis = self.cm.genesis
        cm_public_key = self.other_public_keys['cm']
        decrypted = rsa.verify(
            genesis.original_data.encode(), 
            genesis.signature,
            cm_public_key
        )
        return decrypted == 'SHA-1'

    def __str__(self):
        return self.name