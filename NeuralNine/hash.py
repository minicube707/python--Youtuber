import hashlib

print(hashlib.algorithms_available)
print(hashlib.algorithms_guaranteed)

print("")
print("Hash")
h = hashlib.new("SHA256")
h.update(b"hello world!")
print(h.digest())
print(h.hexdigest())


#Exemple
print("")
print("Exemple")

my_pass = b"Mypassword123"
h = hashlib.new("SHA256")
h.update(my_pass)
correct_pass = h.hexdigest()
print(correct_pass)

input = b"mypassword123"
h = hashlib.new("SHA256")
h.update(input)
input_pass = h.hexdigest()
print(input_pass)

print("Le mot de passe esr correcte ", correct_pass == input_pass)