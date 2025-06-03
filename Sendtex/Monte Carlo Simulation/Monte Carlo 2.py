import random
import matplotlib.pyplot as plt


sampleSize = 1_000
startingFunds = 10_000
wargerSize = 100
wagerCount = 10_000

def rollDice():
    roll = random.randint(1, 100)

    if roll == 100:
        #print(roll, "roll was 100, you lose. Play again")
        return False

    elif roll <= 50:
        #print(roll, "roll was 1-50, you lose. Play again")
        return False
    
    elif roll > 50:
        #print(roll, "roll was 51-99, you win")
        return True
    
def simple_bettor(funds, initial_wager, wager_count, color):
    value = funds
    wagers = initial_wager

    wX = []
    vY = []
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
                break

        currentWager += 1

    #print("Funds:", value)
    plt.plot(wX, vY, color)

def doubler_bettor(funds, initial_wager, wager_count, color):
    value = funds
    wagers = initial_wager

    wX = []
    vY = []
    currentWager = 1

    previousWager = "win"
    previousWagerAmout = initial_wager

    while currentWager <= wager_count:
        if previousWager == "win":
            #print("we won the last wager, great")
            if rollDice():
                value += wagers
                #print(value)
                wX.append(currentWager)
                vY.append(value)
            else:
                value -= wagers
                previousWager = "lost"    
                #print(value)
                previousWagerAmout = wagers
                wX.append(currentWager)
                vY.append(value)

                if value < 0:
                    #print("we are broke after", currentWager, " bets")
                    break
                
        elif previousWager == "lost":
            #print("we lost the last one, so will be smart and double")

            if rollDice():
                wagers = previousWagerAmout * 2
                #print("we won", wagers)
                value += wagers
                #print(value)
                wagers = initial_wager
                previousWager = "win"
                wX.append(currentWager)
                vY.append(value)
                    
            else:
                wagers = previousWagerAmout * 2
                #print("we lost", wagers)
                value -= wagers
                if value < 0:
                    #print("we are broke after", currentWager, " bets")
                    break

                #print(value)
                previousWager = "lost"
                previousWagerAmout = wagers
                wX.append(currentWager)
                vY.append(value)

        currentWager +=1

    #print(value)
    plt.plot(wX, vY, color)

x = 0
while x < sampleSize:             
    simple_bettor(startingFunds,wargerSize,wagerCount,'k')
    #simple_bettor(startingFunds,wargerSize*2,wagerCount,'c')
    doubler_bettor(startingFunds,wargerSize,wagerCount, "c")
    x+=1

plt.axhline(0, color = 'r')
plt.ylabel('Account Value')
plt.xlabel('Wager Count')
plt.show()