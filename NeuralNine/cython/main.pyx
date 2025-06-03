def prime_finder_vanillia (amount):
    primes = []
    number = 2
    found = 0
    while found < amount:
        for x in primes:
            if number % x == 0:
                break
        
        else:
            primes.append(number)
            found +=1
        
        number +=1

    return primes

def prime_finder_optimized(int amount):

    cdef int number, x, found
    cdef int primes[100_000]

    amount = min(amount, 100_000)

    found = 0
    number = 2

    while found < amount:
        for x in primes[:found]:
            if number % x == 0:
                break
        
        else:
            primes[found] = number
            found +=1

        number +=1

    return_list = [p for p in primes[:found]]
    return return_list