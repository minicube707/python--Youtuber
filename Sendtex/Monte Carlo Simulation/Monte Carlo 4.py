import random
import matplotlib.pyplot as plt


sampleSize = 1_000
startingFunds = 10_000
wargerSize = 100
wagerCount = 10_000


def rollDice():
    roll = random.randint(1, 100)

    if roll == 100:
        return False

    elif roll <= 50:
        return False
    
    elif roll > 50:
        return True


def simple_bettor(funds, initial_wager, wager_count, color):
    value = funds
    wagers = initial_wager

    wX = []
    vY = []
    global simple_bust
    global simple_profits
    currentWager = 1

    while currentWager <= wager_count:
        if rollDice():
            value += wagers
            wX.append(currentWager)
            vY.append(value)
        else:
            value -= wagers
            wX.append(currentWager)
            vY.append(value)

            ###add me
            if value < 0:
                simple_bust +=1
                break

        currentWager += 1
    plt.plot(wX, vY, color)
    if value > funds:
        simple_profits += 1


def doubler_bettor(funds, initial_wager, wager_count, color):
    value = funds
    wagers = initial_wager

    wX = []
    vY = []
    currentWager = 1
    global doubler_bust
    global doubler_profits

    previousWager = "win"
    previousWagerAmout = initial_wager

    while currentWager <= wager_count:
        if previousWager == "win":

            if rollDice():
                value += wagers
                wX.append(currentWager)
                vY.append(value)

            else:
                value -= wagers
                previousWager = "lost"    
                previousWagerAmout = wagers
                wX.append(currentWager)
                vY.append(value)

                if value <= 0:
                    doubler_bust += 1
                    break
                
        elif previousWager == "lost":

            if rollDice():
                wagers = previousWagerAmout * 2
                if (value - wagers) < 0:
                    wagers = value

                value += wagers
                wagers = initial_wager
                previousWager = "win"
                wX.append(currentWager)
                vY.append(value)
                    
            else:
                wagers = previousWagerAmout * 2
                if (value - wagers) < 0:
                    wagers = value

                value -= wagers
                previousWagerAmout = wagers
                wX.append(currentWager)
                vY.append(value)

                if value <= 0:
                    doubler_bust += 1
                    break

                previousWager = "lost"

        currentWager +=1
    plt.plot(wX, vY, color)
    if value > funds:
        doubler_profits += 1


def multiple_bettors(funds, initial_wager, wager_count, random_multiple, color):
    value = funds
    wagers = initial_wager

    wX = []
    vY = []
    currentWager = 1
    global multiple_bust
    global multiple_profits

    previousWager = "win"
    previousWagerAmout = initial_wager

    while currentWager <= wager_count:
        if previousWager == "win":

            if rollDice():
                value += wagers
                wX.append(currentWager)
                vY.append(value)

            else:
                value -= wagers
                previousWager = "lost"    
                previousWagerAmout = wagers
                wX.append(currentWager)
                vY.append(value)

                if value <= 0:
                    multiple_bust += 1
                    break
                
        elif previousWager == "lost":

            if rollDice():
                wagers = previousWagerAmout * random_multiple
                if (value - wagers) < 0:
                    wagers = value

                value += wagers
                wagers = initial_wager
                previousWager = "win"
                wX.append(currentWager)
                vY.append(value)
                    
            else:
                wagers = previousWagerAmout * random_multiple
                if (value - wagers) < 0:
                    wagers = value

                value -= wagers
                previousWagerAmout = wagers
                wX.append(currentWager)
                vY.append(value)

                if value <= 0:
                    multiple_bust += 1
                    break

                previousWager = "lost"

        currentWager +=1
    plt.plot(wX, vY, color)
    if value > funds:
        multiple_profits += 1


                    

multiple_bust = 0.0
multiple_profits = 0.0

doubler_bust = 0.0
doubler_profits = 0.0

simple_bust = 0.0
simple_profits = 0.0

#Best mutliplicator ~1.7, 1.9
multiplicator = 1.8
x = 0
while x < sampleSize:      
    random_multiple = random.uniform(0.5, 10.0)
    simple_bettor(startingFunds,wargerSize,wagerCount,'k')
    doubler_bettor(startingFunds,wargerSize,wagerCount, "c")
    #multiple_bettors(startingFunds,wargerSize,wagerCount, random_multiple, "lime")
    multiple_bettors(startingFunds,wargerSize,wagerCount, multiplicator, "magenta")
    x+=1

plt.plot(1, startingFunds, color="k", label = "Single")
plt.plot(1, startingFunds, color="c", label = "Double")
#plt.plot(1, startingFunds, color="lime", label = "Mutli rand")
plt.plot(1, startingFunds, color="magenta", label = f"Mutli {multiplicator}")

print("Simple bettor bust chance", (simple_bust/sampleSize)*100.00)
print("Double bettor bust chance", (doubler_bust/sampleSize)*100.00)
print("Multi bettor bust chance", (multiple_bust/sampleSize)*100.00)
print("Simple bettor profit chance", (simple_profits/sampleSize)*100.00)
print("Double bettor profit chance", (doubler_profits/sampleSize)*100.00)
print("Multi bettor profit chance", (multiple_profits/sampleSize)*100.00)

plt.axhline(startingFunds, color = 'g')
plt.axhline(0, color = 'r')
plt.ylabel('Account Value')
plt.xlabel('Wager Count')
plt.legend(loc='upper left')
plt.show()
    