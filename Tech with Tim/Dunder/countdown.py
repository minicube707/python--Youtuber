class Coutdown:
    """A simple iterator that counts down from a give number."""
    def __init__(self, start):
        self.current = start
    
    def __iter__(self):
        """Return the iterator object itself."""
        return self 
    
    def __next__(self):
        """Return the next value in the countdown."""
        if self.current > 0:
            value = self.current
            self.current -= 1
            return value
        else:
            raise StopIteration
        
for number in Coutdown(5):
    print(number)

#__iter__(Countdown(5)) -> Countdown(5)
#__next__(Countdown(5)) -> 5
#__next__(Countdown(5)) -> 4
#__next__(Countdown(5)) -> 3
#__next__(Countdown(5)) -> raise StopIteration

