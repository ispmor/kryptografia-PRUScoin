import json
import rsa


class Block:
    def __init__(self, prev_hash, data, private_key, sender):
        self.prev_hash = prev_hash
        self.original_data = str(data)
        self.sender = sender # do weryfikacji podpisów
        #self.signature = rsa.encrypt(self.original_data.encode(), private_key)
        self.signature = rsa.sign(self.original_data.encode(), private_key, 'SHA-1')
        self.set_data(data)

    def __str__(self):
        return f"\nBLOCK:\n\t-> {self.prev_hash} (poprzedni hash)\n\t-> {self.data}"

    def set_data(self, data):
        self.data = "{'data': " + str(data) + ", 'signature': " + str(self.signature) + "}"

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4, separators=(',', ':'))

    def from_dict(self, loaded_dict):
        self.prev_hash = loaded_dict["prev_hash"]
        self.data = loaded_dict["data"]
        return self
