import argparse
import hashlib
import json
import os.path

from block import Block

blocks_collection = dict()


def get_last_block():
    if len(blocks_collection.keys()) == 0:
        return None
    print(blocks_collection.values())
    return list(filter(lambda key: (blocks_collection[key].next_hash is None),
                       blocks_collection.keys()))[0]


def create_new_block(data):
    last_existing_hash = get_last_block()
    if last_existing_hash is None:
        add_block_to_container(Block(None, data))  # Stworzenie bloku Genesis
    else:
        add_block_to_container(Block(last_existing_hash, data))


def add_block_to_container(block: Block):
    print("----" + str(block))
    print(blocks_collection)
    hashed_block = hashlib.sha256(str(block).encode('utf-8')).hexdigest()
    if hashed_block in blocks_collection:
        raise RuntimeError("You foolish cheater! We know you've manipulated the blocks as such block already exists!")
    else:
        if block.prev_hash in blocks_collection:
            blocks_collection[block.prev_hash].next_hash = hashed_block
        blocks_collection[hashed_block] = block


def verify_container_cohesion():
    if len(blocks_collection.keys()) == 0:
        return 0

    container_size = len(blocks_collection.keys())
    first_block_key = list(filter(lambda key: (
            blocks_collection[key].prev_hash is None),
                                  blocks_collection.keys()))[0]

    first_block = blocks_collection[first_block_key]
    if first_block is None or first_block_key is None:
        print("No GENESIS block was found.")
        return 1

    next_hash = first_block.next_hash
    counter = 1  # Genesis = 1
    while next_hash is not None:
        if next_hash not in blocks_collection:
            print("Damn you fool of a Took! Blocks have been manipulated! There is no such next block as indicated!")
            return 2
        tmp = blocks_collection[next_hash]
        next_hash = tmp.next_hash
        counter += 1

    if counter != container_size:
        return 3

    return 0


def validate_block(block: Block):
    if block.prev_hash is not None:
        if block.prev_hash in blocks_collection:
            if block.next_hash is not None:
                if block.next_hash in blocks_collection:  # typowy środkowy blok
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


def init_collection(filename):
    global blocks_collection
    if filename is None:
        blocks_collection = dict()
    else:
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                temp_dict = json.load(f)
                for temp_dict_key, temp_dict_object in temp_dict.items():
                    block = Block(None, None).from_dict(json.loads(temp_dict_object))
                    blocks_collection[temp_dict_key] = block
        else:
            print("Given input file does not exist. Initializing an empty dict.")
            blocks_collection = dict()


def save_collection_to_json(filename):
    with open(filename, 'w') as f:
        json.dump(blocks_collection, fp=f, default=lambda block: block.to_json(), sort_keys=True, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--new-block", help="Creates a new block with data provided here and adds it to collection")
    parser.add_argument("--dump", help="Dump collection to .json file at the end", action="store_true")
    parser.add_argument("--print-genesis", help="At the end prints GENESIS block out")
    parser.add_argument("-i", "--input", help="Input file from where one should load collection")
    args = parser.parse_args()

    init_collection(args.input)
    for i in range(10):
        create_new_block("money:" + "$" * i)

    if args.new_block:
        create_new_block(args.new_block)

    if verify_container_cohesion() == 0 and args.dump:
        save_collection_to_json("pruscoin_collection.json")
