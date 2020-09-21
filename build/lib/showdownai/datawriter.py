from gamestateEdited import GameState, Pokemon, Team
import re
import csv
class Datawriter():
    def __init__(self):
        t = open("../log_scraper/data/userList.txt", "r")
        n = len(t.readlines())
        self.n = n
    def run(self):
        with open('data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Turn', 'Health 1.1', 'Health 1.2', 'Health 1.3', 'Health 1.4', 'Health 1.5', 'Health 1.6', 'Health 2.1', 'Health 2.2', 'Health 2.3', 'Health 2.4', 'Health 2.5', 'Health 2.6',\
                             'Species 1.1', 'Species 1.2', 'Species 1.3', 'Species 1.4', 'Species 1.5', 'Species 1.6', 'Species 2.1', 'Species 2.2', 'Species 2.3', 'Species 2.4', 'Species 2.5', 'Species 2.6',\
                             'Active 1', 'Active 2', 'Item 1', 'Item 2', 'Atk Stage 1', 'Def Stage 1', 'SpA Stage 1', 'SpD Stage 1', 'Speed Stage 1', 'Atk Stage 2', 'Def Stage 2', 'SpA Stage 2', 'SpD Stage 2', 'Speed Stage 2',\
                             'Seeds 1', 'Seeds 2', 'Status 1.1', 'Status 1.2', 'Status 1.3', 'Status 1.4', 'Status 1.5', 'Status 1.6', 'Status 2.1', 'Status 2.2', 'Status 2.3', 'Status 2.4', 'Status 2.5', 'Status 2.6',\
                             'Effective 1', 'Effective 2', 'Taunt 1', 'Taunt 2', 'Encore 1', 'Encore 2', 'Disable 1', 'Disable 2', 'Substitute 1', 'Substitute 2', 'Mega 1', 'Mega 2', 'ZMove 1', 'ZMove 2',\
                             'Rocks 1', 'Rocks 2', 'Spikes 1', 'Spikes 2', 'TSpikes 1', 'TSpikes 2', 'Webs 1', 'Webs 2', 'Reflect 1', 'Reflect 2', 'LScreen 1', 'LScreen 2', 'Weather', 'Terrain', 'Room', 'Winner'])
            #for each replay, write data into csv file to be analyzed by machine learning program
            for i in range(self.n):
                #open replay file
                text = open("../log_scraper/data/" + str(i) + ".txt", "r", encoding = 'utf-8')
                #identify winner
                txt = text.read()
                index = txt.find("win|")
                index2 = txt.find("|", index + 4)
                winner = txt[index + 4 : index2 - 1]
                index = txt.find("|player|p1|")
                index2 = txt.find("|", index + 11)
                if winner == txt[index + 11 : index2]:
                    victor = 0
                else:
                    victor = 1
                #create p1 team
                pList = []
                for j in range(6):
                    index = txt.find("|poke|p1|", index + 1)
                    index2 = txt.find("|item", index)
                    s = txt[index + 9:index2]
                    name = s.split(",")[0]
                    p = Pokemon(name)
                    pList.append(p)
                team1 = Team(pList)
                #create p2 team
                pList2 = []
                for j in range(6):
                    index = txt.find("|poke|p2|", index + 1)
                    index2 = txt.find("|item", index)
                    s = txt[index + 9:index2]
                    name = s.split(",")[0]
                    p = Pokemon(name)
                    pList2.append(p)
                team2 = Team(pList2)
                gs = GameState((team1, team2))
                index = txt.find("|start")
                turn = 0
                #update gamestate every turn, check for every feature in csv file
                oncemore = iter([True, False])
                while txt.find("|turn|", index + 1) > 0 or next(oncemore):
                    prevIndex = index
                    index = txt.find("|turn|", index + 1)
                    if index < 0:
                        index = len(txt) - 1
                    #check for megas
                    if txt.find("|-mega|p1a: ", prevIndex, index) > 0:
                        p = gs.get_team(0).sel().mega_evolve()
                        gs.get_team(0).replacePokemon(gs.get_team(0).selected, p)
                    if txt.find("|-mega|p2a: ", prevIndex, index) > 0:
                        p = gs.get_team(1).sel().mega_evolve()
                        gs.get_team(1).replacePokemon(gs.get_team(1).selected, p)
                    #check to update stat stages for p1 pokemon
                    prev = prevIndex
                    for j in range(6):
                        if txt.find("|-boost|p1a:", prev, index) > 0:
                            temp = txt.find("|-boost|p1a:", prev, index)
                            temp2 = txt.find("|", temp + 9)
                            stat = txt[temp2 + 1:temp2 + 4]
                            n = int(txt[temp2 + 5:temp2 + 6])
                            if stat == "eva":
                                n = int(txt[temp2 + 9:temp2 + 10])
                            else:
                                n = int(txt[temp2 + 5:temp2 + 6])
                            active = gs.get_team(0).sel()
                            active.increase_stage(stat, n)
                            prev = temp2
                        elif txt.find("|-unboost|p1a:", prev, index) > 0:
                            temp = txt.find("|-unboost|p1a:", prev, index)
                            temp2 = txt.find("|", temp + 9)
                            stat = txt[temp2 + 1:temp2 + 4]
                            n = int(txt[temp2 + 5:temp2 + 6])
                            active = gs.get_team(0).sel()
                            active.decrease_stage(stat, n)
                            prev = temp2
                    #check to update stat stages for p2 pokemon
                    prev = prevIndex
                    for j in range(6):
                        if txt.find("|-boost|p2a:", prev, index) > 0:
                            temp = txt.find("|-boost|p2a:", prev, index)
                            temp2 = txt.find("|", temp + 14)
                            stat = txt[temp2 + 1:temp2 + 4]
                            if stat == "eva":
                                n = int(txt[temp2 + 9:temp2 + 10])
                            else:
                                n = int(txt[temp2 + 5:temp2 + 6])
                            active = gs.get_team(1).sel()
                            active.increase_stage(stat, n)
                            prev = temp2
                        elif txt.find("|-unboost|p2a:", prev, index) > 0:
                            temp = txt.find("|-unboost|p2a:", prev, index)
                            temp2 = txt.find("|", temp + 14)
                            stat = txt[temp2 + 1:temp2 + 4]
                            if stat == "eva":
                                n = int(txt[temp2 + 9:temp2 + 10])
                            else:
                                n = int(txt[temp2 + 5:temp2 + 6])
                            active = gs.get_team(1).sel()
                            active.decrease_stage(stat, n)
                            prev = temp2
                    #check for active weather
                    temp = prevIndex
                    for i in range(2):
                        if txt.find("|-weather|", temp + 1, index) > 0:
                            temp = txt.find("|-weather|", temp + 1, index)
                            if txt[temp + 10:temp + 14] == "Rain":
                                gs.weather = "Rain"
                            elif txt[temp + 10:temp + 14] == "Sunn":
                                gs.weather = "Sun"
                            elif txt[temp + 10:temp + 14] == "Sand":
                                gs.weather = "Sand"
                            elif txt[temp + 10:temp + 14] == "Hail":
                                gs.weather = "Hail"
                            elif txt[temp + 10:temp + 14] == "none":
                                gs.weather = "None"
                    #check for active terrain/trick room
                    temp = prevIndex
                    for i in range(2):
                        if txt.find("|-fieldstart|move: ", temp + 1, index) > 0:
                            temp = txt.find("|-fieldstart|move: ", temp + 1, index)
                            if txt[temp + 19:temp + 24] == "Elect":
                                gs.terrain = "Electric"
                            elif txt[temp + 19:temp + 24] == "Psych":
                                gs.terrain = "Psychic"
                            elif txt[temp + 19:temp + 24] == "Grass":
                                gs.terrain = "Grassy"
                            elif txt[temp + 19:temp + 24] == "Misty":
                                gs.terrain = "Misty"
                            if txt[temp + 19:temp + 24] == "Trick":
                                gs.room = not gs.room
                        elif txt.find("|-fieldend|move: ", prevIndex, index) > 0:
                            temp = txt.find("|-fieldend|move: ", prevIndex, index)
                            if "Trick Room" in txt[temp + 17:temp + 27]:
                                gs.room = False
                            else:
                                gs.terrain = "None"
                    #check for hazards/screens going up
                    if txt.find("|-sidestart|p1: ", prevIndex, index) > 0:
                        temp = txt.find("|-sidestart|p1: ", prevIndex, index)
                        temp2 = txt.find("|", temp + 15, index)
                        if "Stealth" in txt[temp2:temp2 + 16]:
                            gs.set_rocks(0, True)
                        elif "Sticky" in txt[temp2:temp2 + 16]:
                            gs.webs[0] = True
                        elif "Toxic" in txt[temp2:temp2 + 16] and gs.tspikes[0] < 2:
                            gs.tspikes[0] += 1
                        elif "Spikes" in txt[temp2:temp2 + 16] and gs.spikes[0] < 3:
                            gs.add_spikes(0)
                        elif "Reflect" in txt[temp2:temp2 + 16]:
                            gs.screens[0][0] = True
                        elif "Light" in txt[temp2:temp2 + 16]:
                            gs.screens[0][1] = True
                        elif "Aurora" in txt[temp2:temp2 + 16]:
                            gs.screens[0] = (True, True)
                    if txt.find("|-sidestart|p2: ", prevIndex, index) > 0:
                        temp = txt.find("|-sidestart|p2: ", prevIndex, index)
                        temp2 = txt.find("|", temp + 15, index)
                        if "Stealth" in txt[temp2:temp2 + 16]:
                            gs.set_rocks(1, True)
                        elif "Sticky" in txt[temp2:temp2 + 16]:
                            gs.webs[1] = True
                        elif "Toxic" in txt[temp2:temp2 + 16] and gs.tspikes[1] < 2:
                            gs.tspikes[1] += 1
                        elif "Spikes" in txt[temp2:temp2 + 16] and gs.spikes[1] < 3:
                            gs.add_spikes(1)
                        elif "Reflect" in txt[temp2:temp2 + 16]:
                            gs.screens[1][0] = True
                        elif "Light" in txt[temp2:temp2 + 16]:
                            gs.screens[1][1] = True
                        elif "Aurora" in txt[temp2:temp2 + 16]:
                            gs.screens[1] = (True, True)
                    #check for hazards/screens being removed
                    if txt.find("|-sideend|p1: ", prevIndex, index) > 0:
                        temp = txt.find("|-sideend|p1: ", prevIndex, index)
                        temp2 = txt.find("[from] move: ", temp, index)
                        if txt[temp2 + 13:temp2 + 18] == "Defog":
                            gs.rocks[0] = False
                            gs.rocks[1] = False
                            gs.spikes[0] = 0
                            gs.spikes[1] = 0
                            gs.tspikes[0] = 0
                            gs.tspikes[1] = 0
                            gs.webs[0] = False
                            gs.webs[1] = False
                            gs.screens[1] = (False, False)
                        elif txt[temp2 + 13:temp2 + 18] == "Rapid":
                            gs.rocks[0] = False
                            gs.spikes[0] = 0
                            gs.tspikes[0] = 0
                            gs.webs[0] = False
                        temp2 = txt.find("|move: ", temp, index)
                        if "Reflect" in txt[temp2 + 7:temp2 + 19]:
                            gs.screens[0][0] = False
                        elif "Light Screen" in txt[temp2 + 7:temp2 + 19]:
                            gs.screens[0][1] = False
                        elif "Aurora Veil" in txt[temp2 + 7:temp2 + 19]:
                            gs.screens[0] = (False, False)
                    if txt.find("|-sideend|p2: ", prevIndex, index) > 0:
                        temp = txt.find("|-sideend|p2: ", prevIndex, index)
                        temp2 = txt.find("[from] move: ", temp, index)
                        if txt[temp2 + 13:temp2 + 18] == "Defog":
                            gs.rocks[0] = False
                            gs.rocks[1] = False
                            gs.spikes[0] = 0
                            gs.spikes[1] = 0
                            gs.tspikes[0] = 0
                            gs.tspikes[1] = 0
                            gs.webs[0] = False
                            gs.webs[1] = False
                            gs.screens[0] = (False, False)
                        elif txt[temp2 + 13:temp2 + 18] == "Rapid":
                            gs.rocks[1] = False
                            gs.spikes[1] = 0
                            gs.tspikes[1] = 0
                            gs.webs[1] = False
                        temp2 = txt.find("|move: ", temp, index)
                        if "Reflect" in txt[temp2 + 7:temp2 + 19]:
                            gs.screens[1][0] = False
                        elif "Light Screen" in txt[temp2 + 7:temp2 + 19]:
                            gs.screens[1][1] = False
                        elif "Aurora Veil" in txt[temp2 + 7:temp2 + 19]:
                            gs.screens[1] = (False, False)
                    #check for status
                    if txt.find("|-status|p1a: ", prevIndex, index) > 0:
                        temp = txt.find("|-status|p1a: ", prevIndex, index)
                        temp2 = txt.find("|", temp + 14, index)
                        gs.get_team(0).sel().set_status(txt[temp2 + 1: temp2 + 4])
                    if txt.find("|-activate|p1a: ", prevIndex, index) > 0:
                        temp = txt.find("|-activate|p1a: ")
                        temp2 = txt.find("|move: ", temp + 16, index)
                        temp3 = txt.find("|", temp2 + 7)
                        if "Aromatherapy" in txt[temp2 + 7:temp3] or "Heal Bell" in txt[temp2 + 7:temp3]:
                            for p in gs.get_team(0):
                                p.set_status("None")
                        elif "Refresh" or "Rest" in txt[temp2 + 7:temp3]:
                            gs.get_team(0).sel().set_status("None")
                    if txt.find("|-status|p2a: ", prevIndex, index) > 0:
                        temp = txt.find("|-status|p2a: ", prevIndex, index)
                        temp2 = txt.find("|", temp + 14, index)
                        gs.get_team(1).sel().set_status(txt[temp2 + 1: temp2 + 4])
                    if txt.find("|-activate|p2a: ") > 0:
                        temp = txt.find("|-activate|p2a: ", prevIndex, index)
                        temp2 = txt.find("|move: ", temp + 16, index)
                        temp3 = txt.find("|", temp2 + 7)
                        if "Aromatherapy" in txt[temp2 + 7:temp3] or "Heal Bell" in txt[temp2 + 7:temp3]:
                            for p in gs.get_team(1):
                                p.set_status("None")
                        elif "Refresh" or "Rest" in txt[temp2 + 7:temp3]:
                            gs.get_team(1).sel().set_status("None")
                    #check for loss of item
                    if txt.find("|-enditem|p1a: ", prevIndex, index) > 0:
                        gs.get_team(0).sel().item = False
                    if txt.find("|-enditem|p2a: ", prevIndex, index) > 0:
                        gs.get_team(1).sel().item = False
                    #check for damage
                    switch = txt.find("|switch|p1a:", prevIndex, index)
                    if max(txt.rfind("|-damage|p1a: ", prevIndex, index), txt.rfind("|-heal|p1a: ", prevIndex, index)) > 0 and (switch < 0 or switch > max(txt.find("|-damage|p1a: ", prevIndex, index), txt.find("|-heal|p1a: ", prevIndex, index))):
                        if switch < 0:
                            switch = index
                        damage = txt.rfind("|-damage|p1a: ", prevIndex, switch)
                        heal = txt.rfind("|-heal|p1a: ", prevIndex, switch)
                        temp = max(damage, heal)
                        temp2 = txt.find("|", temp + 14)
                        if txt[temp2 + 1:temp2 + 6] == "0 fnt":
                            gs.get_team(0).sel().hp = 0
                            gs.get_team(0).sel().alive = False
                            gs.get_team(0).sel().is_mega = False
                        else:
                            temp3 = txt.find("\/", temp2)
                            temp4 = txt.find("|", temp3)
                            hp = float(txt[temp2 + 1:temp3])
                            hpTotal = float(txt[temp3 + 2:temp3 + 5])
                            percent = int(hp/hpTotal * 100)
                            gs.get_team(0).sel().hp = percent
                    switch = txt.find("|switch|p2a:", prevIndex, index)
                    if max(txt.rfind("|-damage|p2a: ", prevIndex, index), txt.rfind("|-heal|p2a: ", prevIndex, index)) > 0 and (switch < 0 or switch > max(txt.find("|-damage|p2a: ", prevIndex, index), txt.find("|-heal|p2a: ", prevIndex, index))):
                        if switch < 0:
                            switch = index
                        damage = txt.rfind("|-damage|p2a: ", prevIndex, switch)
                        heal = txt.rfind("|-heal|p2a: ", prevIndex, switch)
                        temp = max(damage, heal)
                        temp2 = txt.find("|", temp + 14)
                        if txt[temp2 + 1:temp2 + 6] == "0 fnt":
                            gs.get_team(1).sel().hp = 0
                            gs.get_team(1).sel().alive = False
                            gs.get_team(1).sel().is_mega = False
                        else:
                            temp3 = txt.find("\/", temp2)
                            temp4 = txt.find("|", temp3)
                            hp = float(txt[temp2 + 1:temp3])
                            hpTotal = float(txt[temp3 + 2:temp3 + 5])
                            percent = int(hp/hpTotal * 100)
                            gs.get_team(1).sel().hp = percent
                    #check effectiveness of move, not sure if this is necessary
                    if txt.find("|-supereffective|p1a: ", prevIndex, index) > 0:
                        gs.get_team(0).sel().effective = 2
                    elif txt.find("|-resisted|p1a: ", prevIndex, index) > 0:
                        gs.get_team(0).sel().effective = 0
                    elif txt.find("|-immune|p1a: ", prevIndex, index) > 0:
                        gs.get_team(0).sel().effective = -1
                    else:
                        gs.get_team(0).sel().effective = 1
                    if txt.find("|-supereffective|p2a: ", prevIndex, index) > 0:
                        gs.get_team(1).sel().effective = 2
                    elif txt.find("|-resisted|p2a: ", prevIndex, index) > 0:
                        gs.get_team(1).sel().effective = 0
                    elif txt.find("|-immune|p2a: ", prevIndex, index) > 0:
                        gs.get_team(1).sel().effective = -1
                    else:
                        gs.get_team(1).sel().effective = 1
                    #deal with miscellaneous "start" effects
                    if txt.find("|-start|p1a: ", prevIndex, index) > 0:
                        temp = txt.find("|-start|p1a: ", prevIndex, index)
                        temp2 = txt.find("|", temp + 13, index)
                        if "Taunt" in txt[temp2 + 7:temp2 + 14]:
                            gs.get_team(0).sel().set_taunt(True)
                        if "Encore" in txt[temp2 + 7:temp2 + 14]:
                            gs.get_team(0).sel().set_encore(True)
                        if "Disable" in txt[temp2 + 7:temp2 + 14]:
                            gs.get_team(0).sel().set_disabled(True)
                        if "Sub" in txt[temp2 + 1:temp2 + 11]:
                            gs.get_team(0).sel().sub = True
                    if txt.find("|-start|p2a: ", prevIndex, index) > 0:
                        temp = txt.find("|-start|p2a: ", prevIndex, index)
                        temp2 = txt.find("|", temp + 13, index)
                        if "Taunt" in txt[temp2 + 7:temp2 + 14]:
                            gs.get_team(1).sel().set_taunt(True)
                        if "Encore" in txt[temp2 + 7:temp2 + 14]:
                            gs.get_team(1).sel().set_encore(True)
                        if "Disable" in txt[temp2 + 7:temp2 + 14]:
                            gs.get_team(1).sel().set_disabled(True)
                        if "Sub" in txt[temp2 + 1:temp2 + 11]:
                            gs.get_team(1).sel().sub = True
                    if txt.find("|-end|p1a: ", prevIndex, index) > 0:
                        temp = txt.find("|-end|p1a: ", prevIndex, index)
                        temp2 = txt.find("|", temp + 11, index)
                        if "Taunt" in txt[temp2 + 7:temp2 + 14]:
                            gs.get_team(0).sel().set_taunt(False)
                        if "Encore" in txt[temp2 + 7:temp2 + 14]:
                            gs.get_team(0).sel().set_encore(False)
                        if "Disable" in txt[temp2 + 7:temp2 + 14]:
                            gs.get_team(0).sel().set_disabled(False)
                        if "Sub" in txt[temp2 + 1:temp2 + 11]:
                            gs.get_team(0).sel().sub = False
                    if txt.find("|-end|p2a: ", prevIndex, index) > 0:
                        temp = txt.find("|-end|p2a: ", prevIndex, index)
                        temp2 = txt.find("|", temp + 11, index)
                        if "Taunt" in txt[temp2 + 7:temp2 + 14]:
                            gs.get_team(1).sel().set_taunt(False)
                        if "Encore" in txt[temp2 + 7:temp2 + 14]:
                            gs.get_team(1).sel().set_encore(False)
                        if "Disable" in txt[temp2 + 7:temp2 + 14]:
                            gs.get_team(1).sel().set_disabled(False)
                        if "Sub" in txt[temp2 + 1:temp2 + 11]:
                            gs.get_team(1).sel().sub = False
                    #check for z moves
                    if txt.find("|-zpower|p1a: ", prevIndex, index) > 0:
                        gs.get_team(0).sel().z_move = True
                    if txt.find("|-zpower|p2a: ", prevIndex, index) > 0:
                        gs.get_team(1).sel().z_move = True
                    #check for switches
                    prev1 = prevIndex
                    prev2 = prevIndex
                    i1 = index
                    i2 = index
                    for i in range(7):
                        if txt.find("|switch|p1a:", prev1, index) > 0:
                            temp = txt.find("|switch|p1a:", prev1, index)
                            temp2 = txt.find("\/", temp, index)
                            i1 = txt.find("|switch|p1a:", temp2, index)
                            if i1 < 0:
                                i1 = index
                            s = txt[temp:temp2]
                            pokemon = re.split('[^a-zA-Z\d-]', s)[5]
                            i = 0
                            for p in team1:
                                if p.species == pokemon:
                                    gs.switch_pokemon(i, 0)
                                i+=1
                            damage = txt.rfind("|-damage|p1a: ", temp, i1)
                            heal = txt.rfind("|-heal|p1a: ", temp, i1)
                            if max(damage, heal) > 0:
                                temp = max(damage, heal)
                                temp2 = txt.find("|", temp + 14)
                                if txt[temp2 + 1:temp2 + 6] == "0 fnt":
                                    gs.get_team(0).sel().hp = 0
                                    gs.get_team(0).sel().alive = False
                                    gs.get_team(0).sel().is_mega = False
                                else:
                                    temp3 = txt.find("\/", temp2)
                                    temp4 = txt.find("|", temp3)
                                    hp = float(txt[temp2 + 1:temp3])
                                    hpTotal = float(txt[temp3 + 2:temp3 + 5])
                                    percent = int(hp/hpTotal * 100)
                                    gs.get_team(0).sel().hp = percent
                            damage = txt.rfind("|-damage|p1a: ", temp, i1)
                            heal = txt.rfind("|-heal|p1a: ", temp, i1)
                            if max(damage, heal) > 0:
                                temp = max(damage, heal)
                                temp2 = txt.find("|", temp + 14)
                                if txt[temp2 + 1:temp2 + 6] == "0 fnt":
                                    gs.get_team(0).sel().hp = 0
                                    gs.get_team(0).sel().alive = False
                                    gs.get_team(0).sel().is_mega = False
                                else:
                                    temp3 = txt.find("\/", temp2)
                                    temp4 = txt.find("|", temp3)
                                    hp = float(txt[temp2 + 1:temp3])
                                    hpTotal = float(txt[temp3 + 2:temp3 + 5])
                                    percent = int(hp/hpTotal * 100)
                                    gs.get_team(0).sel().hp = percent
                            prev1 = i1
                        if txt.find("|switch|p2a:", prev2, index) > 0:
                            temp = txt.find("|switch|p2a:", prev2, index)
                            temp2 = txt.find("\/", temp, index)
                            i2 = txt.find("|switch|p2a:", temp2, index)
                            if i2 < 0:
                                i2 = index
                            s = txt[temp:temp2]
                            pokemon = re.split('[^a-zA-Z\d-]', s)[5]
                            i = 0
                            for p in team2:
                                if p.species == pokemon:
                                    gs.switch_pokemon(i, 1)
                                i+=1
                            damage = txt.rfind("|-damage|p2a: ", temp, i2)
                            heal = txt.rfind("|-heal|p2a: ", temp, i2)
                            if max(damage, heal) > 0:
                                temp = max(damage, heal)
                                temp2 = txt.find("|", temp + 14)
                                if txt[temp2 + 1:temp2 + 6] == "0 fnt":
                                    gs.get_team(1).sel().hp = 0
                                    gs.get_team(1).sel().alive = False
                                    gs.get_team(1).sel().is_mega = False
                                else:
                                    temp3 = txt.find("\/", temp2)
                                    temp4 = txt.find("|", temp3)
                                    hp = float(txt[temp2 + 1:temp3])
                                    hpTotal = float(txt[temp3 + 2:temp3 + 5])
                                    percent = int(hp/hpTotal * 100)
                                    gs.get_team(1).sel().hp = percent
                            prev2 = i2
                    #updates gamestate in csv file
                    if turn > 0:
                        statusDict = {
                            "None": 0,
                            "brn": 1,
                            "psn": 2,
                            "par": 3,
                            "slp": 4,
                            "tox": 5,
                            "frz": 6
                            }
                        weatherDict = {
                            "None": 0,
                            "Rain": 1,
                            "Sun": 2,
                            "Sand": 3,
                            "Hail": 4,
                            }
                        terrainDict = {
                            "None": 0,
                            "Electric": 1,
                            "Psychic": 2,
                            "Grassy": 3,
                            "Misty": 4,
                            }
                        bst1 = 0
                        writer.writerow([turn, gs.get_team(0).pokemonList[0].hp, gs.get_team(0).pokemonList[1].hp, gs.get_team(0).pokemonList[2].hp, gs.get_team(0).pokemonList[3].hp, gs.get_team(0).pokemonList[4].hp, gs.get_team(0).pokemonList[5].hp,\
                                         gs.get_team(1).pokemonList[0].hp, gs.get_team(1).pokemonList[1].hp, gs.get_team(1).pokemonList[2].hp, gs.get_team(1).pokemonList[3].hp, gs.get_team(1).pokemonList[4].hp, gs.get_team(1).pokemonList[5].hp,\
                                         gs.get_team(0).pokemonList[0].num, gs.get_team(0).pokemonList[1].num, gs.get_team(0).pokemonList[2].num, gs.get_team(0).pokemonList[3].num, gs.get_team(0).pokemonList[4].num, gs.get_team(0).pokemonList[5].num,\
                                         gs.get_team(1).pokemonList[0].num, gs.get_team(1).pokemonList[1].num, gs.get_team(1).pokemonList[2].num, gs.get_team(1).pokemonList[3].num, gs.get_team(1).pokemonList[4].num, gs.get_team(1).pokemonList[5].num,\
                                         gs.get_team(0).sel().num, gs.get_team(1).sel().num, int(gs.get_team(0).sel().item_exists), int(gs.get_team(1).sel().item_exists),\
                                         gs.get_team(0).sel().stages['atk'], gs.get_team(0).sel().stages['def'], gs.get_team(0).sel().stages['spa'], gs.get_team(0).sel().stages['spd'], gs.get_team(0).sel().stages['spe'],\
                                         gs.get_team(1).sel().stages['atk'], gs.get_team(1).sel().stages['def'], gs.get_team(1).sel().stages['spa'], gs.get_team(1).sel().stages['spd'], gs.get_team(1).sel().stages['spe'],\
                                         statusDict[gs.get_team(0).pokemonList[0].status], statusDict[gs.get_team(0).pokemonList[1].status], statusDict[gs.get_team(0).pokemonList[2].status], statusDict[gs.get_team(0).pokemonList[3].status], statusDict[gs.get_team(0).pokemonList[4].status], statusDict[gs.get_team(0).pokemonList[5].status],\
                                         statusDict[gs.get_team(1).pokemonList[0].status], statusDict[gs.get_team(1).pokemonList[1].status], statusDict[gs.get_team(1).pokemonList[2].status], statusDict[gs.get_team(1).pokemonList[3].status], statusDict[gs.get_team(1).pokemonList[4].status], statusDict[gs.get_team(1).pokemonList[5].status],\
                                         int(gs.get_team(0).sel().seeds), int(gs.get_team(1).sel().seeds), gs.get_team(0).sel().effective, gs.get_team(1).sel().effective, int(gs.get_team(0).sel().taunt), int(gs.get_team(1).sel().taunt),\
                                         int(gs.get_team(0).sel().encore), int(gs.get_team(1).sel().encore), int(gs.get_team(0).sel().disabled), int(gs.get_team(1).sel().disabled), int(gs.get_team(0).sel().sub), int(gs.get_team(1).sel().sub),\
                                         int(gs.get_team(0).sel().is_mega), int(gs.get_team(1).sel().is_mega), int(gs.get_team(0).sel().z_move), int(gs.get_team(1).sel().z_move), int(gs.rocks[0]), int(gs.rocks[1]), gs.spikes[0], gs.spikes[1],\
                                         gs.tspikes[0], gs.tspikes[1], int(gs.webs[0]), int(gs.webs[1]), int(gs.screens[0][0]), int(gs.screens[0][1]), int(gs.screens[1][0]), int(gs.screens[1][1]), weatherDict[gs.weather], terrainDict[gs.terrain], int(gs.room), victor])
                    turn+=1

if __name__ == '__main__':
    dw = Datawriter()
    dw.run()
