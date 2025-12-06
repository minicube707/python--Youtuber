import random

list_word = ["secret", "brain", "network", "machine", "learning", "computer", "science", "python", "coding", "phone", "linux", "video", "programming", "laptop", "television", "book", "cryptography", "encryption", "hacking", "mathematic", "tutoriel", "youtube", "vector", "matrice", "octect", "process", "screen", "keyboard", "motherboard", "internet", "browser", "password", "headphone", "router", "antivirus" "firewall", "program", "bandwidth", "website", "algorithm", "array", "hologram"]


word = random.choice(list_word)

allow_errors = 7
guesses = []
done = False

while not done:
    print("")
    for letter in word:
        if letter.lower() in guesses:
            print(letter, end=" ")
        
        else:
            print("_", end=" ")
        
    print("")

    guess  = input(f"Alllowed errors Left {allow_errors}, Next Guess: ")
    guesses.append(guess.lower())
    if guess.lower() not in word.lower():
        allow_errors -= 1
        if allow_errors == 0:
            break

    done = True
    for letter in word:
        if letter.lower() not in guesses:
            done = False


if done:
    print(f"You find the word!, It was {word}!")

else:
    print(f"Game over! You should find the word {word}!")