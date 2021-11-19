import hashlib
import json
import os.path

from block import Block


class ChainManager:

    def __init__(self):
        self.blocks_collection = dict()
        self.coins_dict = dict()
        self.users_dict = dict()
        self.coin_to_user = dict()
        self.header_block = None

    def get_last_block_hash(self):
        return self.get_hash_from_block(self.header_block)

    def add_block_to_container(self, block: Block, given_hash=None):
        hashed_block = self.get_hash_from_block(block)
        if hashed_block in self.blocks_collection or (given_hash is not None and not hashed_block == given_hash):
            raise RuntimeError(
                f"You foolish cheater! We know you've manipulated the blocks! Real hash: {hashed_block}, Given hash: {given_hash} This one contains error " + str(
                    block))
        else:
            crucial_info = block.data.split(" ")
            if crucial_info[0] not in "GENESIS":
                # "<user1> pays <coinId> to <user2>"
                user_from, coin_id, user_to = int(crucial_info[0]), int(crucial_info[2]), int(crucial_info[4])
                if not self.validation_check(user_from, coin_id, user_to):
                    raise RuntimeError("Validation check failed")
                self.coin_to_user[coin_id] = user_to

            self.blocks_collection[hashed_block] = block
            self.header_block = block

    def get_hash_from_block(self, block):
        return hashlib.sha256(str(block).encode('utf-8')).hexdigest()

    def validation_check(self, user_from, coin_id, user_to):
        user_from = int(user_from)
        coin_id = int(coin_id)
        user_to = int(user_to)
        if user_from not in self.users_dict or coin_id not in self.coins_dict or user_to not in self.users_dict:
            return False
        # Todo, sprawdzić userowy walet więc tutaj potrzebny user - Monika dasz radę to dopisac?
        return True

    def create_new_block(self, data):
        last_existing_hash = self.get_last_block_hash()
        if last_existing_hash is None:
            self.add_block_to_container(Block(None, data))  # Stworzenie bloku Genesis
        else:
            self.add_block_to_container(Block(last_existing_hash, data))

    def verify_container_cohesion(self):
        if len(self.blocks_collection.keys()) == 0:
            return 0

        container_size = len(self.blocks_collection.keys())
        first_block, first_block_key = self.find_genesis()
        if first_block is None or first_block_key is None:
            raise RuntimeError("No GENESIS block was found.")

        header_hash = self.get_last_block_hash()
        counter = 0
        if header_hash not in self.blocks_collection or header_hash is None:
            raise RuntimeError("Error, Error, wrong header hash")

        while self.blocks_collection[header_hash].prev_hash is not None:
            if not header_hash == self.get_hash_from_block(self.blocks_collection[header_hash]):
                raise RuntimeError(
                    f"Block has been mainpulated: {header_hash} contains data : \n {self.blocks_collection[header_hash]}")

            if self.blocks_collection[header_hash].prev_hash not in self.blocks_collection:
                raise RuntimeError(
                    "Damn you fool of a Took! Blocks have been manipulated! There is no such next block as indicated!")
            tmp = self.blocks_collection[header_hash]
            header_hash = tmp.prev_hash
            counter += 1
        genesis = self.blocks_collection[header_hash]

        if not header_hash == self.get_hash_from_block(genesis):
            raise RuntimeError(
                f"Block has been mainpulated: {header_hash} contains data : \n {self.blocks_collection[header_hash]}")
        counter += 1
        print(counter)
        print(container_size)
        if counter != container_size:
            raise RuntimeError(
                "You foolish cheater! There is an error in you blockchain! You have added artificial blocks!")

        return 0

    def find_genesis(self):
        first_block_key = list(filter(lambda key: (
                self.blocks_collection[key].prev_hash is None),
                                      self.blocks_collection.keys()))[0]
        first_block = self.blocks_collection[first_block_key]
        return first_block, first_block_key

    def validate_block(self, block: Block):
        if block.prev_hash is not None:
            if block.prev_hash in self.blocks_collection:
                if block.data is not None:
                    if not self.get_hash_from_block(self.blocks_collection[block.prev_hash]) == block.prev_hash:
                        print("THIS IS CALCULATED PREV HASH: ",
                              self.get_hash_from_block(self.blocks_collection[block.prev_hash]))
                        print("THIS IS GIVEN PREV HASH: ", block.prev_hash)
                        raise RuntimeError("You foolish cheater! There is an error in you blockchain!")
                    return 0
                raise RuntimeError("Blocks with empty data are not allowed.")
            if block.data is not None:
                return 0  # blok końcowy
        else:  # genesis
            if block.data is not None:
                return 0
            raise RuntimeError("Genesis has no data.")

    def get_coins_dict(self):
        result = {}
        key = 1
        value = 1
        while True:
            key = int(input("Introduce coin id: (Leave empty to finish)") or "-1")
            if key < 0:
                print("Ending")
                break
            value = int(input("Introduce coin value: ") or "-1")
            if value < 0:
                print("Ending")
                break
            result[key] = value
        return result

    def get_users_dict(self):
        result = {}
        while True:
            key = int(input("Introduce user id: (Leave empty to finish)") or "-1")
            if key < 0:
                print("Ending")
                break
            value = input("Introduce user Name: ")
            if value is None:
                print("Ending")
                break
            result[key] = {"name":value}
        return result

    def get_coins_users_dict(self):
        result = {}

        while True:
            key = int(input("Introduce coin id: (Leave empty to finish)") or "-1")
            if key < 0:
                print("Ending")
                break
            value = int(input("Introduce owner(User) id: ") or "-1")
            if value <0:
                print("Ending")
                break
            result[key] = value
        return result

    def init_collection(self, filename):
        if filename is None:
            self.blocks_collection = dict()
            self.coins_dict = self.get_coins_dict()
            self.users_dict = self.get_users_dict()
            self.coin_to_user = self.get_coins_users_dict() # kownencja {coin_id: user_id} WSTAWIĆ USERA zamiast user_id, albo zrobić powiązanie TODO Monika, jak będziesz miała Userka, mogłabyś?
            data = "GENESIS :\n"
            for coin_id, user_id in self.coin_to_user.items():
                data += f"Create {coin_id} to {self.users_dict[user_id]['name']}. \n"
            print(
                "Thou shall be informed about exemplar data generation which has already been performed - we have now 2 User's ids: 0, 1 and 2 coin's ids: 0, 1 of values 1 and 1") # TODO do zmiany
            self.add_block_to_container(Block(None, data))
        else:
            if os.path.isfile(filename):
                with open(filename, 'r') as f:
                    whole_chain_manager = json.load(f)
                    self.coins_to_user = {int(k): v for k, v in whole_chain_manager["coin_to_user"].items()}
                    self.users_dict = {int(k): v for k, v in whole_chain_manager["users_dict"].items()}
                    self.coins_dict = {int(k): v for k, v in whole_chain_manager["coins_dict"].items()}
                    temp_dict = whole_chain_manager["blocks_collection"]
                    for temp_dict_key, temp_dict_object in temp_dict.items():
                        block = Block(None, None).from_dict(temp_dict_object)
                        self.add_block_to_container(block, temp_dict_key)
                    header_block = Block(None, None).from_dict(whole_chain_manager["header_block"])
                    if self.get_hash_from_block(header_block) not in self.blocks_collection:
                        raise RuntimeError("Wrong header block.")
                    else:
                        self.header_block = header_block



            else:
                print("Given input file does not exist. Initializing an empty dict.")
                self.blocks_collection = dict()

    def save_collection_to_json(self, filename):
        with open(filename, 'w') as f:
            self.to_json(f)

    def add_coin(self, value):
        new_id = self.coins_dict.keys()[-1] + 1
        if value <= 0:
            raise RuntimeError("You foolish cheater! Thou shall not provide negative value for our coin!")
        self.coins_dict[new_id] = value

    def add_coin_to_user(self, coin_id, user_id):
        if coin_id not in self.coins_dict:
            raise RuntimeError("You foolish cheater! Thou shall not provide missing coin ids!")
        # TODO walidacja usera?
        self.coin_to_user.append((user_id, coin_id))

    def to_json(self, f):
        return json.dump(self, fp=f, default=lambda o: o.__dict__,
                         sort_keys=True, indent=4, separators=(',', ':'))
