import random
import matplotlib.pyplot as plt

def rollDice():
    roll = random.randint(1, 100)

    if roll <= 50:
        return False
    
    else:
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


def multiple_bettors(funds, initial_wager, wager_count, random_multiple):
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
    #plt.plot(wX, vY)
    if value > funds:
        multiple_profits += 1

def Alembert(funds, initial_wager, wager_count):
    value = funds
    wagers = initial_wager

    wX = []
    vY = []
    currentWager = 1

    global Ret
    global da_bust
    global da_profits

    previousWager = "win"
    previousWagerAmout = initial_wager

    while currentWager <= wager_count:
        if previousWager == "win":
            if wagers == initial_wager:
                pass
            else:
                wagers -= initial_wager
            
            if rollDice():
                value += wagers
                previousWagerAmout = wagers
            else:
                value -= wagers
                previousWagerAmout = wagers
                previousWager = "lost"
                if value <= 0:
                    da_bust += 1
                    break
        
        elif previousWager == "lost":
            wagers = previousWagerAmout + initial_wager
            if(value - wagers) <= 0:
                wagers = value
            
            if rollDice():
                value += wagers
                previousWagerAmout = wagers
                previousWager = "win"
            
            else:
                value -= wagers
                previousWagerAmout = wagers

                if value <= 0:
                    da_bust += 1
                    break
            
        currentWager +=1
    if value > funds:
        da_profits += 1
    Ret += value
                    
sampleSize = 1_000
startingFunds = 100_000

wargerSize = 100
wagerCount = 1_000


Ret = 0.0
da_bust = 0.0
da_profits = 0.0
daSampleSize = 1_000

for _ in range(daSampleSize):
    Alembert(startingFunds, wargerSize, wagerCount)

print ('Total Amount Invested:', daSampleSize * startingFunds)
print ('Total Return:',Ret)
print ('Difference:',Ret-(daSampleSize * startingFunds))
print ('Bust Rate:',(da_bust/daSampleSize)*100.00)
print ('Profit Rate:',(da_profits/daSampleSize)*100.00)
    