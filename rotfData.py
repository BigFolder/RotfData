import tkinter as tk
import datetime
import csv
import operator
import discord
import time
import winsound


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)
        start = time.time()
        text_channel_list = ['primals', 'deaths', 'legendaries']

        death = open('Death.txt', 'w')

        loot = open('Loot.txt', 'w')
        for guild in self.guilds:
            for channel in guild.channels:
                if str(channel) in text_channel_list:
                    messages = await channel.history(limit=None).flatten()
                    for message in messages:
                        message_sort([str(message.channel), str(message.created_at), str(message.content)], death, loot)

        death.close()
        loot.close()
        duration = 1000  # milliseconds
        freq = 440  # Hz
        winsound.Beep(freq, duration)

        end = time.time()
        print("Finished Gathering Text Files, if the program is not responding, its safe to close the files should be saved automatically.")
        print('that took', round(end-start),'seconds ')



def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def final_dates():

    loot_read = open('Loot.txt', 'r')
    last_line_l = loot_read.readlines()[0]
    loot_read.close()
    loot_date = last_line_l.split(',')[1]

    return loot_date[2:21]

def message_sort(message_info, death_file, loot_file):

    channel = message_info[0]
    date = message_info[1]
    content = message_info[2]

    if str(channel) == 'deaths':
        death_file.write(str([channel, date, content])+'\n')
    elif str(channel) == 'primals' or str(channel) == 'legendaries':
        loot_file.write(str([channel, date, content])+'\n')


def discord_text_update(user_token, root):
    start = time.time()
    lbl_Loading = tk.Label(root, text="Currently collecting and creating 2 big text files \n " +
                                      "this will likely take 5+mins let it run It'll ping you when done.",
                            font=("Helvetica", 12, "bold"))
    lbl_Loading.place(x=100, y=400)
    client = MyClient()
    client.run(user_token, bot=False)
    end = time.time()

    lbl_finish = tk.Label(root,text='All Finished! :D \n that took'+str(end-start)+'minutes',
                          font=("Helvetica", 12, "bold"), fg='#00d458')
    lbl_finish.place(x=150, y=250)

def update_gui():
    root = tk.Tk()
    root.title('Update Data - Mr.Squiddy')
    root.geometry('600x600')
    center(root)
    frame_bg = tk.Frame(root, width=600, height=600, bg='#a7f9fa')
    frame_bg.place(x=0, y=0)



    entry_usertoken = tk.Entry(root,font=("Helvetica", 12, "bold"), width=40)
    entry_usertoken.place(x=125, y=450)

    btn_updateUpdate = tk.Button(root, text="Update Text Files\n This takes 5+mins 8D", bd=5,
                                 font=("Helvetica", 12, "bold"), padx=5, pady=5,
                                 command=lambda: [discord_text_update(entry_usertoken.get(), root)])
    btn_updateUpdate.place(x=200, y=500)

    btn_back = tk.Button(root, text='Go Back', command=lambda: [root.destroy(), create_gui()], padx=5, pady=5,
                         font=("Helvetica", 12, "bold"), bd=5)
    btn_back.place(x=10, y=550)

    lbl_token = tk.Label(root, text="Enter your Discord Token, google it to find out where to get it. \n"
                                    "This lets you interact with discord using Python on your discord account.\n"
                                    "It's how we gather all messages in existence for each loot/death channel. :D")
    lbl_token.place(x=120,y=15)

    root.mainloop()


def death_data_sepcific(player_name):

    with open('Death.txt', 'r') as DeathFile:

        death_data = {'Total Recorded Deaths': 0, 'Total Fame Gained(Estimated)': 0,
                      'Player Monster Deaths': [], 'Days of Deaths': 0, 'Deaths by Date': 0
                      }
        deaths_by_date = {}
        monster_Log = {}
        day_of_death = {}
        playerDeaths = []
        blacklist = ['blanks', 'lootaveli', 'kyooooh', 'letgay', 'freakbaby', 'byrooni', 'freeprem', 'darazakel','swan',
                        'chao', 'thotiana', 'kouhai', 'sendhelp', 'weebster', 'son', 'calena','fleaf','loganalt','mike',
                        'skilly','lilGary','myra','kotvkedax', 'zee','keep']

        deaths = csv.reader(DeathFile, delimiter=' ', quoting=csv.QUOTE_NONE)
        for eachDeath in deaths:
            if len(eachDeath) > 4 and eachDeath[3] != "'@Deaths:":

                day = eachDeath[1][1:]
                time = eachDeath[2][:-9]

                death = eachDeath[5:]
                player = death[0]
                player = player.lower()
                #epic clean
                monster = death[7:]
                if monster[0] == 'Epic':
                    monster = monster[1:]

                monster = ' '.join(monster)[:-3]
                basefame = int(death[2][:-1])

                if player == player_name:
                    death_data['Total Recorded Deaths'] += 1

                    #Collect Monster
                    if monster not in monster_Log:
                        monster_Log.update({monster: 1})
                    elif monster  in monster_Log:
                        monster_Log[monster] += 1

                    # Collect Date of Death
                    if day not in deaths_by_date:
                        deaths_by_date.update({day: [time]})
                    else:
                        deaths_by_date[day].append([time])

                # Collect Player that died and their fame gained
                if player not in blacklist and player == player_name:
                    if basefame > 0 and basefame <= 450:
                        playerDeaths.append(basefame*1)
                    elif basefame > 450 and basefame <= 1000:
                        playerDeaths.append(basefame * 1.5)
                    elif basefame > 1000 and basefame <= 3500:
                        playerDeaths.append(basefame * 2)
                    elif basefame > 3500 and basefame <= 5000:
                        playerDeaths.append(basefame * 2.5)
                    elif basefame > 5000 and basefame <= 7500:
                        playerDeaths.append(basefame * 3.5)
                    elif basefame > 7500 and basefame <= 9000:
                        playerDeaths.append(basefame * 4)
                    elif basefame > 9000 and basefame <= 9999:
                        playerDeaths.append(basefame * 4.5)
                    elif basefame >= 10000 and basefame <= 10500:
                        playerDeaths.append(basefame * 7)
                    elif basefame > 10500 and basefame <= 12500:
                        playerDeaths.append(basefame * 5.5)
                    elif basefame > 12500 and basefame <= 15000:
                        playerDeaths.append(basefame * 5.75)
                    elif basefame > 15000 and basefame <= 29999:
                        playerDeaths.append(basefame * 6)
                    elif basefame > 29999 and basefame <= 31000:
                        playerDeaths.append(basefame * 6.5)
                    elif basefame > 31000 and basefame <= 99999:
                        playerDeaths.append(basefame * 10)
                    elif basefame > 99999:
                        playerDeaths.append(basefame * 13)

                #Base fame Weighted slightly annoying
                if player not in blacklist and player == player_name:
                    if basefame > 0 and basefame <=450 :
                        death_data['Total Fame Gained(Estimated)'] += basefame * 1
                    elif basefame > 450 and basefame <= 1000:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 1.5
                    elif basefame > 1000 and basefame <= 3500:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 2
                    elif basefame > 3500 and basefame <= 5000:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 2.5
                    elif basefame > 5000 and basefame<= 7500:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 3.5
                    elif basefame > 7500 and basefame <= 9000:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 4
                    elif basefame > 9000 and basefame <= 9999:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 5
                    elif basefame >= 10000 and basefame<=10500:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 7
                    elif basefame > 10500 and basefame <= 12500:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 5.5
                    elif basefame > 12500 and basefame <= 15000:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 5.75
                    elif basefame > 15000 and basefame <= 29999:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 6
                    elif basefame > 29999 and basefame <= 31000:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 6.5
                    elif basefame > 31000 and basefame <= 99999:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 9
                    elif basefame > 99999:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 13

        # Sort the Monsters/players High to low
        sorted_monsters = sorted(monster_Log.items(), key=operator.itemgetter(1), reverse=True)
        sorted_players = sorted(playerDeaths,reverse=True)

        death_data['Player Monster Deaths'] = [sorted_monsters[x] for x in range(len(sorted_monsters))]
        death_data['Highest Fame Death(Estimate)'] = sorted_players[0]
        death_data.update({'Deaths by Date':deaths_by_date})

        for eachDay in death_data['Deaths by Date']:
            # GET DAY m,w,t,r etc
            Y, M, D = [int(x) for x in eachDay.split('-')]
            myDay = datetime.date(Y, M, D).strftime('%A')
            if myDay not in day_of_death:
                day_of_death.update({myDay:1})
            else:
                day_of_death[myDay] += 1
        death_data['Days of Deaths'] = day_of_death

    return death_data


def loot_data_specific(player_name):

    with open('Loot.txt', 'r') as file:
        items = {} #Used to filter and find names for item blacklist

        players_drop_count = {} #each players total drops lege/primal/200 tokens
        total_primals = {} #Each type of primal drop and the total count of them that have been dropped
        total_legendaries = {} #Each type of lege drop and the total count of them that have dropped
        total_primals_token = {} #Each type of primal that has been opened with 200 necrop tokens
        date_drops = {}    #The date for each drop lege/primal
        day_counter = {}
        #All "TOP" 5 or 10 w.e can be grabbed from sorted dicts we create for others.
        loot_data = {'Total Primal Drops': 0, 'Total Legendary Drops': 0, 'Drops Per Day': 0,
                     'Days of activity': 0, 'Most Common Legendary Drop': 0, 'Most Common Primal Drop': 0,
                     'Name of Day Counter': 0, '200 Tokens Turned in':0, 'Date Drops':0}

        blacklist = ['mike','miniguy','miniguy','skilly','tuckingfypo','blanks','lootaveli','kyooooh','letgay',
                     'freakbaby','byrooni','freeprem','darazakel','swan','chao', 'thotiana', 'kouhai', 'sendhelp',
                     'weebster', 'son', 'calena','fleaf','loganalt','mike','skilly','lilgary','myra','kotvkedax',
                     'zee','keep']

        item_blacklist = ['pls video ;(((', 'pls video ;(((', 'autism', 'u aint gettin one', 'Depression',
                          'hah u thought', 'YOINKED UR 10K FAME - ARENA', 'gay', 'Dead Streamer', 'Gay', '0 0 0',
                          'A can of whoopass made for the hand.', 'yOU SMELL THIS TO0???', 'depression',
                          'Streetwise dumb bruh, but booksmart.', 'Fioreen said to', 'bruhmoment', 'Lol get rekt mate',
                          'Canhannon', 'LOL', 'looooooOOOOOOOOOOoooooooL', 'never getting a hc legit btw', '1',
                          'Hvis pose', 'Hentai', 'Short Dagger', 'breastplate of the big titan',
                          'Followers for Depression', 'u wish', 'Admin Sword', 'Omni Ring', 'oWocannon', ':)I',
                          'handcannon', 'LOOOOOOL', 'Omnipotence Ring', 'u like getting loot', 'Public Arena Key',
                          '64 Stacks of Cobblestone', ':)', 'this guy has 100% death ratio', 'this guy has swagger',
                          'U GOT IT AGAIN GROSS BOW', 'GROSS BOW!!!', 'Shattered Waraxe', 'Lucky Potio',
                          'he got hand & feet too', 'head', 'Lol you wish this was an Asura', 'MONEY MOVES!!!',
                          'Handcannon']

        loots = csv.reader(file, delimiter=' ', quoting=csv.QUOTE_NONE)
        for eachDrop in loots:
            if len(eachDrop) > 5:
                # Get Date
                date = eachDrop[1:3]

                # Complex datetime analysis
                day = date[0][1:]
                time = date[1][:-9]
                day_time = (day,time)

                # Get Player name
                user = eachDrop[5][1:-1]
                user = user.lower()

                # Get Drop Type (Pimal/Lege) 200 tokens check
                drop_type = eachDrop[9]
                # primal=Primal, legendary=Legendary, Necrotic = 200 necrop tokens.

                # Get item name
                item_name = eachDrop[11:]
                final_item = ''
                for eachIndex in item_name:

                    if eachIndex[len(eachIndex)-1] == ']':
                        final_item += eachIndex
                        final_item = final_item[1:-1]
                        break
                    else:
                        final_item += eachIndex + ' '

                if drop_type == 'primal' and final_item not in item_blacklist and user == player_name:
                    # Collect item
                    if final_item not in items and final_item not in item_blacklist:
                        items.update({final_item:1})
                    elif final_item in items and final_item not in item_blacklist:
                        items[final_item]+=1

                    # Total Primal addition
                    loot_data['Total Primal Drops'] += 1

                    # Count specific Primal items

                    if drop_type == 'primal' and final_item not in total_primals:
                        total_primals.update({final_item:1})
                    elif drop_type =='primal' and final_item in total_primals:
                        total_primals[final_item]+=1
                    #Player drop counter
                    if user not in players_drop_count and user not in blacklist:
                        players_drop_count.update({user: {'Primal': 1, 'Legendary': 0, 'Tokens': 0}})
                    elif user in players_drop_count and user not in blacklist:
                        players_drop_count[user]['Primal'] += 1

                    #Date stuff
                    if day_time[0] not in date_drops:
                        date_drops.update({day_time[0]: [day_time[1]]})
                    else:
                        date_drops[day_time[0]].append(day_time[1])

                elif drop_type == 'legendary' and final_item not in item_blacklist and user == player_name:
                    #Item name collection
                    if final_item not in items and final_item not in item_blacklist:
                        items.update({final_item:1})
                    elif final_item in items and final_item not in item_blacklist:
                        items[final_item]+=1
                    # Total lege addition
                    loot_data['Total Legendary Drops'] += 1
                    # Count specific Lege drops
                    if drop_type =='legendary' and final_item not in total_legendaries:
                        total_legendaries.update({final_item: 1})
                    elif drop_type=='legendary' and final_item in total_legendaries:
                        total_legendaries[final_item] += 1
                    # Player drop collection
                    if user not in players_drop_count and user not in blacklist:
                        players_drop_count.update({user:{'Primal': 0, 'Legendary': 1, 'Tokens': 0}})
                    elif user in players_drop_count and user not in blacklist:
                        players_drop_count[user]['Legendary'] += 1

                    # Date stuff
                    if day_time[0] not in date_drops:
                        date_drops.update({day_time[0]: [day_time[1]]})
                    else:
                        date_drops[day_time[0]].append(day_time[1])

                elif drop_type == 'Necrotic' and user == player_name:
                    # Total Token addition

                    if drop_type == 'Necrotic':
                        # Extra work to grab token names
                        token_item = final_item.split()
                        final_item = ''
                        for eachIndex in token_item[2:]:
                            if ']' in eachIndex:
                                final_item += eachIndex
                                final_item = final_item[1:-3]
                                break
                            else:
                                final_item += eachIndex + ' '

                    # Item Collection
                    if final_item not in items and final_item not in item_blacklist:
                        items.update({final_item:1})
                    elif final_item in items and final_item not in item_blacklist:
                        items[final_item]+=1

                    # Sepcific Tokens collection

                    if drop_type =='Necrotic' and final_item not in total_primals_token:
                        total_primals_token.update({final_item:1})
                    elif drop_type=='Necrotic' and final_item in total_primals_token:
                        total_primals_token[final_item] += 1

                    # Player collection
                    if user not in players_drop_count and user not in blacklist:
                        players_drop_count.update({user:{'Primal':0, 'Legendary':0, 'Tokens':1}})
                    elif user in players_drop_count and user not in blacklist:
                        players_drop_count[user]['Tokens'] += 1

                    if day_time[0] not in date_drops:
                        date_drops.update({day_time[0]:[day_time[1]]})
                    else:
                        date_drops[day_time[0]].append(day_time[1])

        sorted_primal_total = sorted(total_primals.items(), key=operator.itemgetter(1), reverse=True)
        sorted_legendary_total = sorted(total_legendaries.items(), key=operator.itemgetter(1), reverse=True)

        for eachDay in date_drops:
            # GET DAY m,w,t,r etc
            Y, M, D = [int(x) for x in eachDay.split('-')]
            myDay = datetime.date(Y, M, D).strftime('%A')
            if myDay not in day_counter:
                day_counter.update({myDay:1})
            else:
                day_counter[myDay] += 1

        loot_data['Most Common Legendary Drop'] = sorted_legendary_total[0]
        loot_data['Most Common Primal Drop'] = sorted_primal_total[0]
        loot_data['200 Tokens Turned in'] = players_drop_count[player_name]['Tokens']
        loot_data['Total Primal Drops'] = players_drop_count[player_name]['Primal']
        loot_data['Total Legendary Drops'] = players_drop_count[player_name]['Legendary']
        loot_data['Days of activity'] = len(date_drops)
        loot_data['Name of Day Counter'] = day_counter
        loot_data['Date Drops'] = date_drops

        summed_drops = 0
        for day in date_drops:
            summed_drops += len(date_drops[day])
        loot_data['Drops Per Day'] = summed_drops/len(date_drops)


        return loot_data

def loot_data():
    with open('Loot.txt', 'r') as file:
        items = {} #Used to filter and find names for item blacklist

        players_drop_count = {} #each players total drops lege/primal/200 tokens
        total_primals = {} #Each type of primal drop and the total count of them that have been dropped
        total_legendaries = {} #Each type of lege drop and the total count of them that have dropped
        total_primals_token = {} #Each type of primal that has been opened with 200 necrop tokens
        date_drops = {}    #The date for each drop lege/primal

        #All "TOP" 5 or 10 w.e can be grabbed from sorted dicts we create for others.
        loot_data = {'Total Primal Drops': 0, 'Total Legendary Drops': 0, '10 Most Common Primal Drops': 0,
                    'Total Primals From Tokens': 0, '5 Most Common Primals(token)': 0, 'Drops Per Day': 0,
                    'Top 10 Players Primals': 0, '10 Most Common Legendary Drops': 0, 'Top 10 Players Legendary':0,
                     'Filtered Drops':0}

        blacklist = ['mike', 'miniguy', 'miniguy', 'skilly', 'tuckingfypo', 'blanks', 'lootaveli', 'kyooooh', 'letgay',
                     'freakbaby', 'byrooni', 'freeprem', 'darazakel', 'swan', 'chao', 'thotiana', 'kouhai', 'sendhelp',
                     'weebster', 'son', 'calena', 'fleaf', 'loganalt', 'mike', 'skilly', 'lilgary', 'myra', 'kotvkedax',
                     'zee', 'keep']


        item_blacklist = ['pls video ;(((', 'pls video ;(((', 'autism', 'u aint gettin one', 'Depression',
                          'hah u thought', 'YOINKED UR 10K FAME - ARENA', 'gay', 'Dead Streamer', 'Gay', '0 0 0',
                          'A can of whoopass made for the hand.', 'yOU SMELL THIS TO0???', 'depression',
                          'Streetwise dumb bruh, but booksmart.', 'Fioreen said to', 'bruhmoment', 'Lol get rekt mate',
                          'Canhannon', 'LOL', 'looooooOOOOOOOOOOoooooooL', 'never getting a hc legit btw', '1',
                          'Hvis pose', 'Hentai', 'Short Dagger', 'breastplate of the big titan',
                          'Followers for Depression', 'u wish', 'Admin Sword', 'Omni Ring', 'oWocannon', ':)I',
                          'handcannon', 'LOOOOOOL', 'Omnipotence Ring', 'u like getting loot', 'Public Arena Key',
                          '64 Stacks of Cobblestone', ':)', 'this guy has 100% death ratio', 'this guy has swagger',
                          'U GOT IT AGAIN GROSS BOW', 'GROSS BOW!!!', 'Shattered Waraxe', 'Lucky Potio',
                          'he got hand & feet too', 'head', 'Lol you wish this was an Asura', 'MONEY MOVES!!!',
                          'Handcannon']

        loots = csv.reader(file, delimiter=' ', quoting=csv.QUOTE_NONE)
        for eachDrop in loots:
            if len(eachDrop) > 5:
                # Get Date
                date = eachDrop[1][1:]

                # Get Player name
                user = eachDrop[5][1:-1]
                user = user.lower()
                # Get Drop Type (Pimal/Lege) 200 tokens check
                drop_type = eachDrop[9]
                # primal=Primal, legendary=Legendary, Necrotic = 200 necrop tokens.

                # Get item name
                item_name = eachDrop[11:]
                final_item = ''
                for eachIndex in item_name:

                    if eachIndex[len(eachIndex)-1] == ']':
                        final_item += eachIndex
                        final_item = final_item[1:-1]
                        break
                    else:
                        final_item += eachIndex + ' '


                if drop_type == 'primal' and final_item not in item_blacklist and user not in blacklist:
                    # Collect item
                    if final_item not in items and final_item not in item_blacklist:
                        items.update({final_item:1})
                    elif final_item in items and final_item not in item_blacklist:
                        items[final_item]+=1

                    # Total Primal addition
                    loot_data['Total Primal Drops'] += 1

                    # Count specific Primal items

                    if drop_type == 'primal' and final_item not in total_primals:
                        total_primals.update({final_item:1})
                    elif drop_type =='primal' and final_item in total_primals:
                        total_primals[final_item]+=1
                    #Player drop counter
                    if user not in players_drop_count and user not in blacklist:
                        players_drop_count.update({user: {'Primal': 1, 'Legendary': 0, 'Tokens': 0}})
                    elif user in players_drop_count and user not in blacklist:
                        players_drop_count[user]['Primal'] += 1

                    #Date stuff
                    if date not in date_drops:
                        date_drops.update({date:1})
                    else:
                        date_drops[date] += 1




                elif drop_type == 'legendary' and final_item not in item_blacklist and user not in blacklist:
                    #Item name collection
                    if final_item not in items and final_item not in item_blacklist:
                        items.update({final_item:1})
                    elif final_item in items and final_item not in item_blacklist:
                        items[final_item]+=1
                    # Total lege addition
                    loot_data['Total Legendary Drops'] += 1
                    # Count specific Lege drops
                    if drop_type =='legendary' and final_item not in total_legendaries:
                        total_legendaries.update({final_item:1})
                    elif drop_type=='legendary' and final_item in total_legendaries:
                        total_legendaries[final_item]+=1
                    # Player drop collection
                    if user not in players_drop_count and user not in blacklist:
                        players_drop_count.update({user:{'Primal':0, 'Legendary':1, 'Tokens':0}})
                    elif user in players_drop_count and user not in blacklist:
                        players_drop_count[user]['Legendary']+=1

                    # Date stuff
                    if date not in date_drops:
                        date_drops.update({date: 1})
                    else:
                        date_drops[date] += 1


                elif drop_type == 'Necrotic' and user not in blacklist:
                    # Total Token addition
                    loot_data['Total Primals From Tokens'] += 1

                    if drop_type =='Necrotic':
                        # Extra work to grab token names
                        token_item = final_item.split()
                        final_item = ''
                        for eachIndex in token_item[2:]:
                            if ']' in eachIndex:
                                final_item += eachIndex
                                final_item = final_item[1:-3]
                                break
                            else:
                                final_item += eachIndex + ' '

                    # Item Collection
                    if final_item not in items and final_item not in item_blacklist:
                        items.update({final_item:1})
                    elif final_item in items and final_item not in item_blacklist:
                        items[final_item]+=1

                    # Sepcific Tokens collection
                    loot_data['Total Primals From Tokens'] += 1
                    if drop_type =='Necrotic' and final_item not in total_primals_token:
                        total_primals_token.update({final_item:1})
                    elif drop_type=='Necrotic' and final_item in total_primals_token:
                        total_primals_token[final_item] += 1

                    # Player collection
                    if user not in players_drop_count and user not in blacklist:
                        players_drop_count.update({user:{'Primal':0, 'Legendary':0, 'Tokens':1}})
                    elif user in players_drop_count and user not in blacklist:
                        players_drop_count[user]['Tokens'] += 1

                elif drop_type != 'primal' and drop_type != 'legendary' and drop_type != 'Necrotic' or final_item in item_blacklist or user in blacklist:
                    loot_data['Filtered Drops'] += 1




        sorted_primal_total = sorted(total_primals.items(), key=operator.itemgetter(1), reverse=True)
        sorted_legendary_total = sorted(total_legendaries.items(), key=operator.itemgetter(1), reverse=True)
        sorted_primal_token_total = sorted(total_primals_token.items(), key=operator.itemgetter(1), reverse=True)

        # Drops per day
        summed_dateDrops = 0
        for k in date_drops:
            summed_dateDrops += date_drops[k]


        # Get final values for many
        loot_data['Drops Per Day'] = round(summed_dateDrops/len(date_drops))
        loot_data['10 Most Common Primal Drops'] = [(sorted_primal_total[x]) for x in range(5)]
        loot_data['10 Most Common Legendary Drops'] = [(sorted_legendary_total[x]) for x in range(5)]
        loot_data['5 Most Common Primals(Tokens)'] = [(sorted_primal_token_total[x]) for x in range(5)]

        players_sorted_primal = sorted(players_drop_count, key=lambda x: (players_drop_count[x]['Primal']), reverse=True)
        players_sorted_legendary = sorted(players_drop_count, key=lambda x: (players_drop_count[x]['Legendary']), reverse=True)
        loot_data['Top 10 Players Primals'] = [(players_sorted_primal[x], players_drop_count[players_sorted_primal[x]]['Primal']) for x in range(10)]
        loot_data['Top 10 Players Legendary'] = [(players_sorted_legendary[x], players_drop_count[players_sorted_legendary[x]]['Legendary']) for x in range(10)]


        '''
        print(loot_data['Top 10 Players Primals'])
        print(loot_data['Top 10 Players Legendary'])
        print(loot_data['10 Most Common Primal Drops'])
        print(loot_data['10 Most Common Legendary Drops'])
        print(loot_data['5 Most Common Primals(Tokens)'])
        print(loot_data['Total Primal Drops'])
        print(loot_data['Total Legendary Drops'])
        print(loot_data['Total Primals From Tokens'])
        '''

        return loot_data

def death_data():
    with open('Death.txt', 'r') as DeathFile:

        death_data = {'Total Recorded Deaths': 0, 'Total 8/8 Deaths': 0, 'Total Fame Gained(Estimated)': 0,
                      'Top 10 Monsters': [], 'Top 10 Worst(best) players': []}
        deaths_by_date = {}
        deaths_by_player = {}
        monster_Log = {}
        blacklist = ['mike', 'miniguy', 'miniguy', 'skilly', 'tuckingfypo', 'blanks', 'lootaveli', 'kyooooh', 'letgay',
                     'freakbaby', 'byrooni', 'freeprem', 'darazakel', 'swan', 'chao', 'thotiana', 'kouhai', 'sendhelp',
                     'weebster', 'son', 'calena', 'fleaf', 'loganalt', 'mike', 'skilly', 'lilgary', 'myra', 'kotvkedax',
                     'zee', 'keep']

        deaths = csv.reader(DeathFile, delimiter=' ', quoting=csv.QUOTE_NONE)
        for eachDeath in deaths:

            if len(eachDeath) > 4 and eachDeath[3] != "'@Deaths:":

                date = eachDeath[1][1:]
                death = eachDeath[5:]
                player = death[0]
                player = player.lower()
                max_deaths = death[1][1:-1]
                #
                monster = death[7:]
                if monster[0] == 'Epic':
                    monster = monster[1:]

                monster = ' '.join(monster)[:-3]
                basefame = int(death[2][:-1])


                death_data['Total Recorded Deaths'] += 1
                # Collect 8/8 Deaths
                if max_deaths == '8/8':
                    death_data['Total 8/8 Deaths'] += 1


                #Collect Monster
                if monster not in monster_Log:
                    monster_Log.update({monster: 1})
                elif monster  in monster_Log:
                    monster_Log[monster] += 1

                # Collect Date of Death
                if date not in deaths_by_date:
                    deaths_by_date.update({date: 1})
                else:
                    deaths_by_date[date] += 1

                # Collect Player that died and their fame gained
                if player not in deaths_by_player and player not in blacklist:
                    if basefame > 0 and basefame <= 450:
                        deaths_by_player.update({player: basefame * 1})
                    elif basefame > 450 and basefame <= 1000:
                        deaths_by_player.update({player: basefame * 1.5})
                    elif basefame > 1000 and basefame <= 3500:
                        deaths_by_player.update({player: basefame * 2})
                    elif basefame > 3500 and basefame <= 5000:
                        deaths_by_player.update({player: basefame * 2.5})
                    elif basefame > 5000 and basefame <= 7500:
                        deaths_by_player.update({player: basefame * 3.5})
                    elif basefame > 7500 and basefame <= 9000:
                        deaths_by_player.update({player: basefame * 4})
                    elif basefame > 9000 and basefame <= 9999:
                        deaths_by_player.update({player: basefame * 4.5})
                    elif basefame >= 10000 and basefame <= 10500:
                        deaths_by_player.update({player: basefame * 7})
                    elif basefame > 10500 and basefame <= 12500:
                        deaths_by_player.update({player: basefame * 5.5})
                    elif basefame > 12500 and basefame <= 15000:
                        deaths_by_player.update({player: basefame * 5.75})
                    elif basefame > 15000 and basefame <= 29999:
                        deaths_by_player.update({player: basefame * 6})
                    elif basefame > 29999 and basefame <= 31000:
                        deaths_by_player.update({player: basefame * 6.5})
                    elif basefame > 31000 and basefame <= 99999:
                        deaths_by_player.update({player: basefame * 10})
                    elif basefame > 99999:
                        deaths_by_player.update({player: basefame * 13})

                elif player in deaths_by_player:
                    if basefame > 0 and basefame <= 450:
                        deaths_by_player[player] += basefame * 1
                    elif basefame > 450 and basefame <= 1000:
                        deaths_by_player[player] += basefame * 1.5
                    elif basefame > 1000 and basefame <= 3500:
                        deaths_by_player[player] += basefame * 2
                    elif basefame > 3500 and basefame <= 5000:
                        deaths_by_player[player] += basefame * 2.5
                    elif basefame > 5000 and basefame <= 7500:
                        deaths_by_player[player] += basefame * 3.5
                    elif basefame > 7500 and basefame <= 9000:
                        deaths_by_player[player] += basefame * 4
                    elif basefame > 9000 and basefame <= 9999:
                        deaths_by_player[player] += basefame * 4.5
                    elif basefame >= 10000 and basefame <= 10500:
                        deaths_by_player[player] += basefame * 7
                    elif basefame > 10500 and basefame <= 12500:
                        deaths_by_player[player] += basefame * 5.5
                    elif basefame > 12500 and basefame <= 15000:
                        deaths_by_player[player] += basefame * 5.75
                    elif basefame > 15000 and basefame <= 29999:
                        deaths_by_player[player] += basefame * 6
                    elif basefame > 29999 and basefame <= 31000:
                        deaths_by_player[player] += basefame * 6.5
                    elif basefame > 31000 and basefame <= 99999:
                        deaths_by_player[player] += basefame * 9
                    elif basefame > 99999:
                        deaths_by_player[player] += basefame * 13


                #Base fame Weighted slightly annoying
                if player not in blacklist:
                    if basefame > 0 and basefame <=450 :
                        death_data['Total Fame Gained(Estimated)'] += basefame * 1
                    elif basefame > 450 and basefame <= 1000:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 1.5
                    elif basefame > 1000 and basefame <= 3500:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 2
                    elif basefame > 3500 and basefame <= 5000:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 2.5
                    elif basefame > 5000 and basefame<= 7500:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 3.5
                    elif basefame > 7500 and basefame <= 9000:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 4
                    elif basefame > 9000 and basefame <= 9999:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 5
                    elif basefame >= 10000 and basefame<=10500:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 7
                    elif basefame > 10500 and basefame <= 12500:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 5.5
                    elif basefame > 12500 and basefame <= 15000:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 5.75
                    elif basefame > 15000 and basefame <= 29999:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 6
                    elif basefame > 29999 and basefame <= 31000:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 6.5
                    elif basefame > 31000 and basefame <= 99999:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 9
                    elif basefame > 99999:
                        death_data['Total Fame Gained(Estimated)'] += basefame * 13

        # Sort the Monsters/players High to low
        sorted_monsters = sorted(monster_Log.items(), key=operator.itemgetter(1), reverse=True)
        sorted_players = sorted(deaths_by_player.items(), key=operator.itemgetter(1), reverse=True)
        #Get top 10 monsters
        death_data['Top 10 Monsters'] = [sorted_monsters[x] for x in range(10)]
        #Get top 10 players exclude Blacklisted Players
        top_players = []
        for player in sorted_players:
            if player[0] not in blacklist and len(top_players) < 10:
                top_players.append(player)
            elif player[0] not in blacklist and len(top_players) >= 10:
                death_data['Top 10 Worst(best) players'] = top_players

        death_data.update({'Deaths by Date':deaths_by_date})

        # prints all death data we wanted just for testing
        #for k in death_data:
        #    print(k, death_data[k])
        return death_data


def death_gui():

    death_info = death_data()
    root = tk.Tk()
    root.title('Death Data - Mr.Squiddy')
    root.geometry('600x600')
    center(root)
    frame_bg = tk.Frame(root, width =600, height=600, bg='#a7f9fa')
    frame_bg.place(x=0,y=0)

    btn_back = tk.Button(root, text='Go Back', command=lambda: [root.destroy(), create_gui()], padx=5, pady=5,
                         font=("Helvetica", 12, "bold"), bd=5)
    btn_back.place(x=25, y=475)


    lbl_monster = tk.Label(root, text='Top 10 Monsters Epic Included',font=("Helvetica", 12, "bold"),bg='#d68709')
    lbl_monster.place(x=355, y=0)

    lbl_players = tk.Label(root, text='Top 10 Players Estimated Fame Gain',font=("Helvetica", 12, "bold"), bg='#d68709')
    lbl_players.place(x=25, y=0)

    lbl_deaths = tk.Label(root, text='Total Recorded Deaths',font=("Helvetica", 12, "bold"),bg='#d68709')
    lbl_deaths.place(x=25, y=545)
    lbl_deaths2 = tk.Label(root, text=("{:,}".format(death_info['Total Recorded Deaths'])+" Deaths"),font=("Helvetica", 10, "bold"),bg='#d68709')
    lbl_deaths2.place(x=25, y=575)

    lbl_deaths = tk.Label(root, text='Total 8/8 Deaths',font=("Helvetica", 12, "bold"),bg='#d68709')
    lbl_deaths.place(x=225, y=545)
    lbl_deaths = tk.Label(root, text=str("{:,}".format(death_info['Total 8/8 Deaths'])+' 8/8 Deaths'), font=("Helvetica", 10, "bold"),bg='#d68709')
    lbl_deaths.place(x=225, y=575)

    lbl_fame = tk.Label(root, text='Total Fame Gained(Estimated)', font=("Helvetica", 12, "bold"),bg='#d68709')
    lbl_fame.place(x=365, y=545)
    lbl_fame2 = tk.Label(root, text=str("{:,}".format(death_info['Total Fame Gained(Estimated)'])+' Fame'), font=("Helvetica", 10, "bold"),bg='#d68709')
    lbl_fame2.place(x=365, y=575)

    lbl_dailyfame = tk.Label(root, text='Average Daily Fame(PH)', font=("Helvetica", 12, "bold"),bg='#d68709')
    lbl_dailyfame.place(x=225, y=470)
    lbl_dailyfame2 = tk.Label(root, text=str("{:,}".format(round(death_info['Total Fame Gained(Estimated)']/len(death_info['Deaths by Date']))))+' Fame increase each day ', font=("Helvetica", 10, "bold"),bg='#d68709')
    lbl_dailyfame2.place(x=225, y=500)
    y=0
    for k in death_info['Top 10 Monsters']:

        y+=27
        tk.Label(root, text=k[0]+' '+"{:,}".format(k[1])+' Kills', font=("Helvetica", 10, "bold"), bg='#d68709').place(x=355,y=y)
    y=0
    for k in death_info['Top 10 Worst(best) players']:

        y+=27
        tk.Label(root, text=k[0].capitalize()+' '+"{:,}".format(k[1])+' Fame',font=("Helvetica", 10, "bold"),bg='#d68709').place(x=25,y=y)


    root.mainloop()
    #death_data = {'Total Recorded Deaths': 0, 'Total 8/8 Deaths': 0, 'Total Fame Gained(Estimated)': 0,
    #                 'Top 10 Monsters': [], 'Top 10 Worst(best) players': []}

def loot_gui():
    #loot_data = {'Total Primal Drops': 0, 'Total Legendary Drops': 0, '10 Most Common Primal Drops': 0,
    #             'Total Primals From Tokens': 0, '5 Most Common Primals(token)': 0, 'Drops Per Day': 0,
    #             'Top 10 Players Primal': 0, '10 Most Common Legendary Drops': 0, 'Top 10 Players Legendary': 0}

    loot_info = loot_data()
    root = tk.Tk()
    root.title('Loot Data - Mr.Squiddy')
    root.geometry('600x600')
    center(root)

    frame_bg = tk.Frame(root, width=600, height=600, bg='#a7f9fa')
    frame_bg.place(x=0, y=0)

    btn_back = tk.Button(root, text='Go Back', command=lambda: [root.destroy(), create_gui()], padx=5, pady=5, font=("Helvetica", 12, "bold"),bd=5)
    btn_back.place(x=10, y=550)

    lbl_total_primals = tk.Label(root, text='Total Primal Drops', font=("Helvetica", 12, "bold"),
                           bg='#d68709')
    lbl_total_primals.place(x=0, y=0)

    lbl_total_primals2 = tk.Label(root, text=str("{:,}".format(loot_info['Total Primal Drops']))+' Primals', font=("Helvetica", 10, "bold"),
                                 bg='#d68709')
    lbl_total_primals2.place(x=0, y=30)

    lbl_total_legendaries = tk.Label(root, text='Total Legendary Drops', font=("Helvetica", 12, "bold"),
                                 bg='#d68709')
    lbl_total_legendaries.place(x=160, y=0)

    lbl_total_legendaries2 = tk.Label(root, text=str("{:,}".format(loot_info['Total Legendary Drops'])) + ' Legendaries',
                                  font=("Helvetica", 10, "bold"),
                                  bg='#d68709')
    lbl_total_legendaries2.place(x=160, y=30)

    lbl_total_primals_tokens = tk.Label(root, text='Total Primals (Tokens)', font=("Helvetica", 12, "bold"),
                                 bg='#d68709')
    lbl_total_primals_tokens.place(x=355, y=0)

    lbl_total_primals_tokens = tk.Label(root, text=str("{:,}".format(loot_info['Total Primals From Tokens'])) + ' Primals', font=("Helvetica", 10, "bold"),
                                        bg='#d68709')
    lbl_total_primals_tokens.place(x=355, y=30)

    lbl_Top10_primals = tk.Label(root, text='Most Common Primals',font=("Helvetica", 12, "bold"),
                 bg='#d68709')
    lbl_Top10_primals.place(x=0, y= 80)
    y = 85
    for k in loot_info['10 Most Common Primal Drops']:
        y += 27
        tk.Label(root, text=k[0] + ' ' + "{:,}".format(k[1]) + ' Dropped', font=("Helvetica", 10, "bold"),
                 bg='#d68709').place(x=0, y=y)

    lbl_Top10_legendaries = tk.Label(root, text='Most Common Legendaries', font=("Helvetica", 12, "bold"),
                                 bg='#d68709')
    lbl_Top10_legendaries.place(x=300, y=80)
    y = 85
    for k in loot_info['10 Most Common Legendary Drops']:
        y += 27
        tk.Label(root, text=k[0] + ' ' + "{:,}".format(k[1]) + ' Dropped', font=("Helvetica", 10, "bold"),
                 bg='#d68709').place(x=300, y=y)

    lbl_Top10_Tokens = tk.Label(root, text='Most Common Token Drops', font=("Helvetica", 12, "bold"),
                                     bg='#d68709')
    lbl_Top10_Tokens.place(x=0, y=260)
    y = 265
    for k in loot_info['5 Most Common Primals(Tokens)']:
        y += 27
        tk.Label(root, text=k[0] + ' ' + "{:,}".format(k[1]) + ' Obtained', font=("Helvetica", 10, "bold"),
                 bg='#d68709').place(x=0, y=y)

    lbl_Top10_Players_Primal = tk.Label(root, text='Top 10 Primal Droppers (WIP)', font=("Helvetica", 12, "bold"),
                                bg='#d68709')
    lbl_Top10_Players_Primal.place(x=300, y=260)
    y = 265
    for k in loot_info['Top 10 Players Primals']:
        y += 27
        tk.Label(root, text=k[0].capitalize() + ' ' + "{:,}".format(k[1]) + ' Dropped', font=("Helvetica", 10, "bold"),
                 bg='#d68709').place(x=300, y=y)

    lbl_total_blocked = tk.Label(root, text='Blocked/Filtered Drops Count', font=("Helvetica", 12, "bold"),
                                     bg='#d68709')
    lbl_total_blocked.place(x=0, y=490)

    lbl_total_blocked2 = tk.Label(root,
                                      text=str("{:,}".format(loot_info['Filtered Drops'])) + ' Blocked Drops',
                                      font=("Helvetica", 10, "bold"),
                                      bg='#d68709')
    lbl_total_blocked2.place(x=0, y=520)

    root.mainloop()

def lookup_gui(player_name, root):
    root.destroy()

    death_info_specific = death_data_sepcific(player_name)
    loot_info_specific = loot_data_specific(player_name)

    #for entry in loot_info_specific:
    #    print(entry, loot_info_specific[entry])


    root = tk.Tk()
    root.title('Loot Data - Mr.Squiddy')
    root.geometry('600x600')
    center(root)

    frame_bg = tk.Frame(root, width=600, height=600, bg='#000000')
    frame_bg.place(x=0, y=0)

    btn_back = tk.Button(root, text='Go Back', command=lambda: [root.destroy(), create_gui()], padx=5, pady=5,
                         font=("Helvetica", 12, "bold"), bd=5)
    btn_back.place(x=10, y=550)

    lbl_loot_info = tk.Label(root, text='Death Info', font=("Helvetica", 12, "bold"),fg='#2bcaff', bg='#646970')
    lbl_loot_info.place(x=5, y=5)

    lbl_total_fame2 = tk.Label(root, text='Fame gained from death: '+str("{:,}".format(round(death_info_specific['Total Fame Gained(Estimated)']))), font=("Helvetica", 12, "bold"),
                                 bg='#d68709')
    lbl_total_fame2.place(x=5, y=35)


    lbl_total_death2 = tk.Label(root, text='Total Deaths: '+str(
        "{:,}".format(round(death_info_specific['Total Recorded Deaths']))),
                               font=("Helvetica", 12, "bold"),
                               bg='#d68709')
    lbl_total_death2.place(x=5, y=65)

    lbl_scary_death = tk.Label(root, text='Scariest Monster 8D: ' + str(death_info_specific['Player Monster Deaths'][0][0]),
                                font=("Helvetica", 12, "bold"),bg='#d68709')
    lbl_scary_death.place(x=5, y=95)

    lbl_highest_death = tk.Label(root, text='Highest Single Char Death(Estimate): ' + str("{:,}".format(round(death_info_specific['Highest Fame Death(Estimate)']))), font=("Helvetica", 12, "bold"), bg='#d68709')
    lbl_highest_death.place(x=5, y=125)

    lbl_days_died = tk.Label(root,text='Unique Days of active dying: ' + str(len(death_info_specific['Days of Deaths'])),
                               font=("Helvetica", 12, "bold"),
                               bg='#d68709')
    lbl_days_died.place(x=5, y=155)

    lbl_loot_info = tk.Label(root, text='Loot Info', font=("Helvetica", 12, "bold"),fg='#2bcaff', bg='#646970')
    lbl_loot_info.place(x=5, y=215)

    lbl_total_primal = tk.Label(root, text='Total # of Primal Drops: ' + str(
        "{:,}".format(round(loot_info_specific['Total Primal Drops']))), font=("Helvetica", 12, "bold"),
                                 bg='#d68709')
    lbl_total_primal.place(x=5, y=245)

    lbl_total_legendary = tk.Label(root, text='Total # of Legendary Drops: ' + str(
        "{:,}".format(round(loot_info_specific['Total Legendary Drops']))), font=("Helvetica", 12, "bold"),
                                bg='#d68709')
    lbl_total_legendary.place(x=5, y=275)

    lbl_daydrop = tk.Label(root, text='Avg drops per day: ' + str((round(loot_info_specific['Drops Per Day'], 2))), font=("Helvetica", 12, "bold"),
                                bg='#d68709')
    lbl_daydrop.place(x=5, y=305)

    lbl_days_played = tk.Label(root, text='Unique Days of active looting: ' + str((round(loot_info_specific['Days of activity']))),
                           font=("Helvetica", 12, "bold"),
                           bg='#d68709')
    lbl_days_played.place(x=5, y=335)

    lbl_common_leg = tk.Label(root,
                               text='Most Popular Legendary: ' +
                                    str(loot_info_specific['Most Common Legendary Drop'][0]) +' -> '+
                                    str(loot_info_specific['Most Common Legendary Drop'][1] ),
                                    font=("Helvetica", 12, "bold"),bg='#d68709')
    lbl_common_leg.place(x=5, y=365)

    lbl_common_primal = tk.Label(root,
                              text='Most Popular Legendary: ' +
                                   str(loot_info_specific['Most Common Primal Drop'][0]) + ' -> ' +
                                   str(loot_info_specific['Most Common Primal Drop'][1]),
                              font=("Helvetica", 12, "bold"), bg='#d68709')
    lbl_common_primal.place(x=5, y=395)

    lbl_token_primal = tk.Label(root,
                                 text='# of Token turn ins ' + str(loot_info_specific['200 Tokens Turned in']),
                                 font=("Helvetica", 12, "bold"), bg='#d68709')
    lbl_token_primal.place(x=5, y=425)

    lbl_playername = tk.Label(root,text=player_name.capitalize(),font=("Helvetica", 16, "bold"),fg='#2bcaff', bg='#646970')
    lbl_playername.place(x=120, y=550)
    root.mainloop()

def create_gui():

    # Grab the last time each file was updated
    final_date = final_dates()

    root = tk.Tk()
    root.title('RoTF Data Mr.Squiddy')
    root.geometry('600x600')
    center(root)
    frame = tk.Frame(root, bg='#a0f2d0', width=600, height=600)
    frame.place(anchor='n', x=300)

    lbl_Loot = tk.Label(frame, text='Last Updated '+final_date, font=("Helvetica", 10), bg="#a0f2d0")
    lbl_Loot.place(anchor='s', x=325, y=600)

    btn_Loot = tk.Button(root, text='Update Loots and Deaths',font=("Helvetica", 10), bd=5, command=
                         lambda: [root.destroy(), update_gui()])
    btn_Loot.place(anchor='s', x=515, y=600)

    btn_player_data = tk.Button(root, text='Player Lookup\n Case-Sensitive', height=6, width=15, bd=5, font=("Helvetica", 10),
                                command=lambda: [lookup_gui(entry_username.get().lower(), root)])
    btn_player_data.place(anchor='n', x=80, y= 375)

    btn_death_data = tk.Button(root, text='Show Death Data',height=6, width=15, bd=5, font=("Helvetica", 10),
                               command=lambda: [root.destroy(), death_gui()])
    btn_death_data.place(anchor='n', x=80, y=15)

    btn_loot_data = tk.Button(root, text='Show Loot Data', height=6, width=15, bd=5, font=("Helvetica", 10),
                              command=lambda: [root.destroy(), loot_gui()])
    btn_loot_data.place(anchor='n', x=80, y=145)

    lbl_button_info = tk.Label(root, text='This lets you lookup Data and information on Deaths for the entire '+
                                            "server or certain players. \n\nClick Show Death Data for for information on deaths ingame\n\n "+
                                            "Show Loot Data for information on Primals/Legendaries. "+
                                            "\n\n Finally hit Player Lookup to search for specific peoples Drops/Deaths \n as well as overall "+
                                            "average activity on the game, where the average is skewed towards current guild members DateTime Logs(WIP)"
                               , wraplength=350, bg='#f0ba46', font=("Helvetica", 14))
    lbl_button_info.place(anchor='n', x=345, y=15)

    entry_username = tk.Entry(root, width=22, font=("Helvetica", 12))
    entry_username.place(anchor='n',x=275, y=465)

    root.mainloop()


create_gui()