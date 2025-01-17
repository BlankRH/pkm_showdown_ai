import pickle
import json

from smogon import Smogon
from team import Team
from gamestate import GameState
from simulator import Simulator
from agent import HumanAgent, PessimisticMinimaxAgent, OptimisticMinimaxAgent
from data import load_data
from simulator import Action

def main():
    from argparse import ArgumentParser
    #see https://docs.python.org/3/library/argparse.html#
    argparser = ArgumentParser()
    argparser.add_argument('team1')
    argparser.add_argument('team2')
    argparser.add_argument('--depth', type=int, default=2)
    argparser.add_argument('--gamestate', type=str)
    argparser.add_argument('--player', type=int, default=0)
    args = argparser.parse_args()

    pokedata = load_data("data")

    players = [None, None]
    #players[args.player] = HumanAgent()
    #self battle
    players[args.player] = PessimisticMinimaxAgent(2, pokedata, log_file="normal.txt")
    players[1 - args.player] = PessimisticMinimaxAgent(2, pokedata, log_file="no_cache.txt", use_cache=False)

    #get team1 & team2
    with open(args.team1) as f1, open(args.team2) as f2, open("data/poke2.json") as f3:
        data = json.loads(f3.read())
        poke_dict = Smogon.convert_to_dict(data)
        teams = [Team.make_team(f1.read(), poke_dict), Team.make_team(f2.read(), poke_dict)]

    #read & write gameState, pickle: https://docs.python.org/3/library/pickle.html
    gamestate = GameState(teams)
    if args.gamestate is not None:
        with open(args.gamestate, 'rb') as fp:
            gamestate = pickle.load(fp)
    with open('cur2.gs', 'wb') as fp:
        pickle.dump(gamestate, fp)

    simulator = Simulator(pokedata)
    
    while not gamestate.is_over():
        print "=========================================================================================="
        print "Player 1 primary:", gamestate.get_team(0).primary()
        print "Player 2 primary:", gamestate.get_team(1).primary()

        my_action = players[0].get_action(gamestate, 0)
        opp_action = players[1].get_action(gamestate, 1)
        gamestate = simulator.simulate(gamestate, [my_action, opp_action], 0, log=True)
    if gamestate.get_team(0).alive():
        print "You win!"
        print "Congrats to", gamestate.opp_team
        print "Sucks for", gamestate.my_team
    else:
        print "You lose!"
        print "Congrats to", gamestate.my_team
        print "Sucks for", gamestate.opp_team
