import os
import pickle
import neat

from Classes.Deck import Deck
from Classes.Graph import Graph
from Classes.Player import Player

from config import C_HANDS_PER_GENERATION, C_FITNESS_THRESHOLD, C_NEAT_CONFIG_DEFAULTS, C_POP_PER_GEN
from helper import display_game_results, display_sim_results, network, deal_two_each, reward_genomes_for_wins, average

# Globals to keep track of
G_gen = 0
G_hall_of_fame = []
G_ao10 = []


# What will evaluate our genomes
def eval_genomes(genome, config):
    # Grab our globals
    global G_gen
    global G_hall_of_fame

    # Increment generation
    G_gen += 1

    # Make our empty lists of players, genomes, and N networks
    players = []
    nets = []
    ge = []

    # Set an impossibly low best fitness, so we can easily find our best of each generation
    best_fitness = -1000
    best_player = Player()

    # For each genome...
        # Give them a starting fitness of 0

    g = genome

    g.fitness = 0

    # Add players, neural networks, and genomes to our own lists
    players.append(Player())
    nets.append(network(g, config))
    ge.append(g)

    # For every hand we want to play in a simulation...
    for i in range(C_HANDS_PER_GENERATION*1000):
        # Let's use a new deck each time
        deck = Deck()
        dealer = Player()

        # Deal two cards to each player
        players, deck = deal_two_each(players, deck)

        for _ in range(2):
            deck.deal_to(dealer)

        for j, player in enumerate(players):
            d = Deck()
            d.cards = []
            for card in deck.cards:
                d.cards.append(card)

            # Activation function
            inputs = player.score, player.has_ace, dealer.hand[0].value
            output = nets[j].activate(inputs)

            # While we have less than 17 points, hit, except 10% of the time stay
            while output[0] > 0.5 and player.score < 21:
                player.hit(d)
                ge[j].fitness += 0.1

        # Standard dealer rules, hit on and up to 16
        while dealer.score <= 16:
            dealer.hit(deck)

        players, ge, msg = reward_genomes_for_wins(players, dealer, ge)

        for j, g in enumerate(ge):
            if g.fitness > best_fitness:
                best_fitness = g.fitness
                best_player = players[j]

        # Display the results of the final game
        if i + 1 == C_HANDS_PER_GENERATION:
            display_game_results(best_player, dealer, i, msg)

        # Make sure their hands are empty
        for player in players:
            player.clear_hand()
        dealer.clear_hand()

    # Display the results of the whole simulation
    display_sim_results(best_player)

    return ge[0]


def run(path):
    global G_gen
    global G_hall_of_fame

    with open('winner-feedforward', 'rb') as f:
        p = pickle.load(f)

    config = neat.config.Config(*C_NEAT_CONFIG_DEFAULTS, path)

    winner = eval_genomes(p, config)

    print("Winner (after %s hand of blackjack):" % (C_HANDS_PER_GENERATION * 100))
    print(winner.fitness)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
