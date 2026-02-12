class Counter:
    def __init__(self):
        self.value = 1
    
    def count_up(self):
        self.value += 1
    
    def count_down(self):
        self.value -= 1

    def __str__(self):
        return f"Count={self.value}"

    def __add__(self, other):
        #Check the instance before adding
        if isinstance(other, Counter):
            return self.value + other.value
        
        raise Exception("Invalide type")
    
count1 = Counter()
count2 = Counter()

count1.count_up()
count2.count_up()

#Without Dunder
#<__main__.Counter object at 0x000001BFF6DEBE50> <__main__.Counter object at 0x000001BFF6DEBDF0>
print(count1, count2)

#Without Dunder
#TypeError: unsupported operand type(s) for +: 'Counter' and 'Counter'
print(count1 + count2)