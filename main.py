import argparse

from chain_manager import ChainManager


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--new-block", help="Creates a new block with data provided here and adds it to collection")
    parser.add_argument("--dump", help="Dump collection to .json file at the end", action="store_true")
    parser.add_argument("--print-genesis", help="At the end prints GENESIS block out", action="store_true")
    parser.add_argument("-i", "--input", help="Input file from where one should load collection")
    args = parser.parse_args()

    chainManager = ChainManager()
    chainManager.init_collection(args.input)

    while True:
        user_from = int(input("SENDER UserID: ") or "-1")
        if user_from < 0:
            print("Ending")
            break
        coin_id = int(input("Coin ID which is being transferred: ") or "-1")
        if coin_id < 0:
            print("Ending")
            break
        user_to = int(input("RECEIVER UserID: ") or "-1")
        if user_to < 0:
            print("Ending")
            break

        chainManager.create_new_block(f"{user_from} pays {coin_id} to {user_to}")
        print(f"{user_from} pays {coin_id} to {user_to}")

    if args.new_block:
        chainManager.create_new_block(args.new_block)

    if args.print_genesis:
        print(chainManager.find_genesis())

    if chainManager.verify_container_cohesion() == 0 and args.dump:
        chainManager.save_collection_to_json("pruscoin_collection.json")
