import csv
import copy
from math import sqrt
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity



# single pass Cosine Similarity

def pcc(user1, user2):
    sum_X = 0
    sum_Y = 0
    sum_XY = 0
    sum_X2 = 0
    sum_Y2 = 0
    n = len(user1)
    for eachKey in user1:
        sum_X += user1[eachKey]
        sum_Y += user2[eachKey]
        sum_XY += user1[eachKey] * user2[eachKey]
        sum_X2 += user1[eachKey]**2
        sum_Y2 += user2[eachKey]**2

    numerator = sum_XY - (sum_X*sum_Y)/n
    denom = sqrt(sum_X2 - (sum_X**2)/n) * sqrt(sum_Y2 - (sum_Y**2)/n)
    if denom == 0:
        return 0

    else:
        return numerator/denom


# Comparisons from loots to find P4's


with open("pandas_loot_P4.txt") as file:

    loots = csv.reader(file, delimiter=";")

    chest_Loots = {"St. Abraham's Wand": 0, "Amulet of Dispersion": 0, "Wand of the Bulwark": 0,
                   "Cloak of the Planewalker": 0, "Void Blade": 0, "Conducting Wand": 0, "Scepter of Fulmination": 0,
                   "Harlequin Armor": 0, "Plague Poison": 0, "Resurrected Warrior's Armor": 0,
                   "Tome of Purification": 0,
                   "Beehemoth Armor": 0, "Spirit Dagger": 0, "Doku No Ken": 0, "Staff of Esben": 0, "Thousand Shot": 0,
                   "Ancient Stone Sword": 0, "Prism of Dire Instability": 0, "Skullish Remains of Esben": 0,
                   "Skull of Endless Torment": 0, 'Red Beehemoth Armor': 0, 'Sullen Blade': 0}

    playerDates = {}
    playerDrops = {}
    # Get Unique player information for each user
    # 0 = name, 1=item 2=type 3=date
    for eachLoot in loots:

        # Collect Unique dates of Drops
        if eachLoot[0] not in playerDates:
            playerDates.update({eachLoot[0]: [eachLoot[3]]})
        elif eachLoot[3] not in playerDates[eachLoot[0]] and eachLoot[0] in playerDates:
            playerDates[eachLoot[0]].append((eachLoot[3]))

        # Collect unique drops this can be done within the above if else, but avoiding complexity for guild.
        if eachLoot[0] not in playerDrops and eachLoot[1] in chest_Loots:
            playerDrops.update({eachLoot[0]: chest_Loots.copy()})
            playerDrops[eachLoot[0]][eachLoot[1]] += 1

        elif eachLoot[0] in playerDrops and eachLoot[1] in chest_Loots:
            playerDrops[eachLoot[0]][eachLoot[1]] += 1



    file.close()
    # Final lootData = playerDrops
    # print(playerDrops)


# List of known p4 players OR staff
blacklist = ['blanks', 'lootaveli', 'kyooooh', 'letgay',
             'freakbaby', 'byrooni', 'freeprem', 'darazakel', 'swan', 'chao', 'thotiana', 'kouhai', 'sendhelp',
             'weebster', 'son', 'calena', 'fleaf', 'loganalt', 'lilgary', 'myra', 'kotvkedax',
             'zee', 'keep']

badBoys = {}
tbdBoys = {}


# Sort bad boys and players to be determined.
for player in playerDrops:
    if player in blacklist:
        badBoys.update({player: playerDrops[player]})
    else:
        tbdBoys.update({player: playerDrops[player]})

finalTests = {}

for eachBoy in badBoys:
    for eachUser in tbdBoys:
        check = pcc(tbdBoys[eachUser], badBoys[eachBoy])

        if check >= .7:

            if eachUser not in finalTests:
                finalTests.update({eachUser: [[eachBoy, check]]})
            elif eachUser in finalTests:
                finalTests[eachUser].append([eachBoy, check])

print("Number of people similar to atleast 1 p4", len(finalTests))
for possibly_baddie in finalTests:
    if len(finalTests[possibly_baddie]) >= 6:
        print(possibly_baddie,"Similar to", len(finalTests[possibly_baddie]), " P4 players")
        print("P4 similarity -1=opposite 0=neutral 1=Similar", finalTests[possibly_baddie])
        print(possibly_baddie, "Data")
        print(tbdBoys[possibly_baddie])
        input("Hit enter to go to next user")


