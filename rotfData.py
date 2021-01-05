import tkinter as tk
import pandas as pd


'''
Centers Window upon screen
Functions for most things in this project because It's easier for me to read and maintain.
'''


def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


'''
Gathers a specific players Death Data and returns in it in a Dictionary
 
'Total Recorded Deaths': total_deaths,
'Total Fame Gained(Estimated)': total_fame,
'Scariest Monster': {"monster": scariest_monster, "amount": scariest_monster_amount},
'Unique Days of Death': unique_death_days,
'Deadliest Day': {"date": deadliest_day, "amount": deadliest_day_amount},
'Highest Fame Death(Estimate)': highest_basefame_death
'''


def death_data_specific(player_name):
    cols = ['player', 'basefame', 'monster', 'date']
    file = "pandas_death.txt"

    deaths = pd.read_csv(file, delimiter=";", usecols=cols)
    specific_player = deaths.loc[deaths['player'] == player_name]
    total_deaths = specific_player.groupby("player").count().max()[0]
    total_fame = specific_player['basefame'].sum()
    unique_death_days = specific_player.groupby('date').count().sum()[0]
    scariest_monster = specific_player.groupby('monster').count().idxmax(axis=0)[0]
    scariest_monster_amount = specific_player.groupby('monster').count().max()[0]
    deadliest_day = specific_player.groupby('date').count().idxmax(axis=0)[0]
    deadliest_day_amount = specific_player.groupby('date').count().max()[0]
    highest_basefame_death = specific_player['basefame'].max()

    death_data = {'Total Recorded Deaths': total_deaths,
                  'Total Fame Gained(Estimated)': total_fame,
                  'Scariest Monster': {"monster": scariest_monster, "amount": scariest_monster_amount},
                  'Unique Days of Death': unique_death_days,
                  'Deadliest Day': {"date": deadliest_day, "amount": deadliest_day_amount},
                  'Highest Fame Death(Estimate)': highest_basefame_death}

    return death_data


'''
Gathers a specified players loot data (Primal, Legendary and Tokens) and returns in a dictionary (Some Nested)

 'Total Primal Drops': total_primal,
 'Total Legendary Drops': total_legendary,
 'Days of activity': unique_days,
 'Most Common Legendary Drop': {"item": legendary_common_item, "amount": legendary_common_amount},
 'Most Common Primal Drop': {"item": primal_common_item, "amount": primal_common_amount},
 '200 Tokens Turned in': total_necroptokens,
 'Best Day of Loot': {"day": best_day, "amount": best_day_drop_count}
'''


def loot_data_specific(player_name):

    cols = ['player', 'item', 'type', 'date']
    file = 'pandas_loot.txt'

    loots = pd.read_csv(file, delimiter=";", usecols=cols, )
    specific_player = loots.loc[loots['player'] == player_name]

    total_primal = specific_player.groupby('type').count()['player']['primal']
    total_legendary = specific_player.groupby('type').count()['player']['legendary']
    total_necroptokens = specific_player.groupby('type').count()['player']['Necrotic']
    best_day = (specific_player.groupby('date').count()).idxmax(axis=0)['player']
    best_day_drop_count = (specific_player.value_counts('date')[0])
    unique_days = (specific_player.groupby('date')).count().count()['player']
    primal_common_item = specific_player.loc[specific_player['type'] == 'primal'].groupby('item').count().idxmax()[0]
    primal_common_amount = specific_player.loc[specific_player['type'] == 'primal'].groupby('item').count()['player'].max()
    legendary_common_item = specific_player.loc[specific_player['type'] == 'legendary'].groupby('item').count().idxmax()[0]
    legendary_common_amount = specific_player.loc[specific_player['type'] == 'legendary'].groupby('item').count()[
        'player'].max()

    loot_data = {'Total Primal Drops': total_primal,
                 'Total Legendary Drops': total_legendary,
                 'Days of activity': unique_days,
                 'Most Common Legendary Drop': {"item": legendary_common_item, "amount": legendary_common_amount},
                 'Most Common Primal Drop': {"item": primal_common_item, "amount": primal_common_amount},
                 '200 Tokens Turned in': total_necroptokens,
                 'Best Day of Loot': {"day": best_day, "amount": best_day_drop_count}}

    return loot_data


'''
Gathers Interesting information about ALL drops within the lifetime of the server. Returns in a dictionary

'Total Primal Drops': total_primal,
'Total Legendary Drops': total_legendary,
'10 Most Common Primal Drops': top_10_primal.to_dict(),
'Total Primals From Tokens': total_tokens,
'5 Most Common Primals(token)': top_5_token.to_dict(),
'Drops Per Day': average_drops,
'Top 10 Players Primals': top_10_player_primal.to_dict('split'),
'10 Most Common Legendary Drops': top_10_legendary.to_dict(),
'Top 10 Players Legendary': top_10_player_legendary.to_dict('split'),
'Filtered Drops': 0 <-- Redacted Data Munging done outside of this program.
'''


def loot_data():

    cols = ['player', 'item', 'type', 'date']
    file = 'pandas_loot.txt'
    loots = pd.read_csv(file, delimiter=";", usecols=cols, )

    total_primal = loots.groupby('type').count()['player'][2]
    total_legendary = loots.groupby('type').count()['player'][1]
    total_tokens = loots.groupby('type').count()['player'][0]
    top_10_primal = loots[loots['type'] == 'primal'].groupby('item').count().nlargest(10, 'player')
    top_10_legendary = loots[loots['type'] == 'legendary'].groupby('item').count().nlargest(10, 'player')
    top_5_token = loots[loots['type'] == 'Necrotic'].groupby('item').count().nlargest(5, 'player')
    top_10_player_primal = loots[loots['type'] == 'primal'].groupby('player').count().reset_index().nlargest(10, 'item')
    top_10_player_legendary = loots[loots['type'] == 'legendary'].groupby('player').count().reset_index().nlargest(10, 'item')
    average_drops = loots.count()[0] / loots['date'].nunique()


    loot_data = {'Total Primal Drops': total_primal,
                 'Total Legendary Drops': total_legendary,
                 '10 Most Common Primal Drops': top_10_primal.to_dict(),
                 'Total Primals From Tokens': total_tokens,
                 '5 Most Common Primals(token)': top_5_token.to_dict(),
                 'Drops Per Day': average_drops,
                 'Top 10 Players Primals': top_10_player_primal.to_dict('split'),
                 '10 Most Common Legendary Drops': top_10_legendary.to_dict(),
                 'Top 10 Players Legendary': top_10_player_legendary.to_dict('split'),
                 'Filtered Drops': 0}

    return loot_data


'''
Gathers interesting information about ALL player deaths in the servers lifetime. Returns in a dictionary
And may be expanded upon.

'Total Recorded Deaths': total_deaths, 
'Total Fame Gained(Estimated)': total_fame,
'Top 10 Monsters': top_10_monsters, 
'Top 10 Worst(best) players': top_10_players,
'Average Daily Fame': avg_daily_fame
'''


def death_data():
    cols = ['player', 'basefame', 'monster', 'date']
    deaths = pd.read_csv("pandas_death.txt", delimiter=";", usecols=cols)

    total_deaths = deaths.count()[0]
    total_fame = deaths['basefame'].sum()
    top_10_monsters = deaths.groupby("monster").count().reset_index().nlargest(10, 'player').to_dict('split')
    top_10_players = deaths.groupby("player").sum().reset_index().nlargest(10, 'basefame').to_dict('split')
    avg_daily_fame = ((deaths.groupby("date").sum().sum()) / (deaths.groupby("date").sum().count()))[0]


    death_data = {'Total Recorded Deaths': total_deaths, 'Total Fame Gained(Estimated)': total_fame,
                  'Top 10 Monsters': top_10_monsters, 'Top 10 Worst(best) players': top_10_players,
                  'Average Daily Fame': avg_daily_fame}

    return death_data


'''
The rest is entirely GUI related, the GUI was made vert hastily during final exam times when I wouldn't be on much.
I wanted to be sure guildies could lookup information (primarily on specific players) while I was away.
'''


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
    btn_back.place(x=5, y=530)


    lbl_monster = tk.Label(root, text='Top 10 Monsters Epic Included',font=("Helvetica", 12, "bold"),bg='#d68709')
    lbl_monster.place(x=355, y=0)
    parse = death_info['Top 10 Monsters']
    y = 0
    for k in parse['data']:
        y += 27
        tk.Label(root, text=k[0] + ' ' + "{:,}".format(k[1]) + ' Kills', font=("Helvetica", 10, "bold"),
                 bg='#d68709').place(x=355, y=y)

    lbl_players = tk.Label(root, text='Top 10 Players Estimated Fame Gain',font=("Helvetica", 12, "bold"), bg='#d68709')
    lbl_players.place(x=25, y=0)
    parse = death_info['Top 10 Worst(best) players']
    y = 0
    for k in parse['data']:
        y += 27
        tk.Label(root, text=k[0].capitalize() + ' ' + "{:,}".format(k[1]) + ' Fame', font=("Helvetica", 10, "bold"),
                 bg='#d68709').place(x=25, y=y)

    lbl_deaths = tk.Label(root, text='Total Recorded Deaths',font=("Helvetica", 12, "bold"), bg='#d68709')
    lbl_deaths.place(x=365, y=400)
    lbl_deaths2 = tk.Label(root, text=str("{:,}".format(death_info['Total Recorded Deaths'])+" Deaths"), font=("Helvetica", 10, "bold"), bg='#d68709')
    lbl_deaths2.place(x=365, y=430)

    lbl_fame = tk.Label(root, text='Total Fame Gained(Estimated)', font=("Helvetica", 12, "bold"),bg='#d68709')
    lbl_fame.place(x=365, y=545)
    lbl_fame2 = tk.Label(root, text=str("{:,}".format(death_info['Total Fame Gained(Estimated)'])+' Fame'), font=("Helvetica", 10, "bold"), bg='#d68709')
    lbl_fame2.place(x=365, y=575)

    lbl_dailyfame = tk.Label(root, text='Average Daily Fame', font=("Helvetica", 12, "bold"),bg='#d68709')
    lbl_dailyfame.place(x=365, y=470)
    lbl_dailyfame2 = tk.Label(root, text=str("{:,}".format(round(death_info['Average Daily Fame'])))+'~ Fame injected each day ', font=("Helvetica", 10, "bold"),bg='#d68709')
    lbl_dailyfame2.place(x=365, y=500)

    root.mainloop()


def loot_gui():

    loot_info = loot_data()
    root = tk.Tk()
    root.title('Loot Data - Mr.Squiddy')
    root.geometry('1200x800')
    center(root)

    frame_bg = tk.Frame(root, width=1200, height=800, bg='#a7f9fa')
    frame_bg.place(x=0, y=0)

    btn_back = tk.Button(root, text='Go Back', command=lambda: [root.destroy(), create_gui()], padx=5, pady=5, font=("Helvetica", 12, "bold"),bd=5)
    btn_back.place(x=10, y=745)

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
    parse = loot_info['Top 10 Players Primals']
    for k in parse['data']:
        y += 27
        tk.Label(root, text= k[0] + ' ' + "{:,}".format(k[1]) + ' Dropped', font=("Helvetica", 10, "bold"),
                 bg='#d68709').place(x=0, y=y)


    lbl_Top10_legendaries = tk.Label(root, text='Most Common Legendaries', font=("Helvetica", 12, "bold"),
                                 bg='#d68709')
    lbl_Top10_legendaries.place(x=300, y=80)
    y = 85
    parse = loot_info['10 Most Common Legendary Drops']['player']
    for k in parse:
        y += 27
        tk.Label(root, text=k + ' ' + "{:,}".format(parse[k]) + ' Dropped', font=("Helvetica", 10, "bold"),
                 bg='#d68709').place(x=300, y=y)

    lbl_Top10_Tokens = tk.Label(root, text='Most Common Token Drops', font=("Helvetica", 12, "bold"),
                                     bg='#d68709')
    lbl_Top10_Tokens.place(x=0, y=410)
    y = 420
    parse = loot_info['5 Most Common Primals(token)']['player']
    for k in parse:
        y += 27
        tk.Label(root, text=k + ' ' + "{:,}".format(parse[k]) + ' Obtained', font=("Helvetica", 10, "bold"),
                 bg='#d68709').place(x=0, y=y)

    lbl_Top10_Players_Primal = tk.Label(root, text='Top 10 Primal Droppers', font=("Helvetica", 12, "bold"),
                                bg='#d68709')
    lbl_Top10_Players_Primal.place(x=600, y=80)
    y = 85
    parse = loot_info['Top 10 Players Primals']
    for k in parse['data']:
        y += 27
        tk.Label(root, text=k[0].capitalize() + ' ' + "{:,}".format(k[1]) + ' Dropped', font=("Helvetica", 10, "bold"),
                 bg='#d68709').place(x=600, y=y)

    lbl_Top10_Players_Lege = tk.Label(root, text='Top 10 Legendary Droppers', font=("Helvetica", 12, "bold"),
                                        bg='#d68709')
    lbl_Top10_Players_Lege.place(x=800, y=80)
    y = 85
    parse = loot_info['Top 10 Players Legendary']
    for k in parse['data']:
        y += 27
        tk.Label(root, text=k[0].capitalize() + ' ' + "{:,}".format(k[1]) + ' Dropped', font=("Helvetica", 10, "bold"),
                 bg='#d68709').place(x=800, y=y)

    root.mainloop()


def player_check(player_name):
    deaths = pd.read_csv("pandas_death.txt", delimiter=";")
    loots = pd.read_csv("pandas_loot.txt", delimiter=";")
    if len(deaths[deaths['player'] == player_name]) == 0 or len(loots[loots['player'] == player_name]) == 0:
        return True
    else:
        return False


def lookup_gui(player_name, root):


    if player_check(player_name):
        root.destroy()
        create_gui()
    else:
        root.destroy()
        death_info_specific = death_data_specific(player_name)
        loot_info_specific = loot_data_specific(player_name)


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

        lbl_scary_death = tk.Label(root, text='Scariest Monster 8D: ' + str(death_info_specific['Scariest Monster']),
                                    font=("Helvetica", 12, "bold"),bg='#d68709')
        lbl_scary_death.place(x=5, y=95)

        lbl_highest_death = tk.Label(root, text='Highest Single Char Death(Estimate): ' + str("{:,}".format(round(death_info_specific['Highest Fame Death(Estimate)']))), font=("Helvetica", 12, "bold"), bg='#d68709')
        lbl_highest_death.place(x=5, y=125)

        lbl_days_died = tk.Label(root,text='Unique Days of active dying: ' + str(death_info_specific['Unique Days of Death']),
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

        lbl_days_played = tk.Label(root, text='Unique Days of active looting: ' + str((round(loot_info_specific['Days of activity']))),
                               font=("Helvetica", 12, "bold"),
                               bg='#d68709')
        lbl_days_played.place(x=5, y=305)

        lbl_common_leg = tk.Label(root,
                                   text='Most Popular Legendary: ' +
                                        str(loot_info_specific['Most Common Legendary Drop']["item"]) +' -> '+
                                        str(loot_info_specific['Most Common Legendary Drop']["amount"] ),
                                        font=("Helvetica", 12, "bold"),bg='#d68709')
        lbl_common_leg.place(x=5, y=365)

        lbl_common_primal = tk.Label(root,
                                  text='Most Popular Primal: ' +
                                       str(loot_info_specific['Most Common Primal Drop']["item"]) + ' -> ' +
                                       str(loot_info_specific['Most Common Primal Drop']["amount"]),
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


    root = tk.Tk()
    root.title('RoTF Data Mr.Squiddy')
    root.geometry('600x600')
    center(root)
    frame = tk.Frame(root, bg='#a0f2d0', width=600, height=600)
    frame.place(anchor='n', x=300)

    lbl_Loot = tk.Label(frame, text='Last Updated: Game Dead', font=("Helvetica", 10), bg="#a0f2d0")
    lbl_Loot.place(anchor='s', x=325, y=600)


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

    btn_player_data = tk.Button(root, text='Player Lookup', height=6, width=15, bd=5, font=("Helvetica", 10),
                                command=lambda: [lookup_gui(entry_username.get().lower(), root)])
    btn_player_data.place(anchor='n', x=80, y=375)

    root.mainloop()


create_gui()
