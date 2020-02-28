import csv
import copy
from math import sqrt

#single pass cosim equation to compare user Data
def pcc(user1, user2):
    sum_X = 0
    sum_Y = 0
    sum_XY = 0
    sum_X2 = 0
    sum_Y2 = 0
    n = len(user1)
    for eachKey in user1:
        sum_X = user1[eachKey]
        sum_Y = user2[eachKey]
        sum_XY = user1[eachKey] * user2[eachKey]
        sum_X2 = user1[eachKey]**2
        sum_Y2 = user2[eachKey]**2

    numerator = sum_XY - (sum_X*sum_Y)/n
    denom = sqrt(sum_X2 - (sum_X**2)/n) * sqrt(sum_Y2 - (sum_Y**2)/n)
    if denom == 0:
        return 0

    else:
        return numerator/denom



# Comparisons from loots to find P4's
with open('Loot.txt','r') as file:
    loots = csv.reader(file, delimiter=' ')
    chest_Loots = {"St. Abraham's Wand": 0, "Amulet of Dispersion": 0, "Wand of the Bulwark": 0,
                   "Cloak of the Planewalker": 0, "Void Blade": 0,"Conducting Wand": 0, "Scepter of Fulmination": 0,
                   "Harlequin Armor": 0, "Plague Poison": 0, "Resurrected Warrior's Armor": 0, "Tome of Purification":0,
                   "Beehemoth Armor": 0, "Spirit Dagger": 0, "Doku No Ken": 0, "Staff of Esben":0, "Thousand Shot":0,
                   "Ancient Stone Sword": 0, "Prism of Dire Instability": 0, "Skullish Remains of Esben": 0,
                   "Skull of Endless Torment": 0, 'Red Beehemoth Armor': 0, 'Sullen Blade': 0}


    blacklist = ['Blanks', 'Lootaveli', 'kyooooh', 'letgay', 'Freakbaby', 'Byrooni', 'freeprem', 'Darazakel', 'Swan',
                 'Chao', 'Thotiana', 'Kouhai', 'sendhelp', 'Weebster', 'Son', 'Calena','fleaf','LoganALT','mike']
    training_set = {}
    test_set = {}


    for eachLoot in loots:
        if len(eachLoot) >= 7:
            lootType = eachLoot[0][2:-2]
            user = eachLoot[5][1:-1]
            drop = eachLoot[11:]
            dropName = ''
           #Get name of item drop
            for eachIndex in drop:
                if ']' not in eachIndex:
                    dropName += eachIndex +' '
                else:
                    dropName += eachIndex
                    break


            if dropName[1:-1] in chest_Loots and user not in blacklist and user not in test_set:
                test_set.update({user:copy.deepcopy(chest_Loots)})
                test_set[user][dropName[1:-1]] += 1
            elif dropName[1:-1] in chest_Loots and user not in blacklist and user in test_set:
                test_set[user][dropName[1:-1]] += 1
            elif dropName[1:-1] in chest_Loots and user in blacklist and user not in training_set:
                training_set.update({user:copy.deepcopy(chest_Loots)})
                training_set[user][dropName[1:-1]] += 1
            elif dropName[1:-1] in chest_Loots and user in blacklist and user in training_set:
                training_set[user][dropName[1:-1]] += 1


    final_neighbors = []
    for eachUser in test_set:
        user_compared = []
        for eachP4 in training_set:
            user_compared.append((eachUser+' compared to '+eachP4, pcc(test_set[eachUser], training_set[eachP4])))

        user_compared = sorted(user_compared, key=lambda tup: tup[1], reverse=True)

        if user_compared[0][1] >= .6:
            final_neighbors.append([user_compared[x] for x in range(3)])

    for eachSet in final_neighbors:
        print(eachSet)