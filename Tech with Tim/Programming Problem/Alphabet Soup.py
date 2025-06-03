
mot = input("\nEntrer un mot :")

result = [char for char in mot]

list_alphabet = [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " "]

res = ""

Maj = True
Min = False

i = 0
j = 0

while 0 < len(result):
    while j <= len(list_alphabet):

        try:
            if list_alphabet[j].upper() == result[i] and Maj == True:
                res = res + list_alphabet[j].upper()
                result.pop(i)

            elif list_alphabet[j] == result[i]  and Min == True:
                res = res + list_alphabet[j]
                result.pop(i)

            else:
                i+=1
                
        except:
            if Maj == True:
                Maj = False
                Min = True
                i=0
            else:
                Maj = True
                Min =False
                j+=1
                i=0
            
            
print("")
print(res)
        
