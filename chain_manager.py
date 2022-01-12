import hashlib
import random
import rsa

from block import Block

PoW_found = False


def get_hash(blocks: list):
    return hashlib.sha256(str(blocks).encode('utf-8')).hexdigest()


def get_transaction_string(t: dict) -> str:
    coin_string = ", ".join(t["coin_id"])
    return f'{t["from"]} pays {coin_string} to {t["to"]}'


def list_to_str(list: list):
    result = ""
    for block in list:
        result += str(block) + ' '
    return result





class ChainManager:
    def __init__(self, users: dict, coins: dict):
        self.genesis = None
        self.blocks = None
        self.header_hash = None
        public, private = rsa.newkeys(1024)
        self.public_key = public
        self._private_key = private
        self.other_public_keys = {}

        # pomocnicze
        self.users = users
        self.coins = coins
        self.nonce = 0

        for name, user in users.items():
            user.hash = self.header_hash
            user.cm = self
            self.other_public_keys[name] = user.public_key
            user.other_public_keys['cm'] = self.public_key

    def setup(self, genesis: Block):
        self.genesis = genesis
        self.blocks = [genesis]
        self.header_hash = self._get_header_hash()

    def _get_hash(self, data: list):
        return hashlib.sha256(list_to_str(data).encode('utf-8') + str(self.nonce).encode()).hexdigest()

    def _get_header_hash(self):
        return self._get_hash(self.blocks)


    def _add(self, transaction: Block, nonce):
        self.blocks.append(transaction)
        self.nonce = nonce
        self.header_hash = self._get_header_hash()

    def _add_to_pending_transactions(self, data: str, sender_private_key, sender):
        for name, user in self.users.items():
            if random.randrange(100) < 90:
                new_block = Block(self.header_hash, "'" + data + "'", sender_private_key, sender)
                user.pending_transactions.append(new_block)


    def __str__(self):
        result = ''
        for block in self.blocks:
            result += str(block) + '\n'
        result += f'\nHEADER HASH:\t{self.header_hash}\n'
        return result

    def validate(self) -> bool:
        for i in range(1, len(self.blocks)):
            actual = self._get_hash(self.blocks[:i])
            expected = self.blocks[i].prev_hash
            if not actual == expected:
                return False
        if not self.header_hash == self._get_hash(self.blocks):
            return False
        return True

    def validate_signatures(self) -> bool:
        for i in range(1, len(self.blocks)):
            block_to_check = self.blocks[i]
            public_key = self.other_public_keys[block_to_check.sender.name]
            decrypted = rsa.verify(
                block_to_check.original_data.encode(),
                block_to_check.signature,
                public_key
            )
            if decrypted != 'SHA-1':
                return False
        return True

    def make_transaction(self, transaction):
        sender = self.users[transaction["from"]]
        receiver = self.users[transaction["to"]]
        coin_ids = transaction["coin_id"]

        for coin_id in coin_ids:
            if coin_id in sender.wallet:
                receiver.wallet[coin_id] = self.coins[coin_id]
                sender.wallet.pop(coin_id)
            else:
                raise RuntimeError(f'{sender.name} nie ma id={coin_id} w swoim portfelu!')

        json = get_transaction_string(transaction)
        self._add(json, sender._private_key,
                  sender)  # tutaj dodanie do pending transactions, następnie całe pending transactions jest wkorzystywane w makeTurn()
        sender.hash = self.header_hash
        receiver.hash = self.header_hash

    def broadcast_to_pending_transactions(self, transaction):
        sender = self.users[transaction["from"]]
        receiver = self.users[transaction["to"]]
        coin_ids = transaction["coin_id"]

        for coin_id in coin_ids:
            if coin_id in sender.wallet:
                receiver.wallet[coin_id] = self.coins[coin_id]
                sender.wallet.pop(coin_id)
            else:
                raise RuntimeError(f'{sender.name} nie ma id={coin_id} w swoim portfelu!')

        json = get_transaction_string(transaction)
        self._add_to_pending_transactions(json, sender._private_key,
                                          sender)  # tutaj dodanie do pending transactions, następnie całe pending transactions jest wkorzystywane w makeTurn()




    def is_verified_by_other_users(self, hashed_pt, nonce):
        verified = True
        for name, user in self.users.items():
            if not user.verify_pow(hashed_pt, nonce):
                verified = False
                break
        print("POW VERIFIED BY USERS: ", verified)
        return verified

    def reward_user(self, user):
        reward_value = 1
        new_coin_id = str(int(sorted(self.coins.keys(), key=lambda x: int(x), reverse=True)[0]) + 1)
        self.coins[new_coin_id] = reward_value
        user.wallet[new_coin_id] = self.coins[new_coin_id]

    def clear_all_pt(self):
        for name, user in self.users.items():
            user.clear_pending_transactions()

    def notify_users_about_new_block(self, new_hash):
        for name, user in self.users.items():
            user.hash = new_hash
