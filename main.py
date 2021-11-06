import argparse
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

    def get_last_block(self):
        if len(self.blocks_collection.keys()) == 0:
            return None
        return list(filter(lambda key: (self.blocks_collection[key].next_hash is None),
                           self.blocks_collection.keys()))[0]

    def add_block_to_container(self, block: Block):
        hashed_block = hashlib.sha256(str(block).encode('utf-8')).hexdigest()
        if hashed_block in self.blocks_collection:
            raise RuntimeError(
                "You foolish cheater! We know you've manipulated the blocks as such block already exists!")
        else:
            crucial_info = block.data.split(" ")
            if crucial_info[0] not in "GENESIS":
                # "<user1> pays <coinId> to <user2>"
                user_from, coin_id, user_to = int(crucial_info[0]), int(crucial_info[2]), int(crucial_info[4])
                if not self.validation_check(user_from, coin_id, user_to):
                    raise RuntimeError("Validation check failed")
                self.coin_to_user[coin_id] = user_to

            if block.prev_hash in self.blocks_collection:
                self.blocks_collection[block.prev_hash].next_hash = hashed_block
            self.blocks_collection[hashed_block] = block

    def validation_check(self, user_from, coin_id, user_to):
        if user_from not in self.users_dict or coin_id not in self.coins_dict or user_to not in self.users_dict:
            return False
        # Todo, sprawdzić userowy walet więc tutaj potrzebny user - Monika dasz radę to dopisac?
        return True

    def create_new_block(self, data):
        last_existing_hash = self.get_last_block()
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
            print("No GENESIS block was found.")
            return 1

        next_hash = first_block.next_hash
        counter = 1  # Genesis = 1
        while next_hash is not None:
            if next_hash not in self.blocks_collection:
                print(
                    "Damn you fool of a Took! Blocks have been manipulated! There is no such next block as indicated!")
                return 2
            tmp = self.blocks_collection[next_hash]
            next_hash = tmp.next_hash
            counter += 1

        if counter != container_size:
            return 3

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
                if block.next_hash is not None:
                    if block.next_hash in self.blocks_collection:  # typowy środkowy blok
                        if block.data is not None:
                            return 0
                        print("Blocks with empty data are not allowed.")
                        return 1
                    print("Next block indicated does not exist.")
                    return 1
                if block.data is not None:
                    return 0  # blok końcowy
                print("Blocks with empty data are not allowed.")
                return 1
            print("Previous hash has not been found in the collection - manipulation detected.")
            return 1
        if block.data is not None:
            return 0  # blok Genesis

    def init_collection(self, filename):
        if filename is None:
            self.blocks_collection = dict()
            self.coins_dict = {0: 1, 1: 1}
            self.users_dict = {0: {"name": "Bob"}, 1: {"name": "Rob"}}
            self.coin_to_user = {0:0, 1:1}  # kownencja {coin_id: user_id} WSTAWIĆ USERA zamiast user_id, albo zrobić powiązanie TODO Monika, jak będziesz miała Userka, mogłabyś?
            data = "GENESIS :\n"
            for coin_id, user_id in self.coin_to_user.items():
                data += f"Create {coin_id} to {self.users_dict[user_id]['name']}. \n"
            print(
                "Thou shall be informed about exemplar data generation which has already been performed - we have now 2 User's ids: 0, 1 and 2 coin's ids: 0, 1 of values 1 and 1")
            self.add_block_to_container(Block(None, data))
        else:
            if os.path.isfile(filename):
                with open(filename, 'r') as f:
                    whole_chain_manager = json.load(f)
                    temp_dict = whole_chain_manager["blocks_collection"]
                    for temp_dict_key, temp_dict_object in temp_dict.items():
                        block = Block(None, None).from_dict(temp_dict_object)
                        self.blocks_collection[temp_dict_key] = block
                    self.coin_to_user = whole_chain_manager["coin_to_user"]
                    self.users_dict = whole_chain_manager["users_dict"]
                    self.coins_dict = whole_chain_manager["coins_dict"]
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--new-block", help="Creates a new block with data provided here and adds it to collection")
    parser.add_argument("--dump", help="Dump collection to .json file at the end", action="store_true")
    parser.add_argument("--print-genesis", help="At the end prints GENESIS block out", action="store_true")
    parser.add_argument("-i", "--input", help="Input file from where one should load collection")
    args = parser.parse_args()

    chainManager = ChainManager()
    chainManager.init_collection(args.input)

    for i in range(5):
        chainManager.create_new_block(f"{0} pays {0} to {1}")  # USER pays COIN to USER
        chainManager.create_new_block(f"{1} pays {0} to {0}")

    chainManager.create_new_block(f"{1} pays {1} to {0}")
    chainManager.save_collection_to_json("test.json")

    if args.new_block:
        chainManager.create_new_block(args.new_block)

    if args.print_genesis:
        print(chainManager.find_genesis())

    if chainManager.verify_container_cohesion() == 0 and args.dump:
        chainManager.save_collection_to_json("pruscoin_collection.json")
