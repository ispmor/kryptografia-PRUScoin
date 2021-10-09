class Block:
    def __init__(self, prev_hash, data, next_block):
        self.prev_hash = prev_hash
        self.data = data
        self.next_block = next_block

    def __str__(self):
        return f"BLOCK: {self.prev_hash} - {self.data} ->\n{self.next_block}" # wypisuje ten blok i kolejne
        # return f"BLOCK: {self.prev_hash} - {self.data}" # wypisuje tylko ten blok

b = Block("inny hash", "PRUS", None)
a = Block("jakiś hash", "Możesz wyjść z internatu, ale internat pozostanie w tobie na zawsze", b)
print(a)