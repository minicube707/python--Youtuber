import hashlib

class NeuralCoinBlock:

    def __init__(self, previous_block_hash, transaction_list) -> None:
        self.previous_block_hash = previous_block_hash
        self.transaction_list = transaction_list

        self.block_data = "-".join(transaction_list) + "-" + previous_block_hash
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()

t1 = "Anna sends 2 NC to Mike"
t2 = "Tibo sends 0.5 NC to Step"
t3 = "Zoe sends 10 NC to Charles"
t4 = "Sophie sends 1.2 NC to Frank"
t5 = "Bob sends 3 NC to Val"
t6 = "Cam sends 2.9 NC to Noé"


print("")
initial_block = NeuralCoinBlock("Initial String", [t1, t2])
print(initial_block.block_data)
print(initial_block.block_hash)

print("")
second_block = NeuralCoinBlock(initial_block.block_hash, [t3, t4])
print(second_block.block_data)
print(second_block.block_hash)

print("")
third_block = NeuralCoinBlock(second_block.block_hash, [t5, t6])
print(third_block.block_data)
print(third_block.block_hash)