import rsa
import hashlib


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

        self.pending_transactions = []


    def checkout(self):
        sum = 0
        for coin_id, value in self.wallet.items():
            sum += value
        return sum

    def validate_blockchain(self):
        print("HASH USERA:", self.hash)
        print("HASH CMA:", self.cm._get_header_hash())
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

    def get_pending_transactions_string(self):
        result = ''
        for transaction_block in self.pending_transactions:
            result += str(transaction_block) + ' '

        return result

    def proof_of_work(self, difficulty_bits, max_nonce):
        pt = self.get_pending_transactions_string()
        target = 2 ** (256 - difficulty_bits)
        for nonce in range(max_nonce):
            hash_result = hashlib.sha256(str(self.hash).encode() + str(pt).encode() + str(nonce).encode()).hexdigest()

            # check if this is a valid result, below the target
            if int(hash_result, 16) < target:
                print("Success with nonce %d" % nonce)
                print("Hash is %s" % hash_result)
                return (self, hash_result, nonce)

        print("Failed after %d (max_nonce) tries" % nonce)
        return nonce


    def verify_pow(self, pow, nonce):
        hash_result = hashlib.sha256(str(self.hash).encode() + self.get_pending_transactions_string().encode() + str(nonce).encode()).hexdigest()
        return pow == hash_result


    def clear_pending_transactions(self):
        self.pending_transactions = []
