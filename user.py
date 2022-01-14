import random

import rsa
import hashlib
from chain_manager import list_to_str

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

    def proof_of_work(self, difficulty_bits, max_nonce):
        new_blockchain_possibility = self.cm.blocks.copy() + self.pending_transactions
        pt = list_to_str(new_blockchain_possibility)
        target = 2 ** (256 - difficulty_bits)
        for i in range(max_nonce):
            nonce = random.randint(0, max_nonce-1)
            hash_result = hashlib.sha256(str(pt).encode() + str(nonce).encode()).hexdigest()

            # check if this is a valid result, below the target
            if int(hash_result, 16) < target:
                return (self, hash_result, nonce)

        print("Failed after %d (max_nonce) tries" % nonce)
        return nonce


    def verify_pow(self, pow, nonce):
        new_blockchain_possibility = self.cm.blocks.copy() + self.pending_transactions
        pt = list_to_str(new_blockchain_possibility)
        hash_result = hashlib.sha256(str(pt).encode() + str(nonce).encode()).hexdigest()
        return pow == hash_result


    def clear_pending_transactions(self):
        self.pending_transactions = []


    def reward(self, coin_id, coin_value):
        self.wallet[coin_id] = coin_value
