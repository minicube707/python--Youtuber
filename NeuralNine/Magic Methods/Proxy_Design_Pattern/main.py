
# The Proxy Design Pattern is a structural design pattern that provides a placeholder or intermediary for another object.
# Instead of accessing the real object directly, a proxy controls access to it,
# which allows adding extra behavior such as lazy initialization, access control, logging, or caching.

# The proxy implements the same interface as the real object, so it can be used as a substitute without the client knowing the difference.
# This makes it especially useful when the real object is expensive to create or when additional control over its usage is needed.

# In Python, the proxy pattern is often implemented by creating a class that wraps the real object and
# delegates method calls to it while adding extra logic before or after the call.

from abc import ABCMeta, abstractstaticmethod

class IPerson(metaclass=ABCMeta):

    @abstractstaticmethod
    def person_method():
        """Interface Method"""

class Person(IPerson):

    def person_method(self):
        print("I am a person")

class ProxyPerson(IPerson):

    def __init__(self):
        self.person = Person()

    def person_method(self):
        print("I am the proxy functionality!")
        self.person.person_method()

p1 = Person()
p1.person_method()

p2 = ProxyPerson()
p2.person_method()