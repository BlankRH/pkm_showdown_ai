from smogon import SmogonMoveset
import json
import re
from mega_items import mega_items
from math import floor

import logging
logging.basicConfig()

class Pokemon():
    def __init__(self, name):
        self.species = name
        txt = open("data/pokedex.txt").read()
        index1 = txt.find("types: ", txt.find("species: \"" + name))
        index2 = txt.find("]", index1)
        types = txt[index1 + 7:index2 + 1]
        self.typing = eval(types, {'__builtins__':None}, {})
        index1 = txt.find("baseStats: ", txt.find("species: \"" + name))
        index2 = txt.find("}", index1)
        stats = txt[index1 + 11:index2 + 1]
        self.stats = eval(stats, {'__builtins__':None}, {})
        index1 = txt.find("num: ", txt.find("species: \"" + name))
        index2 = txt.find(",", index1)
        self.num = int(txt[index1 + 5:index2]) - 1
        self.hp = 100
        self.status = "None"
        self.item_exists = True
        self.taunt = False
        self.disabled = False
        self.encore = False
        self.is_mega = False
        self.alive = True
        self.choiced = False
        self.seeds = False
        self.sub = False
        self.effective = 0
        self.z_move = False
        self.stages = {
            'atk': 0,
            'spa': 0,
            'def': 0,
            'spd': 0,
            'spe': 0,
            'acc': 0,
            'eva': 0
        }

    def damage(self, amount):
            self.health = floor(max(0, self.health - amount))

    def damage_percent(self, percent):
        damage = percent * self.final_stats['hp']
        self.health = floor(max(0, self.health - damage))
        return damage

    def heal(self, percent):
        self.health = floor(min(self.final_stats['hp'], self.health + percent * self.final_stats['hp']))

    def get_stage(self, stat):
        return self.stages[stat]

    def increase_stage(self, stat, amount):
        assert amount > 0
        self.stages[stat] = min(6, self.stages[stat] + amount)

    def decrease_stage(self, stat, amount):
        assert amount > 0
        self.stages[stat] = max(-6, self.stages[stat] - amount)
        if self.ability == "Defiant":
            logging.debug("%s has Defiant and sharply increased attack." % self)
            self.increase_stage('atk', 2)
        elif self.ability == "Competitive":
            self.increase_stage('spa', 2)
            logging.debug("%s has Competitive and sharply increased special attack." % self)

    def meloetta_evolve(self):
        assert self.species == "Meloetta"
        if "Psychic" in self.typing:
            stats = {
                "hp": 100,
                "atk": 128,
                "def": 90,
                "spa": 77,
                "spd": 77,
                "spe": 128
            }
            typing = ['Normal', 'Fighting']
        elif "Fighting" in self.typing:
            stats = {
                "hp": 100,
                "atk": 77,
                "def": 77,
                "spa": 128,
                "spd": 128,
                "spe": 90
            }
            typing = ['Normal', 'Psychic']
        self.set_stats(stats)
        self.typing = typing

    def meloetta_reset(self):
        stats = {
            "hp": 100,
            "atk": 77,
            "def": 77,
            "spa": 128,
            "spd": 128,
            "spe": 90
        }
        self.set_stats(stats)
        self.typing = ['Normal', 'Psychic']

    def reset_stages(self):
        self.stages = {
            'atk': 0,
            'spa': 0,
            'def': 0,
            'spd': 0,
            'spe': 0,
            'acc': 0,
            'eva': 0
        }

    def reset_typing(self):
        self.typing = self.old_typing

    def set_status(self, status):
        self.status = status

    def set_last_move(self, move):
        self.last_move = move

    def set_encore(self, encore):
        self.encore = encore

    def set_disabled(self, move):
        self.disabled = move

    def set_taunt(self, taunt):
        self.taunt = taunt

    def reset_taunt(self):
        self.set_taunt(False)

    def reset_status(self):
        self.set_status(None)

    def reset_disabled(self):
        self.set_disabled(None)

    def reset_last_move(self):
        self.set_last_move(None)

    def reset_encore(self):
        self.set_encore(False)

    def can_evolve(self):
        if self.is_mega:
            return False
        if self.item in mega_items:
            if self.species == mega_items[self.item][0]:
                return True
        return False

    def mega_evolve(self, pokedata, log=False):
        if self.can_evolve():
            name = mega_items[self.item][1]
            mega_poke = pokedata.mega_data[name]
            typing = mega_poke.typing
            stats = mega_poke.stats
            ability = mega_poke.movesets[0]['ability']
            moveset = smogon.SmogonMoveset(self.moveset.species, None, ability, self.moveset.evs, self.moveset.nature, self.moveset.moves, tag=self.moveset.tag)
            status = self.status
            disabled = self.disabled
            taunt = self.taunt
            last_move = self.last_move
            encore = self.last_move
            poke = Pokemon(name)
            poke.health = self.health
            return poke
        return self

    def copy(self):
        poke = Pokemon(self.species)
        poke.final_stats = self.final_stats
        poke.health = self.health
        poke.ability = self.ability
        poke.item = self.item
        poke.stages = self.stages.copy()
        poke.is_mega = self.is_mega
        poke.choiced = self.choiced
        if self.choiced:
            poke.move_choice = self.move_choice
        return poke

    def to_tuple(self):
        return (self.species, self.item, self.health, tuple(self.typing), self.status, self.taunt, self.disabled, self.last_move, self.encore, tuple(self.stages.values()))

    def __repr__(self):
        return "%s(%u)" % (self.species, self.health)

class Team():
    def __init__(self, pokemon):
        self.pokemonList = pokemon
        self.selected = 0

    def copy(self):
        team = Team([p.copy() for p in self.pokemonList])
        team.selected = self.selected
        return team

    def to_tuple(self):
        return (self.selected, tuple(x.to_tuple() for x in self.pokemonList))

    @staticmethod
    def from_tuple(tupl):
        team = Team(poke.from_tuple() for poke in tupl[1])
        team.selected = tupl[0]
        return team

    def sel(self):
        if self.selected is None:
            return None
        else:
            return self.pokemonList[self.selected]

    def setSelect(self, primary):
        if primary is None:
            self.selected = None
            return
        self.selected = primary
        self.sel().choiced = False
        self.sel().reset_stages()

    @staticmethod
    def convert_nature(nature):
        nature_dict = {"hp": 1.0, "patk": 1.0, "pdef": 1.0, "spatk": 1.0, "spdef": 1.0, "spe": 1.0}
        if nature == "Lonely":
            nature_dict['patk'] = 1.1
            nature_dict['pdef'] = 0.9
        elif nature == "Brave":
            nature_dict['patk'] = 1.1
            nature_dict['spe'] = 0.9
        elif nature == "Adamant":
            nature_dict['patk'] = 1.1
            nature_dict['spatk'] = 0.9
        elif nature == "Naughty":
            nature_dict['patk'] = 1.1
            nature_dict['spdef'] = 0.9
        elif nature == "Bold":
            nature_dict['pdef'] = 1.1
            nature_dict['patk'] = 0.9
        elif nature == "Relaxed":
            nature_dict['pdef'] = 1.1
            nature_dict['spe'] = 0.9
        elif nature == "Impish":
            nature_dict['pdef'] = 1.1
            nature_dict['spatk'] = 0.9
        elif nature == "Lax":
            nature_dict['pdef'] = 1.1
            nature_dict['spdef'] = 0.9
        elif nature == "Timid":
            nature_dict['spe'] = 1.1
            nature_dict['patk'] = 0.9
        elif nature == "Hasty":
            nature_dict['spe'] = 1.1
            nature_dict['pdef'] = 0.9
        elif nature == "Jolly":
            nature_dict['spe'] = 1.1
            nature_dict['spatk'] = 0.9
        elif nature == "Naive":
            nature_dict['spe'] = 1.1
            nature_dict['spdef'] = 0.9
        elif nature == "Modest":
            nature_dict['spatk'] = 1.1
            nature_dict['patk'] = 0.9
        elif nature == "Mild":
            nature_dict['spatk'] = 1.1
            nature_dict['pdef'] = 0.9
        elif nature == "Quiet":
            nature_dict['spatk'] = 1.1
            nature_dict['spe'] = 0.9
        elif nature == "Rash":
            nature_dict['spatk'] = 1.1
            nature_dict['spdef'] = 0.9
        elif nature == "Calm":
            nature_dict['spdef'] = 1.1
            nature_dict['patk'] = 0.9
        elif nature == "Gentle":
            nature_dict['spdef'] = 1.1
            nature_dict['pdef'] = 0.9
        elif nature == "Sassy":
            nature_dict['spdef'] = 1.1
            nature_dict['spe'] = 0.9
        elif nature == "Careful":
            nature_dict['spdef'] = 1.1
            nature_dict['spatk'] = 0.9
        return nature_dict

    @staticmethod
    def make_team(text, data):
        poke_list = []
        text_lines = text.split("\n\n")[:6]
        for tl in text_lines:
            if tl.strip() == "":
                continue
            line = tl.strip().split('\n')
            if "(M)" in line[0]:
                line[0] = line[0].replace(" (M)", "")
            if "(F)" in line[0]:
                line[0] = line[0].replace(" (F)", "")
            match = re.search(r'(.+?)\s*(\((.+?)\))?\s*(@ (.+?))?$', line[0])
            nickname = match.group(1)
            name = match.group(3)
            item = match.group(5)
            if name is None:
                name = nickname
            ability = line[1][9:]
            moves = [x[2:] for x in line[4:]]
            ev_list = line[2].split("/")
            ev_list[0] = ev_list[0][4:]
            evs = {'spatk': 0, 'pdef': 0, 'hp': 0, 'spdef': 0, 'patk': 0, 'spe': 0}
            for ev in ev_list:
                if 'HP' in ev:
                    hp = int(''.join(s for s in ev if s.isdigit()))
                    evs['hp'] = hp
                if 'Atk' in ev:
                    patk = int(''.join(s for s in ev if s.isdigit()))
                    evs['patk'] = patk
                if 'Def' in ev:
                    pdef = int(''.join(s for s in ev if s.isdigit()))
                    evs['pdef'] = pdef
                if 'SpA' in ev:
                    spa = int(''.join(s for s in ev if s.isdigit()))
                    evs['spatk'] = spa
                if 'SpD' in ev:
                    spd = int(''.join(s for s in ev if s.isdigit()))
                    evs['spdef'] = spd
                if 'Spe' in ev:
                    spe = int(''.join(s for s in ev if s.isdigit()))
                    evs['spe'] = spe
            nature = line[3][:-7]
            nature = Team.convert_nature(nature)
            moveset = SmogonMoveset(name, item, ability, evs, nature, moves, tag=None)
            typing = data[name].typing
            stats = data[name].stats
            poke = Pokemon(name)
            poke_list.append(poke)
        return Team(poke_list)

    def __getitem__(self, index):
        return self.pokemonList.__getitem__(index)

    def __repr__(self):
        return "[" + ', '.join([repr(x) for x in self.pokemonList]) + "]"

class GameState():
    def __init__(self, teams):
        self.teams = teams
        self.rocks = [False, False]
        self.spikes = [0, 0]
        self.tspikes = [0, 0]
        self.webs = [False, False]
        self.screens = [(False, False), (False, False)]
        self.weather = "None"
        self.room = False
        self.terrain = "None"

    def deep_copy(self):
        state = GameState([x.copy() for x in self.teams])
        state.rocks = self.rocks[:]
        state.spikes = self.spikes[:]
        state.webs = self.webs[:]
        state.screens = self.screens[:]
        state.weather = self.weather
        state.room = self.room
        state.terrain = self.terrain
        return state

    def set_rocks(self, who, rock_bool):
        self.rocks[who] = rock_bool

    def add_spikes(self, who):
        self.spikes[who] += 1

    def get_team(self, team):
        return self.teams[team]

    def to_tuple(self):
        return (tuple(x.to_tuple() for x in self.teams), (self.rocks[0], self.rocks[1], self.spikes[0], self.spikes[1]))

    @staticmethod
    def from_tuple(tupl):
        return GameState([team.from_tuple() for team in tupl[0]])

    def switch_pokemon(self, switch_index, who, log=False):
        my_team = self.get_team(who)
        opp_team = self.get_team(1 - who)
        if my_team.sel().species == "Meloetta":
            my_team.sel().meloetta_reset()
        my_team.setSelect(switch_index)
        my_poke = my_team.sel()
        my_poke.reset_taunt()
        my_poke.reset_disabled()
        my_poke.reset_last_move()
        my_poke.reset_encore()
        opp_poke = opp_team.sel()
        if log:
            print (
            "%s switched in." % my_poke
            )
        if my_poke.ability == "Intimidate":
            if log:
                print ("%s got intimidated." % opp_poke)
                opp_poke.decrease_stage('atk', 1)

    def is_over(self):
            return not (self.teams[0].alive() and self.teams[1].alive())

if __name__ == "__main__":
        poke = Pokemon("Bulbasaur")

#Team: game/showdown
#Pokemon: handlers.py
