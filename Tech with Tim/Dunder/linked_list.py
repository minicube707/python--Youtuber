class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:

    def __init__(self):
        self.head = None
        self.size = 0
    
    def __len__(self):
        """Define behavior of the len()"""
        return self.size
    
    def __getitem__(self, index):
        """Enable indexing (obj[index])"""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        current = self.head
        for _ in range(index):
            current = current.next
        return current.value
    
    def __setitem__(self, index, value):
        """Enable item assignment (obj[index] = value)"""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        current = self.head
        for _ in range(index):
            current = current.next
        current.value = value
    
    def __delitem__(self, index):
        """Delete an item (del obj[index])"""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        if index == 0:
            self.head = self.head.next
        else:
            current = self.head
            for _ in range(index - 1):
                current = current.next
            current.next = current.next.next
        self.size -= 1

    def __contains__(self, value):
        """Define behavior for 'in' keyword."""
        current = self.head
        while current:
            if current.value == value:
                return True
            current = current.next
        return False
    
    def append(self, value):
        """Add a new node to the end of the list"""
        new_node = Node(value)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1

    def __str__(self):
        """User-friendly string representation"""
        values = []
        current = self.head
        while current:
            values.append(str(current.value))
            current = current.next
        return " -> ".join(values)
    
#Exemple  usage
ll = LinkedList()
ll.append(10)
ll.append(20)
ll.append(30)

print(len(ll)) #Output: 3
print(ll[1]) # Output: 20
ll[1] = 25
print(ll) # Output: 10 -> 25 -> 30
del ll[1] # Output: 10 -> 30
print(ll)
print(30 in ll) #Output: True