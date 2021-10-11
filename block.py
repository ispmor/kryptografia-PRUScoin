import json


class Block:
    def __init__(self, prev_hash, data):
        self.prev_hash = prev_hash
        self.data = data
        self.next_hash = None

    def __str__(self):
        return f"BLOCK: {self.prev_hash} - {self.data} ->\n{self.next_hash}"  # unikajmy rekurencji
        # return f"BLOCK: {self.prev_hash} - {self.data}" # wypisuje tylko ten blok

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4, separators=(',', ':'))

    def from_dict(self, loaded_dict):
        self.prev_hash = loaded_dict["prev_hash"]
        self.data = loaded_dict["data"]
        self.next_hash = loaded_dict["next_hash"]
        return self



b = Block("inny hash", "PRUS")
a = Block("jakiś hash",
          "Możesz wyjść z internatu, ale internat pozostanie w tobie na zawsze")  # to jest błąd logiczny... Nstępnym blokiem jest blok 0 ?
print(a)
